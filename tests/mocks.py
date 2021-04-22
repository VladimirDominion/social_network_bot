class MockResponse:
    def __init__(self, text, json, status):
        self._json = json
        self._text = text
        self.status = status

    async def json(self):
        return self._json

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
