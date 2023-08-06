class InvalidNetwork(Exception):
    """Raise when network is not valid"""
    def __init__(self, network: str):
        super().__init__(f"'{network}' is not a valid network")
