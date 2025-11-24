from .game.game import Game
from .ui.cli import CLI
from .word_loader.sensei_japanese_loader import SenseiJapaneseLoader


def main():
    try:
        Game(LOADER=SenseiJapaneseLoader(), UI=CLI())
    except KeyboardInterrupt:
        print("Stopped by user.")


if __name__ == "__main__":
    main()


# tile based answer out of order
# Sentence with an empty word that has to be filled with katakana
# word search grid random katakana letter grid
