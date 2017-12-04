import math
from . import Counter

class Parser(Counter):
    name = 'coin'
    def __init__(self, data):
        super(Parser, self).__init__(data=data.upper())

    @property
    def symbols(self):
        return list('HT')
