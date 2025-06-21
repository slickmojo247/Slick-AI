class GalacticMode:
    def __init__(self):
        self.personas = {
            "homer": self._homer_response,
            "cosmic": self._cosmic_response
        }

    def transform(self, text: str, mode: str) -> str:
        if mode in self.personas:
            return self.personas[mode](text)
        return text

    def _homer_response(self, text: str) -> str:
        return f"Mmm... {text.lower()} *drinks beer*"

    def _cosmic_response(self, text: str) -> str:
        return f"✨ {text.upper()} 🌌"
