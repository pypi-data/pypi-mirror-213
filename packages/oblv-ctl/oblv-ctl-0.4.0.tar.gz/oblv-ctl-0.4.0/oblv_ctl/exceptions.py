"""exceptions.py

Module for defining exception types
"""

HTTP_CLIENT_ERROR_MESSAGE = "An HTTP Client raised an unhandled exception. Kindly raise a request to the support team, along with the {} for resolution."


def _exception_from_packed_args(exception_cls, args=None, kwargs=None):
    # This is helpful for reducing Exceptions that only accept kwargs as
    # only positional arguments can be provided for __reduce__
    # Ideally, this would also be a class method on the OblvError
    # but instance methods cannot be pickled.
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    return exception_cls(*args, **kwargs)


class OblvError(Exception):
    """
    The base exception class for Oblivious exceptions.

    :ivar msg: The descriptive message associated with the error.
    """

    fmt = "An unspecified error occurred"

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs

    def __reduce__(self):
        return _exception_from_packed_args, (self.__class__, None, self.kwargs)


class HTTPClientError(OblvError):
    """HTTPClientError

    Exception to be raised on status code 500 for requests
    """

    fmt = "An HTTP Client raised an unhandled exception. Kindly raise a request to the support team, along with the {request_id} for resolution."

    def __init__(self, request_id=""):
        super().__init__(request_id=request_id)


class ValidationError(OblvError):
    """
    An exception occurred validating parameters.

    Subclasses must accept a ``value`` and ``param``
    argument in their ``__init__``.

    :ivar value: The value that was being validated.
    :ivar param: The parameter that failed validation.
    :ivar type_name: The name of the underlying type.
    """

    fmt = "Invalid value ('{value}') for param {param} of type {type_name} "

    def __init__(self, value="", param="", type_name=""):
        super().__init__(value=value, param=param, type_name=type_name)


class ParamValidationError(OblvError):
    """ParamValidationError

    To be raised when request arguments are invalid
    """

    fmt = "{report}"


class UnauthorizedTokenError(OblvError):
    """UnauthorizedTokenError

    To be raised when expired token is used for requests.
    """

    fmt = (
        "The session associated with this profile has expired or is "
        "otherwise invalid. To refresh this session use the authenticate method "
        "with the corresponding profile."
    )


class BadRequestError(OblvError):
    """BadRequestError

    To be raised on request status code 400
    """

    fmt = "{message}"

    def __init__(self, message=""):
        super().__init__(message=message)


class AuthenticationError(OblvError):
    """AuthenticationError

    To be raised for invalid credentials use.
    """

    fmt = "Invalid credentials provided. Kindly verify the same and try again."


class BadYamlData(OblvError):
    """BadYamlData

    To be raised for invalid service yaml data
    """

    fmt = "Validation failed for service yaml data with message - {message}"

    def __init__(self, message=""):
        super().__init__(message=message)
