from .cli import CLI
from .word_loader.sensei_japanese_loader import SenseiJapaneseLoader
from .mode.word_grid import WordGrid
from pprint import pprint
from .cli import WordSearchPuzzle


def main():
    try:
        CLI(LOADER=SenseiJapaneseLoader())
    except KeyboardInterrupt:
        print("Stopped by user.")


if __name__ == "__main__":
    main()


# tile based answer out of order
# Sentence with an empty word that has to be filled with katakana
# word search grid random katakana letter grid
