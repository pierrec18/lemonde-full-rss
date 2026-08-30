import asyncio
import html
import re


class KiosqueArticleFetcher:
    """Use Kiosque's legitimate Le Monde login and article extractor."""

    def __init__(self, settings):
        self.settings = settings

    async def fetch(self, url):
        def extract():
            from kiosque import Website
            return Website.instance(url).full_text(url)

        try:
            markdown = await asyncio.to_thread(extract)
            if not markdown:
                return 200, "", True
            # Kiosque returns Markdown; create a small HTML document for the
            # existing generic extractor and RSS content:encoded pipeline.
            try:
                import markdown as md
                body = md.markdown(markdown, extensions=["extra", "sane_lists"])
            except ImportError:
                body = "<p>" + "</p><p>".join(
                    html.escape(x.strip()) for x in re.split(r"\n\s*\n", markdown) if x.strip()
                ) + "</p>"
            return 200, f"<html><body><article>{body}</article></body></html>", False
        except Exception:
            return 0, "", True
