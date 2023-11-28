class BaseAppException(Exception):
    """Common base class for all app exception"""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.detail = args[0]
        else:
            self.detail = kwargs.get("detail", "")


class HTTPException(BaseAppException):
    """Class for all http exception"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = kwargs.get("code", "")


class DBError(BaseAppException):
    pass


class Forbidden(BaseAppException):
    pass


class EntityDoesntExist(BaseAppException):
    pass


class NotRequiredContent(BaseAppException):
    pass


class EntityAlreadyExists(BaseAppException):
    pass


class OldPasswordIsIncorrect(BaseAppException):
    pass


class NonSensitiveException(BaseAppException):
    pass
