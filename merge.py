#!/usr/bin/env python3
'''
    Takes multiple sources of entropy and merges them together.
    Author: jonathan lung

    Takes multiple lines of input from the keyboard and spits out a configurable
    number of bits of entropy. Keyboard input is used to avoid persistent storage.
'''
from entropy.sources import parsers, reduce_space, ParseError
import sys
import argparse

def decode_line(line, base):
    '''Auto-detect and decode the contents of the line using one of the entropy
    source parsers.'''

    # Try every parser to see which ones can decode the line.
    interpretations = []
    for parser in parsers:
        try:
            interpretations.append(parser(line))
        except ParseError:
            pass

    # Ensure interpretation exists and is unique; select the interpretation
    # with the smallest symbol set size.
    interpretations.sort(key=lambda x: len(x.symbols))

    if len(interpretations) == 0:
        raise ValueError("No interpretations.")

    if len(interpretations) > 1 and \
        len(interpretations[0].symbols) == len(interpretations[1].symbols):
        raise ValueError("Ambiguous line.")


    interpretation = interpretations[0]
    src_entropy = interpretation.random_symbols(base)
    print(len(src_entropy),'symbols of entropy from', interpretation.name)
    # Return the interpretation.
    return src_entropy

if __name__ == '__main__':
    # Parse command line options.
    parser = argparse.ArgumentParser(description='Merge entropy from multiple sources.')
    parser.add_argument('-H', '--entropy', metavar='H', type=int, nargs=1,
                    default=[256],
                    help='Symbols of entropy to produce.')
    parser.add_argument('-b', '--base', metavar='b', type=int, nargs=1,
                    default=[2],
                    help='Base of entropy.')
    parser.add_argument(metavar='filename', type=str, nargs='?', dest='filename',
                    help='Filename with entropy, one line per entropy source. Defaults to stdin.')
    args = parser.parse_args(sys.argv[1:])

    # Open selected entropy source file.
    if args.filename:
        entropy_source = open(args.filename, 'r')
    else:
        entropy_source = sys.stdin

    symbols = []
    for line in entropy_source.read().strip().split('\n'):
        symbols.extend(decode_line(line.strip(), args.base[0]))

    entropy_source.close()

    print('Available entropy:', len(symbols))
    entropy = reduce_space(args.base[0], symbols, args.entropy[0])
    print('Random sequence:\n', entropy)