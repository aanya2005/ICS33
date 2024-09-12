from grin import GrinLocation


class GrinException(Exception): # Shows all green but not 100% coverage
    def __init__(self, message: str, location: GrinLocation):
        formatted = f'Error during execution: {str(location)}: {message}'
        super().__init__(formatted)
        self._message = message
        self._location = location

    def location(self) -> GrinLocation:
        return self._location