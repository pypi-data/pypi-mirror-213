"""
Starts and runs a game in a window between two human players.
"""

# ======================================================================

import sys

from alicechess import bots
from alicechess.game import Game
from alicechess.player import HumanPlayer

# ======================================================================


def main():
    _, *args = sys.argv

    if len(args) == 0:
        white = HumanPlayer
        black = HumanPlayer
    elif len(args) == 2:
        pass

    Game(white=HumanPlayer, black=HumanPlayer).start_window()


if __name__ == "__main__":
    main()
