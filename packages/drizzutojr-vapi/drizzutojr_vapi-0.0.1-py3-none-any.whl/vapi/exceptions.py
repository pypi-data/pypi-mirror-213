class VAPIPermissionDeniedError(Exception):
    """Vault returned permission denied"""


class VAPISealedError(Exception):
    """Vault is sealed"""


class VAPIAcceptedStatusCodeError(Exception):
    """The Status Code returned from Vault does match the accepted status codes set by the user"""


class VAPIGenericError(Exception):
    """Vault returned an Error"""
