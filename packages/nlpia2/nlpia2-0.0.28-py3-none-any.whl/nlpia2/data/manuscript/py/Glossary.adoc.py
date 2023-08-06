from pathlib import Path
from nlpia.book_parser import write_glossary
from nlpia.constants import DATA_PATH as DATA_DIR
DATA_DIR = Path(DATA_DIR)
print(write_glossary(
    DATA_DIR / 'book'))  # <1>
