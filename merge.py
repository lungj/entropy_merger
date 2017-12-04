#!/usr/bin/env python3
'''
    Takes multiple sources of entropy and merges them together.
    Author: jonathan lung

    Takes multiple lines of input from the keyboard and spits out a configurable
    number of bits of entropy. Keyboard input is used to avoid persistent storage.
'''
from entropy.sources import parsers, reduce_space
import sys
import argparse

def decode_line(line):
    '''Auto-detect and decode the contents of the line using one of the entropy
    source parsers.'''

    # Try every parser to see which ones can decode the line.
    interpretations = []
    for parser in parsers:
        try:
            p = parser(line)
            src_entropy = p.binary()
            interpretations.append(src_entropy)
            print(len(src_entropy),'bits of entropy from', p.name)
        except ValueError:
            pass

    # Ensure interpretation exists and is unique.
    if len(interpretations) > 1:
        raise ValueError("Ambiguous line.")
    elif len(interpretations) == 0:
        raise ValueError("No interpretations.")

    # Return the interpretation.
    return interpretations[0]

if __name__ == '__main__':
    # Parse command line options.
    parser = argparse.ArgumentParser(description='Merge entropy from multiple sources.')
    parser.add_argument('-H', '--entropy', metavar='H', type=int, nargs=1,
                    default=[256],
                    help='Bits of entropy to produce')

    args = parser.parse_args(sys.argv[1:])

    bits = []
    for line in sys.stdin.read().strip().split('\n'):
        bits.extend(decode_line(line.strip()))

    print('Available entropy: ', len(bits))
    entropy = reduce_space(bits, args.entropy[0])
    print(entropy)