from __future__ import absolute_import

import unittest
from pledge import pre, post, check, takes, list_of
import pledge

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

    def test_takes(self):
        @takes(int, basestring)
        def add(x, y):
            return "%s,%s" % (x, y)

        add(10, '')
        add(10, y='')
        self.assertRaises(AssertionError, lambda: add('', ''))
        self.assertRaises(AssertionError, lambda: add('', 10))
        self.assertRaises(AssertionError, lambda: add(10, 10))

        class Test(object):
            @takes(int, int)
            def add(self, x, y):
                return x + y

        t = Test()
        t.add(10, 11)
        t.add(10, y=11)
        self.assertRaises(AssertionError, lambda: t.add(10, ''))
        self.assertRaises(AssertionError, lambda: t.add(10, y=''))

    def test_list_of(self):
        @takes(list_of(int))
        def add(x):
            return x

        add([10, 11])
        self.assertRaises(AssertionError, lambda: add(set([10, 11])))
        self.assertRaises(AssertionError, lambda: add([10, '']))
        self.assertRaises(AssertionError, lambda: add(['', 10]))

    def test_defaults(self):
        @takes(int, int, int)
        def add(x, y=10, z=11):
            return x+y+z

        self.assertEqual(22, add(1))
        self.assertEqual(14, add(1, 2))
        self.assertEqual(6, add(1, 2, 3))
        self.assertEqual(14, add(1, y=2))
        self.assertEqual(13, add(1, z=2))
        self.assertRaises(AssertionError, lambda: add(''))
        self.assertRaises(AssertionError, lambda: add(10, ''))
        self.assertRaises(AssertionError, lambda: add(10, 11, ''))
        self.assertRaises(AssertionError, lambda: add(10, 11, z=''))
        self.assertRaises(AssertionError, lambda: add(10, y=''))

        @pre(lambda x: isinstance(x, int))
        def add(x=10):
            return x

        add()
        self.assertRaises(AssertionError, lambda: add(''))

    def test_kwargs_and_none(self):
        @takes(int, (int, None), (int, None))
        def add(x, y=None, z=None):
            total = x
            if y:
                total += y
            if z:
                total += z
            return total

        self.assertEqual(1, add(1))
        self.assertEqual(3, add(x=1, y=2))
        self.assertEqual(4, add(x=1, z=3))
        self.assertEqual(6, add(x=1, y=2, z=3))

    def test_disabled(self):
        pledge.enabled = False

        try:
            @takes(int, int)
            def add(x, y):
                return "%s,%s" % (x, y)

            add(10, 11)
            add('', '')
            add('', 10)
            add(10, 10)
        finally:
            pledge.enabled = True
