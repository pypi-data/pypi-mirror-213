class InvalidAddress(Exception):
    """Raise when address is not valid"""
    def __init__(self, address: str, coin: str, network: str = 'mainnet'):
        super().__init__(f"'{address}' is not valid for '{coin} {network}'")

class AddressMatchNotFound(Exception):
    """Raise when address doesn't match any coin"""
    def __init__(self, address: str):
        super().__init__(f"'{address}' is invalid")

class AddressNetworkMatchNotFound(Exception):
    """Raise when address doesn't match any network"""
    def __init__(self, address: str):
        super().__init__(f"'{address}' is invalid")