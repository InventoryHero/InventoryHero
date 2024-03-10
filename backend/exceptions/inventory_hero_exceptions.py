class InventoryHeroBaseException(Exception):
    pass


class UnknownDatabaseType(InventoryHeroBaseException):
    pass


class MissingSmtpConfig(InventoryHeroBaseException):
    pass


class InvalidAppUrl(InventoryHeroBaseException):
    pass


class UnsupportedSmtpProtocol(InventoryHeroBaseException):
    pass
