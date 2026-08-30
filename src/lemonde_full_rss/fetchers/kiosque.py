import asyncio
import html
import re


def _remove_kiosque_metadata(markdown):
    """Remove Kiosque's one-line metadata header from the article body."""
    lines = markdown.splitlines()
    first = next((i for i, line in enumerate(lines) if line.strip()), None)
    if first is None or not lines[first].lstrip().lower().startswith("title:"):
        return markdown.strip()
    # Kiosque places its metadata on the first paragraph, followed by the
    # article after a blank line. Keep everything after that separator.
    for i in range(first + 1, len(lines)):
        if not lines[i].strip():
            body = "\n".join(lines[i + 1:]).strip()
            if body:
                return body
    return markdown.strip()


class KiosqueArticleFetcher:
    """Use Kiosque's legitimate Le Monde login and article extractor."""

    def __init__(self, settings):
        self.settings = settings

    async def fetch(self, url):
        def extract():
            from kiosque import Website
            return Website.instance(url).full_text(url)

        try:
            markdown = _remove_kiosque_metadata(await asyncio.to_thread(extract))
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
