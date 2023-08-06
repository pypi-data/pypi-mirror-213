class CoinNotFound(Exception):
    """Raise when a coin is not found"""
    def __init__(self, coin: str):
        super().__init__(f"'{coin}' coin is not found")

class AcronymNotFound(Exception):
    """Raise when an acronym is not found"""
    def __init__(self, acronym: str):
        super().__init__(f"'{acronym}' is not found")