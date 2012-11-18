from __future__ import absolute_import

import unittest
from contracts import pre, post, check

class ContractsTestCase(unittest.TestCase):
    def test_precondition(self):
        @pre(lambda x, y: x > 0 and y > 0)
        def add(x, y):
            return x + y

        add(10, 10)
        add(x=10, y=10)
        add(10, y=10)

        self.assertRaises(AssertionError, lambda: add(-1, 10))
        self.assertRaises(AssertionError, lambda: add(-1, y=10))
        self.assertRaises(AssertionError, lambda: add(x=-1, y=10))

        @pre(lambda x: x > 0)
        def add(x, y):
            return x + y

        add(10, 10)
        add(x=10, y=10)
        add(10, y=10)
        self.assertRaises(AssertionError, lambda: add(-1, 10))

    def test_postcondition(self):
        @post(lambda rt: rt > 0)
        def add(x, y):
            return x + y

        add(10, 10)
        self.assertRaises(AssertionError, lambda: add(10, -10))

    def test_combined(self):
        @pre(lambda x, y: isinstance(x, int) and isinstance(y, int))
        @post(lambda rt: rt > 0)
        def add(x, y):
            return x + y

        add(10, 10)
        self.assertRaises(AssertionError, lambda: add(10, -10))
        self.assertRaises(AssertionError, lambda: add('', -10))

    def test_combined_on_class(self):
        class Test(object):
            @pre(lambda x, y: isinstance(x, int) and x > 0 and isinstance(y, int))
            @post(lambda rt: rt > 0)
            def add(self, x, y):
                return x + y

        t = Test()
        t.add(10, 10)
        self.assertRaises(AssertionError, lambda: t.add(10, -10))
        self.assertRaises(AssertionError, lambda: t.add('', -10))

        class SubTest(Test):
            @pre(lambda x: x > 5)
            def add(self, x, y):
                return x + y

        t = SubTest()
        t.add(10, 10)
        self.assertRaises(AssertionError, lambda: t.add(1, 10))
        self.assertRaises(AssertionError, lambda: t.add(10, -10))
        self.assertRaises(AssertionError, lambda: t.add('', -10))
        self.assertRaises(AssertionError, lambda: t.add(10, ''))

        class Sub2Test(SubTest):
            @check
            def add(self, x, y):
                return x + y

        t = Sub2Test()
        t.add(10, 10)
        self.assertRaises(AssertionError, lambda: t.add(1, 10))
        self.assertRaises(AssertionError, lambda: t.add(10, -10))
        self.assertRaises(AssertionError, lambda: t.add('', -10))
        self.assertRaises(AssertionError, lambda: t.add(10, ''))

class FakeClass(object):
    def get_number(self):
        return 10

