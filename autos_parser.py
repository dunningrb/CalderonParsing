"""
autos_parser

Rodney Dunning

Parses a single auto sacrementales in text format.

"""

from string import digits
from itertools import islice
import collections

print('*** Starting. ***')

LINES = {}
REMOVE_DIGITS = str.maketrans('', '', digits)
PAGE_HEADER_SKIP_LINES = 4
PAGE_HEADER_TOKENS = ['EL JARDÍN DE FALERINA', 'CALDERÓN DE LA BARCA']
HTML_LINK_TOKENS = ['ANTERIOR', 'INICIO']

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        next(islice(iterator, n, n+1), None)

print('Opening the file for reading.')

with open('./el-jardin.txt', 'r') as f:
    line_number = 0
    for line in f.readlines():
        line_number += 1
        LINES[line_number] = {'keep': True, 'text': line}

print('Finished reading the file into the lines dictionary.')

print('Flagging page header lines in the dictionary.')

lines_iterator = iter(LINES.items())
for line_number, line_data in lines_iterator:
    if any(token in line_data['text'] for token in PAGE_HEADER_TOKENS):
        for i in range(PAGE_HEADER_SKIP_LINES):
            LINES[line_number+i]['keep'] = False

        consume(lines_iterator, PAGE_HEADER_SKIP_LINES)

    if any(token in line_data['text'].upper() for token in HTML_LINK_TOKENS):
        LINES[line_number]['keep'] = False

print(f'Finished flagging page header lines in the dictionary.')

print('Writing all lines not flagged into the output file.')

with open('./el-jardin-output-yes-consume-5.txt', 'w') as f:
    for line_number, line_data in LINES.items():
        if line_data['keep']:
            f.write(line_data['text'].translate(REMOVE_DIGITS))

print('Finished writing un-flagged lines to the output file.')

print('*** Finished. ****')
