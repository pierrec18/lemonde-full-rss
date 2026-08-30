from lemonde_full_rss.config import load_cookies

class PlaywrightArticleFetcher:
    """Fetch an article in a real Chromium session using the user's cookies."""
    def __init__(self, settings):
        self.s = settings

    async def fetch(self, url):
        from playwright.async_api import async_playwright
        cookies = load_cookies(self.s.cookies)
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=self.s.ua)
            if cookies:
                await context.add_cookies([
                    {'name': name, 'value': value, 'domain': '.lemonde.fr', 'path': '/'}
                    for name, value in cookies.items()
                ])
            page = await context.new_page()
            response = await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(3000)
            html = await page.content()
            low = html.lower()
            auth = ('client challenge' in low or 'javascript is disabled' in low or
                    'connexion' in low or 'paywall' in low) and len(html) < 100000
            code = response.status if response else 0
            await browser.close()
            return code, html, auth
