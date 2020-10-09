

class BaseException(Exception):
    pass


class MissingRequiredValue(BaseException):
    pass


class TemplateBundleError(BaseException):
    """
    An error in the selected template bundle, such as incorrect formatting of the bundle
    and/or missing required parts.
    """
    pass


class TemplateNotFound(BaseException):
    pass
