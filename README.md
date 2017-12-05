# Entropy merger
Merge entropy from various sources such as shuffled decks of cards and coin flipping.

## Requirements
 * Python 3

## Example usage
Flip some coins, roll some dice, and/or shuffle a deck of cards, entering the data into a textfile, one data-source per line. The same type of entropy source can be used more than once.

    HTHHTHTHT
    152632134
    AD JS 5C TC 3H
    HTTTHT
    00101010010010

For cryptographic purposes, this file should never be saved to a non-volatile storage device (including hard drives, solid state drives, and USB keys) unless precautions have been taken against adversaries recovering the data. Alternately, the results of the entropy can be entered directly on the console for `merger.py`.

Next step is to run the entropy merger program, `merger.py`.

    $ ./merge.py -H 256            # Generate 256 random bits using input from console (stdin).
    $ ./merge.py -H 6 -b 10        # Generate 6-digit PIN.
    $ ./merge.py -H 64 entropy.txt # Generate 64 random bits using input entropy.txt.

The program will quit with errors if the input is not valid or insufficient entropy is provided for the task.