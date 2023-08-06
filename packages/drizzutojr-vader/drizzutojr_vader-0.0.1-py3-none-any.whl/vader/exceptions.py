def vader_exception_handler(exception):
    if type(exception.message) == dict:
        exception.message["internal_code"] = exception.internal_code
        return exception.message, exception.status_code
    else:
        return {
            "message": str(exception.message),
            "internal_code": exception.internal_code,
        }, exception.status_code


class VaderCommonException(Exception):
    def __init__(self, message, internal_code=None, status_code=400):
        self.message = message
        self.internal_code = internal_code
        self.status_code = status_code
        super().__init__()


class VaderConfigException(VaderCommonException):
    """Bad Configuration passed to Vader"""


class VaderUnauthorizedException(VaderCommonException):
    """Unauthorized request to a project"""


class VaderMongoException(VaderCommonException):
    """Unauthorized request to a project"""


class VaderVaultException(VaderCommonException):
    """Unauthorized request to a project"""


class VaderGeneralException(VaderCommonException):
    """Unauthorized request to a project"""
