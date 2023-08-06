class CxCliException(Exception):
    ...


class RefreshTokenExpiredException(CxCliException):
    ...


class UnauthenticatedException(CxCliException):
    ...
