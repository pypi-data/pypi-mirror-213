import re

from coin_valid.coins import network_coin_regex
from coin_valid.exceptions.address_exceptions import InvalidAddress
class Validate:
    """Validation class"""

    @staticmethod
    def validate(address: str, coin: str, network: str = 'mainnet') -> bool:
        """
        Checks if address is valid for specific coin and network

        :param str address: address
        :param str coin: acronym or full name
        :param str network: mainnet, stagenet, testnet
        :raise: InvalidAddress if address is not valid
        :return bool: True
        """
        regex = network_coin_regex(coin, network)
        if not re.match(regex, address):
            raise InvalidAddress(address, coin, network)
        return True


