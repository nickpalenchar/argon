

class BaseException(Exception):
    pass


class TemplateBundleError(Exception):
    """
    An error in the selected template bundle, such as incorrect formatting of the bundle
    and/or missing required parts.
    """
    pass

