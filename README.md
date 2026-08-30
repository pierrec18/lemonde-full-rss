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

Le MVP utilise HTTP uniquement. Aucun mécanisme de contournement n'est prévu ; Playwright reste une extension ultérieure si le HTML authentifié ne contient pas le contenu.
## Backend Playwright (si le site renvoie un Client Challenge)

Le backend HTTP est utilisé par défaut. Si Le Monde renvoie une page `Client Challenge`, utilisez l’image Chromium incluse :

```bash
cp docker-compose.playwright.example.yml docker-compose.playwright.yml
sed -i 's/^FETCHER=.*/FETCHER=playwright/' .env
docker compose -f docker-compose.yml -f docker-compose.playwright.yml up -d --build
```

Le fichier `docker-compose.playwright.yml` est local et peut rester hors Git. Les cookies sont toujours lus depuis `secrets/lemonde-cookies.json` et ne sont jamais journalisés.

## Backend Kiosque

Kiosque peut utiliser l’authentification Le Monde par identifiant et mot de passe. Créez `kiosque-config/kiosque.conf` avec une section `[https://www.lemonde.fr/]`, puis utilisez :

```bash
cp docker-compose.kiosque.example.yml docker-compose.kiosque.yml
docker compose -f docker-compose.yml -f docker-compose.kiosque.yml up -d --build
```

Le mot de passe reste dans le fichier local monté en lecture seule et ne doit jamais être committé.
