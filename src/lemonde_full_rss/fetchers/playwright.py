class PlaywrightArticleFetcher:
    """Extension optionnelle : volontairement non incluse dans l'image MVP."""
    async def fetch(self, url):
        raise RuntimeError('Playwright backend is not installed; use FETCHER=http')
