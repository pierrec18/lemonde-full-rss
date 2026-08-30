from .generic import extract
class LeMondeExtractor:
    """Point d'extension pour les sélecteurs spécifiques au Monde."""
    def extract(self, html, url=''):
        return extract(html, url)
