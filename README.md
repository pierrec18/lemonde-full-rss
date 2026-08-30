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
