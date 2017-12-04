import math
from . import Counter

class Parser(Counter):
    '''
        120 6-sided die rolls gives 256-bits of entropy with bias of less than 1 in 2^-64.
    '''
    name = 'dice'
    def __init__(self, data):
        super(Parser, self).__init__(data=data.upper())

    @property
    def symbols(self):
        return list('123456')
