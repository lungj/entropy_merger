import math

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