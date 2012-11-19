from __future__ import absolute_import

"""
 Lambda based design by contract. Use preconditions and postconditions
 to veryify the input and output of methods. Preconditions are fired
 before method execution and inspect parameters, postconditions are
 fired after execution and inspect the return value.

 Conditions can be inherited. Any pre/post conditions on a base class
 super method will be run as long as the sub class method is annotated
 with @pre/@post or @check.
"""

__author__ = 'Jason Horman <jhorman@gmail.com>'
__version__ = '1.0'
__website__ = 'https://github.com/jhorman/pledge_py'
__license__ = 'Modified BSD License'

from functools import wraps
import inspect

def pre(cond):
    """
     Add a precondition check to the annotated method. The condition
     is passed the arguments from the annotated method. It does not
     need to accept all of the methods parameters. The condition
     is inspected to figure out which parameters to pass.
    """
    cond_args, cond_varargs, cond_varkw, cond_defaults = inspect.getargspec(cond)
    source = inspect.getsource(cond).strip()

    def inner(f):
        # deal with the real function, not a wrapper
        f = getattr(f, 'wrapped_fn', f)

        # need to check if 'self' is the first arg, 
        # since @pre doesn't want the self param
        member_function = is_member_function(f)

        def check_condition(args, kwargs):
            cond_kwargs = {}

            # collection the args
            for name, value in map(None, cond_args, args[member_function:]):
                if name and value:
                    cond_kwargs[name] = value

            # collect the remaining kwargs
            for name in cond_args:
                if name not in cond_kwargs:
                    cond_kwargs[name] = kwargs.get(name)

            # test the precondition
            if not cond(**cond_kwargs):
                # otherwise raise the exception
                raise AssertionError('Precondition failure, %s' % source)

        # append to the rest of the preconditions attached to this method
        if not hasattr(f, 'preconditions'):
            f.preconditions = []
        f.preconditions.append(check_condition)

        return check(f)

    return inner

def post(cond):
    """
     Add a postcondition check to the annotated method. The condition
     is passed the return value of the annotated method.
    """
    source = inspect.getsource(cond).strip()

    def inner(f):
        # deal with the real function, not a wrapper
        f = getattr(f, 'wrapped_fn', f)

        def check_condition(result):
            if not cond(result):
                raise AssertionError('Postcondition failure, %s' % source)

        # append to the rest of the postconditions attached to this method
        if not hasattr(f, 'postconditions'):
            f.postconditions = []
        f.postconditions.append(check_condition)

        return check(f)

    return inner

def check(f):
    """
    Wraps the function with a decorator that runs all of the 
    pre/post conditions.
    """
    if hasattr(f, 'wrapped_fn'):
        return f
    else:
        @wraps(f)
        def decorated(*args, **kwargs):
            return check_conditions(f, args, kwargs)
        decorated.wrapped_fn = f
        return decorated

def check_conditions(f, args, kwargs):
    """
    This is what runs all of the conditions attached to a method,
    along with the conditions on the superclasses.
    """
    member_function = is_member_function(f)

    # check the functions direct pre conditions
    check_preconditions(f, args, kwargs)

    # for member functions check the pre conditions up the chain
    base_classes = []
    if member_function:
        base_classes = inspect.getmro(type(args[0]))[1:-1]
        for clz in base_classes:
            super_fn = getattr(clz, f.func_name, None)
            check_preconditions(super_fn, args, kwargs)

    # run the real function
    return_value = f(*args, **kwargs)

    # check the functions direct post conditions
    check_postconditions(f, return_value)

    # for member functions check the post conditions up the chain
    if member_function:
        for clz in base_classes:
            super_fn = getattr(clz, f.func_name, None)
            check_postconditions(super_fn, return_value)

    return return_value

def check_preconditions(f, args, kwargs):
    """ Runs all of the preconditions. """
    f = getattr(f, 'wrapped_fn', f)
    if f and hasattr(f, 'preconditions'):
        for cond in f.preconditions:
            cond(args, kwargs)

def check_postconditions(f, return_value):
    """ Runs all of the postconditions. """
    f = getattr(f, 'wrapped_fn', f)
    if f and hasattr(f, 'postconditions'):
        for cond in f.postconditions:
            cond(return_value)

def is_member_function(f):
    """ Checks if the first argument to the method is 'self'. """
    f_args, f_varargs, f_varkw, f_defaults = inspect.getargspec(f)
    return 1 if 'self' in f_args else 0

