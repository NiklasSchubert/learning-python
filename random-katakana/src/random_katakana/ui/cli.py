from os import system
from ..ui.ui import UI


class CLI(UI):
    def ask_option(self, question: str, options: dict[int, str]) -> int:
        print(f"{question}\n")
        for INDEX, OPTION_TEXT in options.items():
            print(f"{INDEX}: {OPTION_TEXT}")
        RESPONSE = int(input("Enter the number of your choice: "))
        return RESPONSE
