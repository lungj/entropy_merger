from os.path import dirname, basename, isfile
import pkgutil
import glob
import math

def __get_modules():
    '''Return all modules in this package.'''
    modules = glob.glob(dirname(__file__) + '/*.py')
    return [basename(filename)[:-3] for filename in modules if isfile(filename) and not filename.endswith('/__init__.py')]

def reduce_space(input_list, length):
    '''Reduce a list of bits to a list of length 'length.'
    '''
    if len(input_list) < length:
        raise ValueError("Insufficient entropy.")

    output = [0] * length
    for (idx, bit) in enumerate(input_list):
        output[idx % length] ^= bit

    return output

def get_usable_bits(space, bias):
    '''Return the number of usable bits with <= bias amount of bias for
       a search space of size 'space'.
    '''

    usable_bits = 0         # Number of bits of entropy we have at the end, accounting
                            # for losses due to bias.

    while True:
        ratio = space / (2 ** (usable_bits + 1))
        if ratio < 1 or (math.ceil(ratio) / math.floor(ratio) - 1) > bias:
            return usable_bits

        usable_bits = usable_bits + 1


class Counter(object):
    '''A class that counts permutations/combinations.'''
    def __init__(self, data=None, epsilon=(2** -64)):
        '''epsilon is the percent more that combinations with lower enumerations appear
           than their higher enumeration siblings. Essentially, an amount of bias. Smaller
           epsilons require more input data to generate the same amount of entropy for
           non-power-of-two symbol sizes.'''

        # If all of the symbols are 1-character long, make spaces optional.
        if [s for s in self.symbols if len(s) != 1]:
            data = data.split(' ')
        else:
            data = list(data.replace(' ', ''))

        # If the set to be counted has replacements, ensure the entire symbol space is
        # used.
        if self.with_replacement:
            if set(data) != set(self.symbols):
                raise ValueError('Not valid for this symbol set')

        # If set to be counted has no replacements, ensure symbol set is valid and
        # no duplicates exist.
        # Currently no support where duplicate symbols can appear in the symbol set.
        if not self.with_replacement:
            if not set(self.symbols).issuperset(set(data)) or len(data) != len(set(data)):
                raise ValueError('Not valid for this symbol set')

        self._data = data
        self._epsilon = epsilon

    @property
    def with_replacement(self):
        return True

    def binary(self):
        '''
            This implementation maps combinatorial counts to binary outputs. Suppose a
            single 6-sided die roll is being mapped to a 2-bit value (number from 0 to 4):

                2-bit   |   Die rolls
                --------+--------------
                0       |   1, 5
                1       |   2, 6
                2       |   3
                3       |   4

            Bias here is 100% (the most value appears 100% more than the least-
            common).

            In a two-die-roll situation, the event count of a 6-sided die is 36.

                2-bit   |   Die rolls
                --------+--------------
                0       |   1, 5, ..., 33
                1       |   2, 6, ..., 34
                2       |   3, 7, ..., 35
                3       |   4, 8, ..., 36


            More generally, this function maps a b^c bit value to d 1-bit numbers (2^d
            values). If n = b^c and m = 2^d, bias is ⌈n/m⌉ / ⌊n/m⌋ - 1. Note that bias
            can be driven arbitrarily close to zero. This function constrains bias to be
            less than epsilon.
        '''

        event_space_size = 1    # Count the event space.
        count = 0               # Enumeration of the witnessed event.
        symbols = self.symbols[:]

        for symbol in self._data:
            event_space_size *= len(symbols)
            count = count * len(symbols) + symbols.index(symbol)

            # Update remaining symbol space if counting a no-replacement set.
            if not self.with_replacement:
                symbols.remove(symbol)

        usable_bits = get_usable_bits(event_space_size, self._epsilon)

        # Map the enumerated permutation or combination to binary bits.
        binary = []
        while event_space_size >= 2:
            binary.append(count % 2)
            count //= 2
            event_space_size /= 2

        return reduce_space(binary, usable_bits)

__all__ = __get_modules()

parsers = []
for importer, modname, ispkg in pkgutil.iter_modules(__path__, 'entropy.sources.'):
    parsers.append(__import__(modname, fromlist="dummy").Parser)
