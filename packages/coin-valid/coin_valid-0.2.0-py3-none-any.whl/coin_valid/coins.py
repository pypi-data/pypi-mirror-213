from coin_valid.exceptions.coin_exceptions import CoinNotFound
from coin_valid.exceptions.network_exceptions import InvalidNetwork

class Acronym:
    def __init__(self):
        """Coin acronyms"""
        self._bitcoin = 'btc'
        self._ethereum = 'eth'
        self._litecoin = 'litecoin'
        self._wownero = 'wow'
        self._bitcoincash = 'bch'
        self._firo = 'firo'

    @staticmethod
    def acronym_getter() -> dict:
        """
        Returns every acronym of every coin

        :return: all coins acronyms
        """
        return Acronym().__dict__


class MAINNET:
    def __init__(self):
        """Mainnet regex strings"""
        self._bitcoin = "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$"
        self._ethereum = "^(0x)[0-9A-Fa-f]{40}$"
        self._litecoin = "^(L|M|3)[A-Za-z0-9]{33}$|^(ltc1)[0-9A-Za-z]{39}$"
        self._wownero = "^W[oW][1-9A-HJ-NP-Za-km-z]{95}"
        self._bitcoincash = "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[0-9A-Za-z]{42,42}$"
        self._firo = "^[a|Z|3|4][0-9A-za-z]{33}$"

    @staticmethod
    def getter() -> dict:
        """
        Returns every regex of every coin

        :return dict: all mainnet regex list
        """
        return MAINNET().__dict__

    @staticmethod
    def coin_getter(coin: str) -> str:
        """
        Returns the regex of the coin

        :param str coin: acronym or full name
        :return str: regex of coin
        """
        mainnet: dict = MAINNET().__dict__
        if not (regex_string := mainnet.get(f'_{coin}', None)):
            raise CoinNotFound(coin)
        return regex_string

class TESTNET:
    def __init__(self):
        """Testnet regex strings"""
        ...

    @staticmethod
    def getter() -> dict:
        """
        Returns every regex of every coin

        :return dict: all testnet regex list
        """
        return TESTNET().__dict__

    @staticmethod
    def coin_getter(coin: str) -> str:
        """
        Returns the regex of the coin

        :param str coin: acronym or full name
        :return str: regex of coin
        """
        testnet: dict = TESTNET().__dict__
        if not (regex_string := testnet.get(f'_{coin}', None)):
            raise CoinNotFound(coin)
        return regex_string

class STAGENET:
    def __init__(self):
        """Stagenet regex strings"""

    @staticmethod
    def getter() -> dict:
        """
        Returns every regex of every coin

        :return dict: all stagenet regex list
        """
        return STAGENET().__dict__

    @staticmethod
    def coin_getter(coin: str) -> str:
        """
        Returns the regex of the coin

        :param str coin: acronym or full name
        :return str: regex of coin
        """
        stagenet: dict = STAGENET().__dict__
        if not (regex_string := stagenet.get(f'_{coin}', None)):
            raise CoinNotFound(coin)
        return regex_string

def all_regex() -> dict:
    """
    Returns all coins in every network with its own regex

    :return dict: all coins in every network with its own regex
    """
    mainnet_regexps: dict = MAINNET.getter()
    testnet_regexps: dict = TESTNET.getter()
    stagenet_regexps: dict = STAGENET.getter()

    regexps: list = {'mainnet': mainnet_regexps, 'testnet': testnet_regexps, 'stagenet': stagenet_regexps}

    return regexps

def coin_regex(coin: str) -> dict:
    """
    Returns all regexps of all coins

    :param str coin: acronym of full name
    :return dict: all regexps of all coins
    """
    coin_regexes: dict = {}
    coin_regexes.update({'coin': {
        'mainnet': MAINNET.coin_getter(coin),
        'testnet': TESTNET.coin_getter(coin),
        'stagenet': STAGENET.coin_getter(coin)
    }})
    return coin_regexes

def network_coin_regex(coin: str, network: str = 'mainnet') -> str:
    """
    Returns regex string based on coin and network

    :param str coin: acronym or full name
    :param str network: mainnet, testnet, stagenet
    :raise: InvalidNetwork if network is not mainner, stagenet or testnet
    :return str: coin string or
    """
    if network == 'mainnet':
        return MAINNET.coin_getter(coin)
    elif network == 'testnet':
        return TESTNET.coin_getter(coin)
    elif network == 'stagenet':
        return STAGENET.coin_getter(coin)
    else:
        raise InvalidNetwork(network)