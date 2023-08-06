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
from collections import Counter
import copy
from pathlib import Path
import random
import time

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


from nlpia2.init import SRC_DATA_DIR, maybe_download
from nlpia2.string_normalizers import Asciifier, ASCII_NAME_CHARS
from persistence import save_model, load_model_meta


class RNN(nn.Module):
    def __init__(self, vocab_size, n_hidden, n_categories):
        super(RNN, self).__init__()

        self.n_hidden = n_hidden
        self.n_categories = n_categories  # <1> n_categories = n_outputs (one-hot)

        self.i2h = nn.Linear(vocab_size + n_hidden, n_hidden)
        self.i2o = nn.Linear(vocab_size + n_hidden, n_categories)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, char_tens, hidden):  # <2> x = input = char_tens
        combined = torch.cat((char_tens, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.n_hidden)


MODEL_PATH = Path(__file__).with_suffix('').name
try:
    META = load_model_meta(MODEL_PATH)
except IOError:
    META = {
        'categories': [
            "Arabic", "Irish", "Spanish", "French", "German", "English",
            "Korean", "Vietnamese", "Scottish", "Japanese", "Polish",
            "Greek", "Czech", "Italian", "Portuguese", "Russian", "Dutch", "Chinese"
        ],
        'char2i': {
            "g": 0, "J": 1, "j": 2, "l": 3, "X": 4, "e": 5, "L": 6, "H": 7, " ": 8,
            "'": 9, "w": 10, "O": 11, "U": 12, "E": 13, "c": 14, "F": 15, "a": 16,
            "Q": 17, "y": 18, "u": 19, "I": 20, "W": 21, ",": 22, "p": 23, "b": 24,
            "z": 25, "G": 26, "T": 27, "t": 28, "q": 29, "S": 30, "m": 31, "d": 32,
            "K": 33, "n": 34, "i": 35, "x": 36, "Y": 37, "M": 38, "R": 39, "r": 40,
            "N": 41, "-": 42, "f": 43, "Z": 44, "s": 45, "D": 46, "P": 47, "o": 48,
            ";": 49, "v": 50, "k": 51, "V": 52, "h": 53, "C": 54, "A": 55, ".": 56,
            "B": 57
        }
    }
    META['n_hidden'] = 128
    META['n_categories'] = len(META['categories'])
    META["model"] = RNN(
        len(META['char2i']),
        n_hidden=META['n_hidden'],
        n_categories=META['n_categories']
    )
    save_model(MODEL_PATH, **META)

print(f"Loaded META:\n{META}")
# globals().update(META)
CATEGORIES = META['categories']
n_categories = META.get('n_categories', len(CATEGORIES))
assert n_categories == len(CATEGORIES)
n_hidden = META.get('n_hidden', 128)
CHAR2I = META['char2i']
rnn = META.get('model', None)
print(f"Loaded model:\n{rnn}")
if rnn is None:
    rnn = RNN(
        len(META['char2i']),
        n_hidden=n_hidden,
        n_categories=n_categories,
    )
if 'state_dict' in META:
    rnn.load_state_dict(META['state_dict'])
    print(f"Loaded state_dict:\n{rnn}")


asciify = Asciifier(include=ASCII_NAME_CHARS)


def load_dataset(data_dir=SRC_DATA_DIR, categories=CATEGORIES):
    # !curl -O https://download.pytorch.org/tutorial/data.zip; unzip data.zip

    # Build the category_lines dictionary, a list of names per language
    # category_lines = {}
    labeled_lines = []
    print(f"Looking for files for {len(categories)} categories: {categories}")
    for i, filepath in enumerate((SRC_DATA_DIR / 'names').glob('*.txt')):
        filepath = Path(filepath)
        print(f"Loading file {i}: {filepath}.")
        category = filepath.with_suffix('').name
        if category not in categories:
            print(f"The path {filepath} looks like a new category.")
            print(f"Add it to the {filepath.with_suffix('.meta.json')} and rerun.")
            continue
        filepath = maybe_download(filename=filepath)
        with filepath.open() as fin:
            lines = [asciify(line.rstrip()) for line in fin]
            labeled_lines += list(zip(lines, [category] * len(lines)))
    return pd.DataFrame(labeled_lines, columns=('name', 'category'))


def encode_one_hot_vec(letter, char2i=CHAR2I):
    """ one-hot encode a single char """
    tensor = torch.zeros(1, len(char2i))
    tensor[0][char2i[letter]] = 1
    return tensor


def encode_one_hot_seq(line, char2i=CHAR2I):
    """ one-hot encode each char in a str => matrix of size (len(str), len(alphabet)) """
    tensor = torch.zeros(len(line), 1, len(ASCII_NAME_CHARS))
    for pos, letter in enumerate(line):
        tensor[pos][0][char2i[letter]] = 1
    return tensor


def category_from_output(output, categories=CATEGORIES):
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return categories[category_i], category_i


def output_from_str(s, char2i=CHAR2I, categories=CATEGORIES):
    """ TODO: put this in the model """
    global rnn

    inpt = encode_one_hot_seq(s, char2i=char2i)
    hidden = torch.zeros(1, n_hidden)

    output, next_hidden = rnn(inpt[0], hidden)
    print(output)

    return category_from_output(output, categories=categories)


def random_example(df, categories=CATEGORIES, char2i=CHAR2I):
    """ balanced sampling of all categories """
    line = None
    while not line:
        category = random.choice(categories)
        is_category = df['category'] == category
        num_matches = sum(is_category)
        if num_matches:
            i = random.choice(range(num_matches))
            row = df[is_category].iloc[i]
            break
    name = row['name']
    category_tensor = torch.tensor([categories.index(category)], dtype=torch.long)
    line_tensor = encode_one_hot_seq(name, char2i=char2i)
    return category, name, category_tensor, line_tensor


def train_sample(category_tensor, line_tensor, model=rnn,
                 criterion=nn.NLLLoss(), lr=.005,
                 char2i=CHAR2I, chategories=CATEGORIES):
    """ train for one epoch (one batch of example tensors) """
    hidden = model.init_hidden()

    model.zero_grad()

    for i in range(line_tensor.size()[0]):
        output, hidden = model(line_tensor[i], hidden)

    loss = criterion(output, category_tensor)
    loss.backward()

    # Add parameters' gradients to their values, multiplied by learning rate
    for p in rnn.parameters():
        p.data.add_(p.grad.data, alpha=-lr)

    return model, output, loss.item()


def time_elapsed(t0):
    """ Compute time since t0 (t0 = time.time() in seconds) """
    secs = time.time() - t0
    mins = secs // 60
    secs = int(secs - mins * 60)
    mins = int(mins)
    return f'{mins:02d}:{secs:02d}'


def evaluate_tensor(line_tensor, model=rnn):
    hidden = model.init_hidden()
    for i in range(line_tensor.size()[0]):
        output, hidden = model(line_tensor[i], hidden)
    return output


def predict_category(name, categories=CATEGORIES, char2i=CHAR2I, model=rnn):
    tensor = encode_one_hot_seq(name, char2i=char2i)
    pred_i = evaluate_tensor(tensor, model=model).topk(1)[1][0].item()
    return categories[pred_i]


def confusion_df(truth, pred, categories=CATEGORIES):
    """ Count mislabeled examples in entire dataset """
    pair_counts = Counter(zip(truth, pred))
    confusion = {c_tru: {c_pred: 0 for c_pred in categories} for c_tru in categories}
    for ((t, p), count) in pair_counts.items():
        confusion[t][p] = count
    return pd.DataFrame(confusion)


def plot_confusion(df, categories=CATEGORIES):
    df_conf = confusion_df(
        truth=df['name'],
        pred=df['name'].apply(predict_category).values,
        categories=categories,
    )
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(df_conf.values)
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + list(df_conf.columns), rotation=90)
    ax.set_yticklabels([''] + list(df_conf.index))

    # Force label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # sphinx_gallery_thumbnail_number = 2
    plt.show()


def topk_predictions(text, topk=3, categories=CATEGORIES, char2i=CHAR2I, model=rnn):
    with torch.no_grad():
        output = evaluate_tensor(encode_one_hot_seq(text, char2i=char2i), model=model)
        topvalues, topindices = output.topk(topk, 1, True)
        predictions = []
        # TODO: try this:
        for rank, (log_loss_tens, category_index) in enumerate(zip(topvalues[0], topindices[0])):
            predictions.append(
                [rank, text, log_loss_tens.item(), categories[category_index]])
    return pd.DataFrame(predictions, columns='rank text log_loss category'.split())


def print_predictions(text, n_predictions=3, categories=CATEGORIES):
    preds_df = topk_predictions(text=text, topk=n_predictions, categories=categories)
    print(preds_df)
    return preds_df


def print_example_tensor(text="O’Néàl", category="Irish", char2i=CHAR2I):

    # Transcode Unicode str ASCII without embellishments, diacritics (https://stackoverflow.com/a/518232/2809427)
    ascii_text = asciify(text)
    print(f'asciify({text}) => {ascii_text}')

    encoded_char = encode_one_hot_vec(ascii_text[0], char2i=char2i)
    print(f"encode_one_hot_vec({ascii_text[0]}): {encoded_char}")
    input_tensor = encode_one_hot_seq(ascii_text, char2i=char2i)
    print(f"input_tensor.size(): {input_tensor.size()}")


def print_dataset_samples(df, n_samples=10):
    # hidden = torch.zeros(1, n_hidden)
    # output, next_hidden = rnn(inpt, hidden)

    for i in range(n_samples):
        category, text, category_tensor, text_tensor = random_example(df)
        print(f"category:{category} text:{text} text_tens.shape:{text_tensor.shape}")


def train(df=None, model=rnn, n_iters=70000, print_every=1000, char2i=CHAR2I, categories=CATEGORIES):
    df = df if df is not None else load_dataset()
    current_loss = 0
    all_losses = []
    plot_every = print_every

    start = time.time()

    for it in range(1, n_iters + 1):
        category, line, category_tensor, line_tensor = random_example(df)
        model, output, loss = train_sample(category_tensor, line_tensor, model=model, char2i=char2i, chategories=categories, lr=.005)
        current_loss += loss

        # Print iteration number, loss, name and guess
        if not it % print_every:
            guess, guess_i = category_from_output(output, categories=categories)
            correct = '✓' if guess == category else '✗ (%s)' % category
            print(f'{it:06d} {it*100//n_iters}% {time_elapsed(start)} {loss:.4f} {line} => {guess} {correct}')

        # Add current loss avg to list of losses
        if not it % plot_every:
            all_losses.append(current_loss / plot_every)
            current_loss = 0

    train_time = time_elapsed(start)
    return dict(model=rnn, n_hidden=model.n_hidden, losses=all_losses, train_time=train_time, categories=categories, char2i=char2i)


def plot_training_curve(losses):
    plt.figure()
    plt.plot(losses)
    plt.show(block=False)

    print(f"META['categories']: {META['categories']}")
    print(f'CATEGORIES: {CATEGORIES}')
    print()
    print('Russia: https://en.wikipedia.org/wiki/Fyodor_Dostoevsky')
    print_predictions(text='Fyodor', n_predictions=3, categories=CATEGORIES)
    print_predictions(text='Dostoevsky', n_predictions=3, categories=CATEGORIES)
    print()
    print('Nigeria: https://en.wikipedia.org/wiki/Sanmi_Koyejo # Oluwasanmi')
    print_predictions(text='Oluwasanmi', n_predictions=3, categories=CATEGORIES)
    print_predictions(text='Sanmi', n_predictions=3, categories=CATEGORIES)
    print_predictions(text='Koyejo', n_predictions=3, categories=CATEGORIES)
    print()
    print('Japan: https://en.wikipedia.org/wiki/Satoshi_Nakamoto')
    print_predictions(text='Satoshi', n_predictions=3, categories=CATEGORIES)
    print_predictions(text='Nakamoto', n_predictions=3, categories=CATEGORIES)
    print()
    print('Etheopia: https://en.wikipedia.org/wiki/Rediet_Abebe')
    print_predictions(text='Rediet', n_predictions=3, categories=CATEGORIES)
    print_predictions(text='Abebe', n_predictions=3, categories=CATEGORIES)
    print()
    print('Italy: https://en.wikipedia.org/wiki/Silvio_Micali')
    print_predictions(text='Silvio', n_predictions=3, categories=CATEGORIES)
    print_predictions(text='Micali', n_predictions=3, categories=CATEGORIES)


def save_results(**results):
    # load/save test for use on the huggingface spaces server
    METANEW = copy.copy(results)
    # METANEW = dict(
    #     categories=CATEGORIES,
    #     char2i=CHAR2I
    # )
    METANEW['model'] = results['model']
    METANEW['losses'] = results['losses']
    METANEW['train_time'] = results['train_time']

    METANEW['state_dict'] = results['model'].state_dict()
    METANEW['min_loss'] = min(METANEW['losses'])
    print(f"min_loss: {METANEW['min_loss']}")
    train_time_str = str(results['train_time']).replace(':', 'min_') + 'sec'
    filename = str(MODEL_PATH) + f"-{METANEW['min_loss']:.3f}-{train_time_str}"
    filename = filename.replace('.', '_')
    save_model(filename, **METANEW)
    print(f'Model METANEW.keys(): {METANEW.keys()}')
    print(f'Saving model state_dict and meta to {filename}.*')


if __name__ == '__main__':
    df = load_dataset()
    results = train(df=df)
    save_results(**results)
