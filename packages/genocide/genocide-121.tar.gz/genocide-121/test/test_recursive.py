# This file is placed in the Public Domain.
#
# pylint: disable=C0413,C0115,C0116,E1101
# pylama: ignore=W0611,E303,E402


"""
    >>> import genocide
    >>> o = genocide.Object()
    >>> o.o = genocide.Object()
    >>> o.o.a = "test"
    >>> print(o)
    {'o': {'a': 'test'}}

"""


import sys
import unittest


sys.path.insert(0, "..")


from genocide.objects import Object
from genocide.persist import readrec, writerec


class TestRecursive(unittest.TestCase):


    def testrecursive(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        pth = writerec(obj)
        print(pth)
        readrec(obj, pth)
        self.assertEqual(obj.obj.a, "test")
