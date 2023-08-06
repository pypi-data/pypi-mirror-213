from coin_valid.coins import Acronym
from coin_valid.exceptions.coin_exceptions import CoinNotFound, AcronymNotFound


class Utils:

    @staticmethod
    def get_acronym(coin: str) -> str:
        """
        Converts coin name to acronym

        :param str coin: coin name
        :raise: CoinNotFound if coin is not found
        :return str: coin acronym
        """
        acronyms: dict = Acronym.acronym_getter()
        if not (acronym := acronyms.get(f'_{coin}', None)):
            raise CoinNotFound(coin)
        return acronym

    @staticmethod
    def get_name(acronym: str) -> str:
        """
        Converts coin acronym to name

        :param str acronym: coin acronym
        :return str: coin name
        :raise: AcronymNotFound if acronym is not found
        """
        acronyms: dict = Acronym.acronym_getter()
        acronyms_list: list = list(acronyms.values())
        try:
            index = acronyms_list.index(acronym)
            name = list(acronyms)[index].replace('_', '')
            return name
        except ValueError:
            raise AcronymNotFound(acronym)
