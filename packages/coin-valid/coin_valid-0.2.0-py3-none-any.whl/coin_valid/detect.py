import re

from coin_valid.coins import all_regex
from coin_valid.exceptions.address_exceptions import AddressMatchNotFound, AddressNetworkMatchNotFound


class Detect:

    @staticmethod
    def detect_coin(address: str) -> str:
        """
        Detects coin from an address

        :param str address: address
        :return str: coin
        :raise: AddressMatchNotFound if address doesn't match any coin
        """
        regex_list: dict = all_regex()
        for network in regex_list.keys():
            for regex in (current_list := regex_list[network].values()):
                if re.match(regex, address):
                    coin_list: list = list(regex_list[network].keys())
                    match: int = list(current_list).index(regex)
                    resulting_coin: str = coin_list[match].replace('_', '')
                    return resulting_coin
        raise AddressMatchNotFound(address)

    @staticmethod
    def detect_network(address: str) -> str:
        """
        Detects network from on address

        :param str address: address
        :return str: network
        :raise: AddressNetworkMatchNotFound if address doesn't match any network
        """
        regex_list: dict = all_regex()
        for network in regex_list.keys():
            for regex in (current_list := regex_list[network].values()):
                if re.match(regex, address):
                    return network
        raise AddressNetworkMatchNotFound(address)