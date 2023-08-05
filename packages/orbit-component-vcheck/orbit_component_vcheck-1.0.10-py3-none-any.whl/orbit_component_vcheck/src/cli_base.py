class CliBase:

    COLLECTIONS = []

    def __init__ (self, odb):
        self._odb = odb

    def setup (self):
        for cls in self.COLLECTIONS:
            cls().open(self._odb)
        return self
