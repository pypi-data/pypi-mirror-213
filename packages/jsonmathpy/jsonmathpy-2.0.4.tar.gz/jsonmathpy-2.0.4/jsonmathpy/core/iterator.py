from locale import currency
from more_itertools import peekable
from jsonmathpy.interfaces.iterator import IIterator

class Iterator(IIterator):

    def __init__(self, object):
        self.object = object
        try:
            if isinstance(self.object, str):
                self.iterable_object = peekable(object + ' ') # ' ' only applies to lexer => this class should not care about that.
            self.iterable_object = peekable(object)
        except TypeError:
            raise TypeError(f"Trying to iterate a non iterable object: {object}")

    def advance(self):
        try:
            self.current_item = next(self.iterable_object)
        except StopIteration:
            self.current_item = None

    def peek(self):
        return self.iterable_object.peek(' ')

    def __len__(self):
        return len(self.object)

    def current(self):

        return self.current_item