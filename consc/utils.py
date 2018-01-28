"""Utility functions and decorators for consc."""

###################################################################################################
###################################################################################################

def check_extract(tag, label):

    try:
        return tag.find(label).text
    except:
        return None

###################################################################################################
###################################################################################################

def CatchNone(func):
    """Decorator function to catch and return None,
                if given as argument."""

    def wrapper(arg):

        if arg is not None:
            return func(arg)
        else:
            return None

    return wrapper
