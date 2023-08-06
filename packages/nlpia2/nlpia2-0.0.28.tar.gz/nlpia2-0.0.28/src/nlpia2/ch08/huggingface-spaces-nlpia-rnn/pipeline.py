# pipeline.py
from pathlib import Path
# import random
# import time
import string

import torch
import torch.nn as nn
import unicodedata
from unidecode import unidecode

from persistence import load_model


ASCII_LETTERS = string.ascii_letters
ASCII_PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
ASCII_PRINTABLE_COMMON = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r'

ASCII_VERTICAL_TAB = '\x0b'
ASCII_PAGE_BREAK = '\x0c'
ASCII_ALL = ''.join(chr(i) for i in range(0, 128))  # ASCII_PRINTABLE
ASCII_DIGITS = string.digits
ASCII_IMPORTANT_PUNCTUATION = " .?!,;'-=+)(:"
ASCII_NAME_PUNCTUATION = " .,;'-"
ASCII_NAME_CHARS = set(ASCII_LETTERS + ASCII_NAME_PUNCTUATION)
ASCII_IMPORTANT_CHARS = set(ASCII_LETTERS + ASCII_IMPORTANT_PUNCTUATION)

CURLY_SINGLE_QUOTES = '‘’`´'
STRAIGHT_SINGLE_QUOTES = "'" * len(CURLY_SINGLE_QUOTES)
CURLY_DOUBLE_QUOTES = '“”'
STRAIGHT_DOUBLE_QUOTES = '"' * len(CURLY_DOUBLE_QUOTES)


META = load_model('rnn_from_scratch_name_nationality')
CHAR2I = META['char2i']
all_categories = META['all_categories']


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, char_tens, hidden):
        combined = torch.cat((char_tens, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)


n_hidden = 128
rnn = RNN(len(ASCII_NAME_CHARS), n_hidden, len(all_categories))
rnn.load_state_dict(META['state_dict'])


def normalize_newlines(s):
    s = s.replace(ASCII_VERTICAL_TAB, '\n')
    s = s.replace(ASCII_PAGE_BREAK, '\n\n')


class Asciifier:
    """ Construct a function that filters out all non-ascii unicode characters

    >>> test_str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
    >>> Asciifier(include='a b c 123XYZ')(test_str):
    '123abcXYZ '
    """

    def __init__(
            self,
            min_ord=1, max_ord=128,
            exclude=None,
            include=ASCII_PRINTABLE,
            exclude_category='Mn',
            normalize_quotes=True,
    ):
        self.include = set(sorted(include or ASCII_PRINTABLE))
        self._include = ''.join(sorted(self.include))
        self.exclude = exclude or set()
        self.exclude = set(sorted(exclude or []))
        self._exclude = ''.join(self.exclude)
        self.min_ord, self.max_ord = int(min_ord), int(max_ord or 128)
        self.normalize_quotes = normalize_quotes

        if self.min_ord:
            self.include = set(c for c in self.include if ord(c) >= self.min_ord)
        if self.max_ord:
            self.include = set(c for c in self._include if ord(c) <= self.max_ord)
        if exclude_category:
            self.include = set(
                c for c in self._include if unicodedata.category(c) != exclude_category)

        self.vocab = sorted(self.include - self.exclude)
        self._vocab = ''.join(self.vocab)
        self.char2i = CHAR2I

        self._translate_from = self._vocab
        self._translate_to = self._translate_from

        # FIXME: self.normalize_quotes is accomplished by unidecode.unidecode!!
        # ’->'  ‘->'  “->"  ”->"
        if self.normalize_quotes:
            trans_table = str.maketrans(
                CURLY_SINGLE_QUOTES + CURLY_DOUBLE_QUOTES,
                STRAIGHT_SINGLE_QUOTES + STRAIGHT_DOUBLE_QUOTES)
            self._translate_to = self._translate_to.translate(trans_table)
            # print(self._translate_to)

        # eliminate any non-translations (if from == to)
        self._translate_from_filtered = ''
        self._translate_to_filtered = ''

        for c1, c2 in zip(self._translate_from, self._translate_to):
            if c1 == c2:
                continue
            else:
                self._translate_from_filtered += c1
                self._translate_to_filtered += c2

        self._translate_del = ''
        for c in ASCII_ALL:
            if c not in self.vocab:
                self._translate_del += c

        self._translate_from = self._translate_from_filtered
        self._translate_to = self._translate_to_filtered
        self.translation_table = str.maketrans(
            self._translate_from,
            self._translate_to,
            self._translate_del)

    def __call__(self, text):
        return unidecode(unicodedata.normalize('NFD', text)).translate(self.translation_table)


name_char_vocab_size = len(ASCII_NAME_CHARS) + 1  # Plus EOS marker

# Transcode Unicode str ASCII without embelishments, diacritics (https://stackoverflow.com/a/518232/2809427)
asciify = Asciifier(include=ASCII_NAME_CHARS)


def find_files(path, pattern):
    return Path(path).glob(pattern)


# all_letters = ''.join(set(ASCII_NAME_CHARS).union(set(" .,;'")))
char2i = {c: i for i, c in enumerate(ASCII_NAME_CHARS)}

# !curl -O https://download.pytorch.org/tutorial/data.zip; unzip data.zip

print(f'asciify("O’Néàl") => {asciify("O’Néàl")}')


######################################################################
# Turning Names into Tensors
# --------------------------
#
# Now that we have all the names organized, we need to turn them into
# Tensors to make any use of them.
#
# To represent a single letter, we use a "one-hot vector" of size
# ``<1 x n_letters>``. A one-hot vector is filled with 0s except for a 1
# at index of the current letter, e.g. ``"b" = <0 1 0 0 0 ...>``.
#
# To make a word we join a bunch of those into a 2D matrix
# ``<line_length x 1 x n_letters>``.
#
# That extra 1 dimension is because PyTorch assumes everything is in
# batches - we're just using a batch size of 1 here.
#

# Find letter index from all_letters, e.g. "a" = 0


def letterToIndex(c):
    return char2i[c]

# Just for demonstration, turn a letter into a <1 x n_letters> Tensor


def encode_one_hot_vec(letter):
    tensor = torch.zeros(1, len(ASCII_NAME_CHARS))
    tensor[0][CHAR2I[letter]] = 1
    return tensor

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors


def encode_one_hot_seq(line):
    tensor = torch.zeros(len(line), 1, len(ASCII_NAME_CHARS))
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


input = encode_one_hot_vec('A')
hidden = torch.zeros(1, n_hidden)

output, next_hidden = rnn(input, hidden)


def categoryFromOutput(output):
    global all_categories
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return all_categories[category_i], category_i


def output_from_str(s):
    global rnn

    input = encode_one_hot_seq(s)
    hidden = torch.zeros(1, n_hidden)

    output, next_hidden = rnn(input[0], hidden)
    print(output)

    return categoryFromOutput(output)


########################################
# load/save test for use on the huggingface spaces server
# torch.save(rnn.state_dict(), 'rnn_from_scratch_name_nationality.state_dict.pickle')

state_dict = torch.load('rnn_from_scratch_name_nationality.state_dict.pickle')
rnn.load_state_dict(state_dict)


def predict_tensor(line_tensor):
    global rnn
    hidden = rnn.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    return output


def predict_nationality(input_line, n_predictions=3):
    global all_categories
    print('\n> %s' % input_line)
    with torch.no_grad():
        output = predict_tensor(encode_one_hot_seq(input_line))

        # Get top N categories
        topv, topi = output.topk(n_predictions, 1, True)
        predictions = []

        for i in range(n_predictions):
            value = topv[0][i].item()
            category_index = topi[0][i].item()
            print('(%.2f) %s' % (value, all_categories[category_index]))
            predictions.append([value, all_categories[category_index]])


predict_nationality('Dovesky')
predict_nationality('Jackson')
predict_nationality('Satoshi')

# load/save test for use on the huggingface spaces server
########################################
