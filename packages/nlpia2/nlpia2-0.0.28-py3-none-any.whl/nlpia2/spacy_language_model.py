import spacy

LANG_MODEL_NAME = 'en_core_web_md'

nlp = None

# try `load()` twice and `cli.download()` once:
for i in range(2):  
    try:
        nlp = spacy.load(LANG_MODEL_NAME)
        break
    except IOError:
        spacy.cli.download(LANG_MODEL_NAME)
