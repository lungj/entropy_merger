from os.path import dirname, basename, isfile
import pkgutil
import glob
import math

class ParseError(Exception): pass

def __get_modules():
    '''Return all modules in this package.'''
    modules = glob.glob(dirname(__file__) + '/*.py')
    return [basename(filename)[:-3] for filename in modules if isfile(filename) and not filename.endswith('/__init__.py')]


def reduce_space(base, input_list, length):
    '''Reduce a list of symbols in base 'base' to a list of length 'length.'
    '''
    if len(input_list) < length or length == 0:
        raise ValueError("Insufficient entropy.")

    output = [0] * length
    for (idx, symbol) in enumerate(input_list):
        # Add the entropy. I'm pretty sure central limit theorem does not apply here.
        output[idx % length] = (output[idx % length] + symbol) % base

    return output


def get_usable_output_length(base, space, bias):
    '''Return the number of usable base 'base' symbols with <= bias amount of bias for
       a search space of size 'space'.
    '''

    usable_length = 0       # Number of symbols of entropy we have at the end, accounting
                            # for losses due to bias.

    while True:
        ratio = space / (base ** (usable_length + 1))
        if ratio < 1 or (math.ceil(ratio) / math.floor(ratio) - 1) > bias:
            return usable_length

        usable_length = usable_length + 1


class Counter(object):
    '''A class that counts permutations/combinations.'''
    _case_sensitive = False             # If not case sensitive, everything will be
                                        # treated as uppercase.

    def __init__(self, data=None, epsilon=(2** -64)):
        '''epsilon is the percent more that combinations with lower enumerations appear
           than their higher enumeration siblings. Essentially, an amount of bias. Smaller
           epsilons require more input data to generate the same amount of entropy for
           non-power-of-two symbol sizes.'''

        if not self._case_sensitive:
            data = data.upper()

        # If all of the symbols are the same length, make spaces optional.
        if [s for s in self.symbols if len(s) != len(self.symbols[0])]:
            data = data.split(' ')
        else:
            data = data.replace(' ', '')
            symbol_len = len(self.symbols[0])
            # Group the data into symbol_len-sized chunks
            data = [data[i:i + symbol_len] for i in range(0, len(data), symbol_len)]

        # If the set to be counted has replacements, ensure the entire symbol space is
        # used.
        if self.with_replacement:
            if set(data) != set(self.symbols):
                raise ParseError('Not valid for this symbol set')

        # If set to be counted has no replacements, ensure symbol set is valid and
        # no duplicates exist.
        # Currently no support where duplicate symbols can appear in the symbol set.
        if not self.with_replacement:
            if not set(self.symbols).issuperset(set(data)) or len(data) != len(set(data)):
                raise ParseError('Not valid for this symbol set')

        self._data = data
        self._epsilon = epsilon

    @property
    def with_replacement(self):
        return True

    def random_symbols(self, base):
        '''
            Maps combinatorial counts to n-ary outputs in base 'base'.

            Suppose a single 6-sided die roll is being mapped to a 2-bit value
            (a number from 0 to 4):

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


            More generally, this function maps a b^c bit value to d 1-base-ary numbers
            (base^d values). If n = b^c and m = base^d, bias is ⌈n/m⌉ / ⌊n/m⌋ - 1.
            Note that bias can be driven arbitrarily close to zero. This function
            constrains bias to be less than epsilon.
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

        output_len = get_usable_output_length(base, event_space_size, self._epsilon)

        # Map the enumerated permutation or combination to base-ary bits.
        output = []
        while event_space_size >= base:
            output.append(count % base)
            count //= base
            event_space_size /= base

        return reduce_space(base, output, output_len)


__all__ = __get_modules()

parsers = []
for importer, modname, ispkg in pkgutil.iter_modules(__path__, 'entropy.sources.'):
    parsers.append(__import__(modname, fromlist="dummy").Parser)
