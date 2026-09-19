# Le Monde Full RSS

Service auto-hébergé qui découvre les articles via les RSS officiels et conserve le contenu accessible par une session de cookies locale.

## Déploiement

```sh
cp .env.example .env
cp config/feeds.example.yaml config/feeds.yaml
mkdir -p data secrets
# déposer un export JSON de cookies navigateur dans secrets/lemonde-cookies.json
docker compose up -d --build
curl http://localhost:8000/health
```

Les flux sont `/lemonde/une.xml` et `/lemonde/all.xml`. Activez `RSS_AUTH_ENABLED=true` puis utilisez `?token=...`. Le fichier de cookies est monté en lecture seule et exclu de Git. N'exposez pas le port : utilisez le réseau partagé de NGINX Proxy Manager si nécessaire.

POC : `python scripts/test_article.py URL --save-html /tmp/article.html`.

```sh
python -m pytest
```

Le backend HTTP sert surtout au développement et aux diagnostics. Pour le déploiement de production avec extraction du texte intégral, utilisez **Kiosque** comme décrit ci-dessous.

## Backend Playwright (si le site renvoie un Client Challenge)

Le backend HTTP est utilisé par défaut. Si Le Monde renvoie une page `Client Challenge`, utilisez l’image Chromium incluse :

```bash
cp docker-compose.playwright.example.yml docker-compose.playwright.yml
sed -i 's/^FETCHER=.*/FETCHER=playwright/' .env
docker compose -f docker-compose.yml -f docker-compose.playwright.yml up -d --build
```

Le fichier `docker-compose.playwright.yml` est local et peut rester hors Git. Les cookies sont toujours lus depuis `secrets/lemonde-cookies.json` et ne sont jamais journalisés.

## Backend Kiosque — configuration de production recommandée

[Kiosque](https://www.xoolive.org/kiosque/) assure l’authentification Le Monde et l’extraction du texte intégral. Créez `kiosque-config/kiosque.conf` avec une section `[https://www.lemonde.fr/]`, puis préparez l’override local :

```bash
cp docker-compose.kiosque.example.yml docker-compose.kiosque.yml
```

Toutes les commandes qui créent ou recréent le service doivent ensuite inclure **les deux fichiers Compose** :

```bash
docker compose \
  -f docker-compose.yml \
  -f docker-compose.kiosque.yml \
  up -d --build
```

Utilisez également les deux fichiers pour les commandes d’exploitation afin d’éviter toute ambiguïté :

```bash
# État
docker compose -f docker-compose.yml -f docker-compose.kiosque.yml ps

# Journaux
docker compose -f docker-compose.yml -f docker-compose.kiosque.yml logs -f --tail 50 lemonde-full-rss

# Recréation après une modification
docker compose -f docker-compose.yml -f docker-compose.kiosque.yml up -d --build --force-recreate
```

Vérifiez le backend réellement actif après chaque recréation :

```bash
docker compose \
  -f docker-compose.yml \
  -f docker-compose.kiosque.yml \
  exec -T lemonde-full-rss \
  python -c 'from lemonde_full_rss.config import Settings; print(Settings().fetcher)'
```

La sortie attendue est `kiosque`. Un simple `docker compose up -d` sans l’override peut recréer le service avec le backend HTTP : les articles sont alors découverts mais leur contenu intégral peut échouer à l’extraction et ils n’apparaissent pas dans le flux généré.

Le mot de passe reste dans le fichier local monté en lecture seule et ne doit jamais être committé.

## Diagnostic d’un flux figé

1. Comparez la source officielle et le flux généré.
2. Vérifiez l’URL réellement montée dans `/app/config/feeds.yaml`. La Une utilise actuellement `https://www.lemonde.fr/rss/une.xml` ; l’ancienne URL `/rss/tag/une.xml` renvoie HTTP 404.
3. Contrôlez `/health`, mais ne vous fiez pas uniquement à `last_refresh` : la boucle peut terminer sans nouvel article si la source renvoie une page d’erreur ou un flux vide.
4. Vérifiez que `Settings().fetcher` vaut bien `kiosque` avec la commande ci-dessus.
5. Consultez les journaux et les statuts `extraction_status` si les articles sont présents dans SQLite mais absents du XML. Le rendu RSS ne publie que les articles dont l’extraction est marquée `success`.
