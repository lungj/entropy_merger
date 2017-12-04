import math
from . import Counter

class Parser(Counter):
    name = 'binary'
    def __init__(self, data):
        super(Parser, self).__init__(data=data.upper())

    @property
    def symbols(self):
        return list('01')