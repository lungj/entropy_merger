from . import Counter

class Parser(Counter):
    '''
    Number of cards | Entropy (bits) with bias <= 1/(2^64)
    ----------------+------------------------------------
         1          | 3
         7          | 7
        14          | 35
        21          | 64
        34          | 126
        53          | 196
    '''
    name = 'cards'
    with_replacement = False

    @property
    def symbols(self):
        '''Generate a list of all cards in a deck.'''

        deck = []
        for suit in 'CDHS':
            for value in '123456789TJQKA':
                deck.append(value + suit)
        return deck

    def gen_table(self):
        '''Generate a table of number of cards to entropy bits.

        >>> Parser('').gen_table()
        '''

        deck = Parser('').symbols
        print('Number of cards | Entropy (bits) with bias <= 1/(2^64)')
        print('----------------+------------------------------------')

        for i in range(len(deck) + 1):
            print(str(i).rjust(15), '|', len(Parser(' '.join(deck[:i])).binary()))