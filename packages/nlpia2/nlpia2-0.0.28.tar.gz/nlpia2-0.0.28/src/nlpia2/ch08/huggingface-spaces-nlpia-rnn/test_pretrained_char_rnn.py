from pathlib import Path
import sys

from char_rnn_from_scratch_refactored import predict_category, RNN, load_model


if __name__ == '__main__':
    args = dict(zip('filepath name'.split(), sys.argv))
    filepath = args.get('filepath', 'char_rnn_from_scratch_refactored-1_541-09min_59sec')
    filepath = Path(filepath).with_suffix('').with_suffix('')
    name = args.get('name', 'Abebe')
    if not filepath:
        filepath = 'char_rnn_from_scratch_refactored-1_541-09min_59sec'

    meta = load_model(filepath)

    model = RNN(
        n_categories=len(meta['categories']),
        vocab_size=len(meta['char2i']), n_hidden=meta['state_dict']['i2h.weight'].shape[0]
    )

    model.load_state_dict(meta['state_dict'])
    char2i = meta['char2i']

    predict_category('Hobson', categories=meta['categories'])
