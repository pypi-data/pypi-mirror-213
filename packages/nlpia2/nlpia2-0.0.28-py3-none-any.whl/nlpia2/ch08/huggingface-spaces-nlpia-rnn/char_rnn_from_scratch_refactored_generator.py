# -*- coding: utf-8 -*-
"""

    $ python predict.py Hinton
    (-0.47) Scottish
    (-1.52) English
    (-3.57) Irish

    $ python predict.py Schmidhuber
    (-0.19) German
    (-2.48) Czech
    (-2.68) Dutch
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from pathlib import Path
import random
import time
import torch
import torch.nn as nn

import pandas as pd

from nlpia2.init import SRC_DATA_DIR, maybe_download
from nlpia2.string_normalizers import Asciifier, ASCII_NAME_CHARS

from persistence import preserve_model, load_model


name_char_vocab_size = len(ASCII_NAME_CHARS) + 1  # +1 for EOS marker

# Transcode Unicode str ASCII without embelishments, diacritics (https://stackoverflow.com/a/518232/2809427)
asciify = Asciifier(include=ASCII_NAME_CHARS)


def find_files(path, pattern):
    return Path(path).glob(pattern)


# all_letters = ''.join(set(ASCII_NAME_CHARS).union(set(" .,;'")))
META = load_model('rnn_from_scratch_name_nationality')
CHAR2I = META['char2i']
I2CHAR = [''] * len(CHAR2I)
for c in CHAR2I:
    I2CHAR[CHAR2I[c]] = c

# all_categories = META['all_categories']
# more src/nlpia2/all_categories.json 
# {"all_categories": ["Arabic", "Irish", "Spanish", "French", "German", "English", "Korean", "Vietnamese", "Scottish", "Japanese", "Polish", "Greek", "Czech", "Italian", "Por
# tuguese", "Russian", "Dutch", "Chinese"], "char2i": {"g": 0, "J": 1, "j": 2, "l": 3, "X": 4, "e": 5, "L": 6, "H": 7, " ": 8, "'": 9, "w": 10, "O": 11, "U": 12, "E": 13, "c"
# : 14, "F": 15, "a": 16, "Q": 17, "y": 18, "u": 19, "I": 20, "W": 21, ",": 22, "p": 23, "b": 24, "z": 25, "G": 26, "T": 27, "t": 28, "q": 29, "S": 30, "m": 31, "d": 32, "K":
#  33, "n": 34, "i": 35, "x": 36, "Y": 37, "M": 38, "R": 39, "r": 40, "N": 41, "-": 42, "f": 43, "Z": 44, "s": 45, "D": 46, "P": 47, "o": 48, ";": 49, "v": 50, "k": 51, "V": 
# 52, "h": 53, "C": 54, "A": 55, ".": 56, "B": 57}}

# !curl -O https://download.pytorch.org/tutorial/data.zip; unzip data.zip

print(f'asciify("O’Néàl") => {asciify("O’Néàl")}')

# Build the category_lines dictionary, a list of names per language
category_lines = {}
labeled_lines = []
categories = []
for filepath in find_files(SRC_DATA_DIR / 'names', '*.txt'):
    filename = Path(filepath).name
    filepath = maybe_download(filename=Path('names') / filename)
    with filepath.open() as fin:
        lines = [asciify(line.rstrip()) for line in fin]
    category = Path(filename).with_suffix('')
    categories.append(category)
    labeled_lines += list(zip(lines, [category] * len(lines)))

n_categories = len(categories)
all_categories = categories

df = pd.DataFrame(labeled_lines, columns=('name', 'category'))


def readLines(filename):
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    return [asciify(line) for line in lines]


def build_category_line_dict():
    global all_categories
    for filename in find_files(path='data/names', pattern='*.txt'):
        category = os.path.splitext(os.path.basename(filename))[0]
        if category not in all_categories:
            all_categories += [category]
        lines = readLines(filename)
        category_lines[category] = lines
    return category_lines


category_lines = build_category_line_dict()
print(category_lines)
print(all_categories)

n_categories = len(all_categories)


######################################################################
# Now we have ``category_lines``, a dictionary mapping each category
# (language) to a list of lines (names). We also kept track of
# ``all_categories`` (just a list of languages) and ``n_categories`` for
# later reference.
#

print(category_lines['Italian'][:5])


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

# Just for demonstration, turn a letter into a <1 x n_letters> Tensor


def encode_one_hot_vec(letter):
    global CHAR2I
    tensor = torch.zeros(1, len(CHAR2I))
    tensor[0][CHAR2I[letter]] = 1
    return tensor

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors


def encode_one_hot_seq(line):
    global CHAR2I
    tensor = torch.zeros(len(line), 1, len(ASCII_NAME_CHARS))
    for li, letter in enumerate(line):
        tensor[li][0][CHAR2I[letter]] = 1
    return tensor


print(encode_one_hot_vec('A'))

print(encode_one_hot_seq('Abe').size())


######################################################################
# Creating the Network
# ====================
#
# Before autograd, creating a recurrent neural network in Torch involved
# cloning the parameters of a layer over several timesteps. The layers
# held hidden state and gradients which are now entirely handled by the
# graph itself. This means you can implement a RNN in a very "pure" way,
# as regular feed-forward layers.
#
# This RNN module (mostly copied from `the PyTorch for Torch users
# tutorial <https://pytorch.org/tutorials/beginner/former_torchies/
# nn_tutorial.html#example-2-recurrent-net>`__)
# is just 2 linear layers which operate on an input and hidden state, with
# a LogSoftmax layer after the output.
#
# .. figure:: https://i.imgur.com/Z2xbySO.png
#    :alt:
#
#


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.hidden = self.init_hidden()

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, char_tens, hidden=None):
        self.hidden = self.init_hidden() if hidden is None else hidden
        combined = torch.cat((char_tens, self.hidden), 1)
        self.hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, self.hidden

    def init_hidden(self):
        self.hidden = torch.zeros(1, self.hidden_size)
        return self.hidden

    def output_from_line_tensor(self, line_tensor):
        hidden = self.init_hidden()
        for i in range(line_tensor.size()[0]):
            output, hidden = self(line_tensor[i], hidden)
        return output

    def output_from_str(self, s):
        input_tens = encode_one_hot_seq(s)
        hidden = torch.zeros(1, self.hidden_size)
        output, next_hidden = self(input_tens[0], hidden)
        return category_from_output(output)


rnn = RNN(input_size=len(ASCII_NAME_CHARS), hidden_size=128, output_size=n_categories)


######################################################################
# To run a step of this network we need to pass an input (in our case, the
# Tensor for the current letter) and a previous hidden state (which we
# initialize as zeros at first). We'll get back the output (probability of
# each language) and a next hidden state (which we keep for the next
# step).
#

input_tens = encode_one_hot_vec('A')
hidden = torch.zeros(1, rnn.hidden_size)

output, next_hidden = rnn(input_tens, hidden)

print(output, next_hidden)


######################################################################
# For the sake of efficiency we don't want to be creating a new Tensor for
# every step, so we will use ``encode_one_hot_seq`` instead of
# ``one_hot_encode`` and use slices. This could be further optimized by
# pre-computing batches of Tensors.
#

def category_from_output(output):
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return all_categories[category_i], category_i


def last_char_from_output(output):
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return I2CHAR[category_i], category_i


######################################################################
# As you can see the output is a ``<1 x n_categories>`` Tensor, where
# every item is the likelihood of that category (higher is more likely).
#


print(category_from_output(output))
print(last_char_from_output(output))


######################################################################
# We will also want a quick way to get a training example (a name and its
# language):
#

def random_training_example_category():
    """ Extract random training examples from dataset
    returns:
        - category (int)
        - name or line (str)
        - one-hot-encoded category
        - 2d tensor of one-hot-encoded chars (name)
    """
    category = random.choice(all_categories)
    line = random.choice(category_lines[category])
    category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
    line_tensor = encode_one_hot_seq(line)
    return dict(category=category, line=line, category_tensor=category_tensor, line_tensor=line_tensor)


def random_training_example_char():
    """ Extract random training examples from dataset
    returns:
        - last_char (str)
        - one-hot-encoded char
        - 2d tensor of one-hot-encoded chars (name)
    """
    retval = {}
    category = random.choice(all_categories)
    line = random.choice(category_lines[category])
    retval['last_char'] = line[-1]
    retval['line'] = line[:-1]
    retval['last_char_tensor'] = encode_one_hot_seq(retval['last_char'])
    retval['line_tensor'] = encode_one_hot_seq(line)
    return retval


def preview_dataset():
    for i in range(10):
        samp = random_training_example_category()
        print(f'category: {samp["category"]} | line: {samp["line"]}')


######################################################################
# Training the Network
# --------------------
#
# Now all it takes to train this network is show it a bunch of examples,
# have it make guesses, and tell it if it's wrong.
#
# For the loss function ``nn.NLLLoss`` is appropriate, since the last
# layer of the RNN is ``nn.LogSoftmax``.
#

criterion = nn.NLLLoss()


######################################################################
# Each loop of training will:
#
# -  Create input and target tensors
# -  Create a zeroed initial hidden state
# -  Read each letter in and
#
#    -  Keep hidden state for next letter
#
# -  Compare final output to target
# -  Back-propagate
# -  Return the output and loss
#

learning_rate = 0.005  # If you set this too high, it might explode. If too low, it might not learn


def train(rnn, true_category_tensor, line_tensor):
    hidden = rnn.init_hidden()

    rnn.zero_grad()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    loss = criterion(output, true_category_tensor)
    loss.backward()

    # Add parameters' gradients to their values, multiplied by learning rate
    for p in rnn.parameters():
        p.data.add_(p.grad.data, alpha=-learning_rate)

    return output, loss.item()


######################################################################
# Now we just have to run that with a bunch of examples. Since the
# ``train`` function returns both the output and loss we can print its
# guesses and also keep track of loss for plotting. Since there are 1000s
# of examples we print only every ``print_every`` examples, and take an
# average of the loss.
#


# Keep track of losses for plotting


def timeSince(since):
    now = time.time()
    s = now - since
    m = s // 60
    s -= m * 60
    return '%dm %ds' % (m, s)


start = time.time()


def rnn_gen_fit(n_iters=10, print_every=5000, plot_every=1000):
    current_loss = 0
    all_losses = []

    for iter in range(1, n_iters + 1):
        example = random_training_example_char()

        last_char = example['last_char']
        line = example['line']
        last_char_tensor = example['last_char_tensor']
        line_tensor = example['line_tensor']
        print(f'last_char {last_char}')
        print(f'line: {line}')
        print(f'last_char_tensor: {last_char_tensor}')
        print(f'line_tensor: {line_tensor}')

        # last_char_tensor needs to be the same shape as the output tensor from the rnn
        output, loss = train(last_char_tensor[0], line_tensor)
        current_loss += loss

        # Print iter number, loss, name and guess
        if iter % print_every == 0:
            guess, guess_i = last_char_from_output(output)
            correct = '✓' if guess == last_char else '✗ (%s)' % last_char
            print('%d %d%% (%s) %.4f %s / %s %s' % (iter, iter / n_iters * 100, timeSince(start), loss, line, guess, correct))

        # Add current loss avg to list of losses
        if iter % plot_every == 0:
            all_losses.append(current_loss / plot_every)
            current_loss = 0
    return dict(model=rnn, losses=all_losses, categories=all_categories, char2i=CHAR2I, i2char=I2CHAR)


def rnn_fit(model, n_iters=10, print_every=5000, plot_every=1000):
    current_loss = 0
    all_losses = []

    for iter in range(1, n_iters + 1):
        example = random_training_example_char()

        category = example['category']
        line = example['line']
        last_char_tensor = example['last_char_tensor']
        line_tensor = example['line_tensor']
        print(f'category: {category}')
        print(f'line: {line}')
        print(f'last_char_tensor: {last_char_tensor}')
        print(f'line_tensor: {line_tensor}')

        # last_char_tensor needs to be the same shape as the output tensor from the rnn
        output, loss = train(model, last_char_tensor[0], line_tensor)
        current_loss += loss

        # Print iter number, loss, name and guess
        if iter % print_every == 0:
            cat_pred, cat_i_pred = last_char_from_output(output)
            check = '✓' if cat_pred == category else f'✗ (truth={category})'
            print(f'{iter} {(iter / n_iters):2d}% {timeSince(start)} {loss:.4f} {line} / {cat_pred} {check}')

        # Add current loss avg to list of losses
        if iter % plot_every == 0:
            all_losses.append(current_loss / plot_every)
            current_loss = 0
    return dict(model=rnn, losses=all_losses, categories=all_categories, char2i=CHAR2I, i2char=I2CHAR)


# Just return an output given a line


def compute_confusion(model, n_categories=n_categories, n_confusion=10000):
    # Keep track of correct guesses in a confusion matrix
    confusion = torch.zeros(n_categories, n_categories)

    # Go through a bunch of examples and record which are correctly guessed
    for i in range(n_confusion):
        samp = random_training_example_category()
        output = model.output_from_line_tensor(samp['line_tensor'])
        guess, guess_i = category_from_output(output)
        category_i = all_categories.index(samp['category'])
        confusion[category_i][guess_i] += 1

    # Normalize by dividing every row by its sum
    for i in range(n_categories):
        confusion[i] = confusion[i] / confusion[i].sum()

    return confusion


def predict_category(input_line, topk=3, **meta):
    categories = meta['categories']
    model = meta['model']
    print(f'\nline: {input_line}')
    with torch.no_grad():
        output = model.output_from_line_tensor(encode_one_hot_seq(input_line))
        topv, topi = output.topk(topk, 1, True)
        predictions = []

        for i in range(topk):
            value = topv[0][i].item()
            category_index = topi[0][i].item()
            print(f'{value:.2f}: {categories[category_index]}')
            predictions.append([value, [category_index]])


if __name__ == '__main__':
    # predict nationality (category)
    rnn = RNN(input_size=len(ASCII_NAME_CHARS), hidden_size=128, output_size=len(all_categories))
    meta = rnn_fit(n_iters=10, print_every=5000, plot_every=1000)
    preserve_model('rnn_name_nationality', **meta)
#     more src/nlpia2/all_categories.json 
# {"all_categories": ["Arabic", "Irish", "Spanish", "French", "German", "English", "Korean", "Vietnamese", "Scottish", "Japanese", "Polish", "Greek", "Czech", "Italian", "Por
# tuguese", "Russian", "Dutch", "Chinese"], "char2i": {"g": 0, "J": 1, "j": 2, "l": 3, "X": 4, "e": 5, "L": 6, "H": 7, " ": 8, "'": 9, "w": 10, "O": 11, "U": 12, "E": 13, "c"
# : 14, "F": 15, "a": 16, "Q": 17, "y": 18, "u": 19, "I": 20, "W": 21, ",": 22, "p": 23, "b": 24, "z": 25, "G": 26, "T": 27, "t": 28, "q": 29, "S": 30, "m": 31, "d": 32, "K":
#  33, "n": 34, "i": 35, "x": 36, "Y": 37, "M": 38, "R": 39, "r": 40, "N": 41, "-": 42, "f": 43, "Z": 44, "s": 45, "D": 46, "P": 47, "o": 48, ";": 49, "v": 50, "k": 51, "V": 
# 52, "h": 53, "C": 54, "A": 55, ".": 56, "B": 57}}

    predict_category('Dovesky', topk=2, **meta)
    predict_category('Jackson', topk=2, **meta)
    predict_category('Satoshi', topk=2, **meta)

    plt.figure()
    plt.plot(meta['losses'])
    plt.xlabel('sample')
    plt.ylabel('cross-entropy (log loss)')

    # predict last char
    meta_char = rnn_gen_fit(n_iters=10, print_every=5000, plot_every=1000)
    preserve_model('rnn_name_last_char', **meta_char)

    predict_category('Dovesk', topk=3, **meta_char)  # 'y'
    predict_category('Jackso', topk=3, **meta_char)  # 'n'
    predict_category('Satosh', topk=3, **meta_char)  # 'i'

    confusion = compute_confusion()

    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(confusion.numpy())
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + all_categories, rotation=90)
    ax.set_yticklabels([''] + all_categories)

    # Force label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # sphinx_gallery_thumbnail_number = 2
    plt.show()
