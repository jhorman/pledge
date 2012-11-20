pledge
============

Simple decorator based design by contract (DBC) for Python. Loosley based
on the open source [decontractors](https://github.com/thp/python-decontractors).
Some ideas are also lifted from [Method signature checking decorators](http://code.activestate.com/recipes/426123-method-signature-checking-decorators/).

There are a number of open source projects that embed DBC contracts in pydoc,
or in decorators but with an alternate eval'd syntax. pledge describes contracts
using simple lambda expressions. The advantage is that the expressions are
validated by the python interpreter, editors syntax highlight properly, and
the implementation is very simple.

The other important thing that pledge does is enforce superclass contracts,
but you do have to at least add the @check decorator to "pledged" methods.

### Usage

    @pre(lambda x, y: isinstance(x, int) and isinstance(y, int))
    @post(lambda rt: rt > 0)
    def add(x, y):
        return x + y

Shorthand for type checking.

    @takes(int, int)
    @returns(int)
    def add(x, y):
        return x+y
        
    @takes(list_of(int))
    def add(x):
        return x

    @takes(int, (int, None), (int, None))
    def add(x, y=None, z=None):
        total = x
        if y:
            total += y
        if z:
            total += z
        return total

Your expressions don't need to accept all of the wrapped methods parameters.
The library figures out which parameters to pass to the lambda.

    @pre(lambda x: isinstance(x, int))
    def add(x, y):
        return x + y

You can nest any number of @pre and @post conditions.

    @pre(lambda x: isinstance(x, int))
    @pre(lambda y: isinstance(x, int))
    @post(lambda rt: rt > 0)
    def add(x, y):
        return x + y

Contracts on member class methods are executable in subclasses via the
@check decorator.

    class Adder(object):
        @pre(lambda x, y: isinstance(x, int) and x > 0 and isinstance(y, int))
        @post(lambda rt: rt > 0)
        def add(self, x, y):
            return x + y

    class SubAdder(Adder):
        @check
        def add(self, x, y):
            return x + y + y

### Tests

    python setup.py test

### Enable/Disable checks

To turn off all checks set

    pledge.enabled=False

The default value of pledge.enabled is

    enabled = not sys.flags.optimize

So running python with -O will also disable checks.