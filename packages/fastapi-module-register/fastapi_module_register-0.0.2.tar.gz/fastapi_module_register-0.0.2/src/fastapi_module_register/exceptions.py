class BaseRegisterException(Exception):
    """
    Base Register Exception.
    """

class ConfigurationError(BaseRegisterException):
    """
    The ConfigurationError exception is raised when the configuration of the ORM is invalid.
    """
