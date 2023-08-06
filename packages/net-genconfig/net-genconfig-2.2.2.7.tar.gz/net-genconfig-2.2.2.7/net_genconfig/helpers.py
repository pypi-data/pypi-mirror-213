# net_genconfig.helpers



import re
import sys



# dictionary containing the helper functions - the keys are the names
# of the functions available in Jinja2 and the values are the function
# references themselves
#
# after each function is defined, below, it is added to this dictionary
#
# this dictionary is available to the caller to iterate through and add
# all the functions in this file.

helpers = {}



# --- exceptions ---



class HelperBaseException(BaseException):
    """Base class for exceptions raised explicitly through helper functions.

    This class can be caught in a 'try ... except HelperBaseException' block
    to determine the exception is explicit rather than something
    unexpected/uncaught failing.  This usually means the exception can be
    printed as a simple one line error, rather than raising the entire call
    stack, which can be confusing for errors with clear explanations.

    It doesn't actually do anything but just exists as an exception class to
    match on.
    """

    pass


class HelperException(Exception, HelperBaseException):
    """Child of Exception for use in helper functions.

    See HelperBaseException for an explanation.
    """

    pass


class HelperAssertionError(AssertionError, HelperBaseException):
    """Child of AssertionError for use in helper functions.

    See HelperBaseException for an explanation.
    """
    pass



# --- helper functions ---



def warn_helper(msg):
    """Helper function to print a warning inside a Jinja2 template.
    The supplied message is printed to stderr but execution is not
    stopped.

    Keyword arguments:

    msg -- warning message to display
    """

    print("warning:", msg, file=sys.stderr)


    # helper functions return a string to be included in the template;
    # we don't particularly have anything to include but have to return
    # something, so we return an empty string

    return ""


helpers["warn"] = warn_helper



def raise_helper(msg):
    """Helper function to raise an exception inside a Jinja2 template.
    The generic 'Exception' class is raised in Python.

    Keyword arguments:

    msg -- exception message to display when aborting
    """

    raise HelperException(msg)


helpers["raise"] = raise_helper



def undef_helper(var):
    """Helper function that is a simple wraparound for raise() that will
    add the leading string 'undefined:' to the message.

    It is intended for use to trap undefined variables that would
    otherwise just default to an empty string.  It is intended to be
    called with something such as '{{ dict.key or undef("dict.key") }}'.

    Note that a general exception will be raised if a parent dictionary
    (or similar) does not exist anyway - so if 'dict' didn't exist, in
    the example above, this would fault: this is just intended to catch
    the ones where the leaf portion is undefined and would default.
    """

    raise_helper("undefined: " + var)


helpers["undef"] = undef_helper



def assert_helper(condition, msg):
    """Helper function for assertions inside a Jinja2 template.  If the
    supplied condition is False, an exception is raised with the given
    error message.  The 'AssertionError' class is raised by Python.

    If the condition is True, an empty string is returned to avoid
    printing anything.

    Keyword arguments:

    condition -- the condition which must be satisfied to not raise the
    exception

    msg -- message to display in the event of the condition not being
    true
    """

    if not condition:
        raise HelperAssertionError(msg)

    return ""


helpers["assert"] = assert_helper



def re_match_helper(pattern, string):
    """Helper function for matching strings against regular expressions
    in a Jinja2 template: a boolean is returned, indicating whether the
    match succeeded or not.

    This is a wrapper around re.match().

    Keyword arguments:

    pattern -- the regular expression to match against

    string -- the string to match against
    """

    return bool(re.match(pattern, string))


helpers["re_match"] = re_match_helper



def re_match_group_helper(pattern, string, *groups, no_match_msg=None):
    """Helper function for matching strings against regular expressions
    and extract selected groups (marked by parentheses) of text in a
    Jinja2 template, returning them in the form of a tuple, one for
    each group, in order.

    The desired groups are identified either by number (0 for the first
    one, by opening bracket, 1 for the second, etc.) or by name (using
    the syntax '(?P<name>...)'.  These styles can be mixed.

    This is a wrapper around re.match().group() (re.match() returns a
    Match object and group() is called on that).

    If the match fails, a ValueError() is raised, giving the pattern and
    string.  A customised error, raised using HelperException(), can be
    supplied with no_match_msg.  To avoid raising an exception, the
    string must be separately matched with re_match_helper() first.

    Keyword arguments:

    pattern -- the regular expression to match against; the required
    groups to return should be specified using parentheses

    string -- the string to match and return the groups of

    *groups -- a list of arguments giving the numbers or names of the
    desired match groups

    no_match_msg=None -- raise a HelperException() with the supplied
    message, instead of a generic error (which might display the full
    call stack).  The message will be passed through str.format() with
    'string' and 'pattern' arguments, if needed
    """

    r = re.match(pattern, string)

    if r is None:
        if no_match_msg:
            raise HelperException(
                      no_match_msg.format(pattern=pattern, string=string))

        raise ValueError(
            "re_match_group() string: %s does not match pattern: %s"
                % (repr(string), repr(pattern)))

    return r.group(*groups)


helpers["re_match_group"] = re_match_group_helper



def re_match_groups_helper(pattern, string, no_match_msg=None):
    """Helper function for matching strings against regular expressions
    and extract groups (marked by parentheses) of text in a Jinja2
    template, returning them in the form of a tuple, one for each pair.

    The caller can extract the desired one by indexing the tuple.  To
    select an arbitrary list of groups (by name),
    re_match_group_helper() is more useful.

    This is a wrapper around re.match().groups() (re.match() returns a
    Match object and groups() is called on that).

    If the match fails, a ValueError() is raised, giving the pattern and
    string.  A customised error, raised using HelperException(), can be
    supplied with no_match_msg.  To avoid raising an exception, the
    string must be separately matched with re_match_helper() first.

    Keyword arguments:

    pattern -- the regular expression to match against; the required
    groups to return should be specified using parentheses

    string -- the string to match and return the groups of

    no_match_msg=None -- raise a HelperException() with the supplied
    message, instead of a generic error (which might display the full
    call stack).  The message will be passed through str.format() with
    'string' and 'pattern' arguments, if needed
    """

    r = re.match(pattern, string)

    if r is None:
        if no_match_msg:
            raise HelperException(
                     no_match_msg.format(pattern=pattern, string=string))

        raise ValueError(
            "re_match_groups() string: %s does not match pattern: %s"
                % (repr(string), repr(pattern)))

    return r.groups()


helpers["re_match_groups"] = re_match_groups_helper



def to_list_helper(s):
    """Helper function to make a list from the lines in a multiline
    string: each line is added as an item to the list.

    Blank lines (including ones consiting entirely of spaces) are
    skipped, as well as leading and trailing spaces on the remaining
    lines.

    The function is useful to get more complex data structures back
    from Jinja2 macros (which can only return text).
    """

    l = []

    for i in s.split("\n"):
        i = i.strip()
        
        # only add to the list, if the line is not blank
        if i:
            l.append(i)

    return l


helpers["to_list"] = to_list_helper



def to_set_helper(s):
    """Helper function to make a set from the lines in a multiline
    string: each line is added as an item to the list.

    Blank lines (including ones consiting entirely of spaces) are
    skipped, as well as leading and trailing spaces on the remaining
    lines.

    The function is useful to get more complex data structures back
    from Jinja2 macros (which can only return text).
    """

    t = set()

    for i in s.split("\n"):
        i = i.strip()
        
        # only add to the list, if the line is not blank
        if i:
            t.add(i)

    return t


helpers["to_set"] = to_set_helper



def to_dict_helper(s):
    """Helper function to make a dictionary from a string: the lines of
    the string are parsed in the form 'key:value' and used to populate
    a dictionary that is returned.

    Blank lines (including ones consisting entirely of spaces) are
    skipped, as well as leading and trailing spaces in the key and
    value.

    The function is useful to get more complex data structures back
    from Jinja2 macros (which can only return text).
    """

    d = {}
    
    for i in s.split("\n"):
        # skip blank lines (including ones just composed of spaces)
        if not i.strip():
            continue

        try:
            k, v = i.split(":", 1)
        except ValueError:
            raise(ValueError(
                "failed parsing 'key:value' from line: %s" % repr(i)))

        # store the key:value in the dictionary, trimming spaces
        d[k.strip()] = v.strip()

    return d


helpers["to_dict"] = to_dict_helper
