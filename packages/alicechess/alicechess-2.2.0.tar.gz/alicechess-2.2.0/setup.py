# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['alicechess', 'alicechess.pieces']

package_data = \
{'': ['*'], 'alicechess': ['pictures/*']}

install_requires = \
['Pillow>=9.5.0,<10.0.0']

setup_kwargs = {
    'name': 'alicechess',
    'version': '2.2.0',
    'description': 'A Python package to play Alice Chess',
    'long_description': '# Alice Chess\n\nThis project allows you to play Alice Chess, a variant of chess.\n\n## Installation\n\nThe package may be installed through `pip`:\n\n```bash\n$ pip install alicechess\n```\n\n## Rules\n\nHere is a [description of the concept and rules][rules].\n\n[rules]: https://www.chessvariants.com/other.dir/alice.html\n\nNotable game rules:\n\n- A piece\'s move must be valid on the board it is on, which means that a piece\n  on Board B can block a check on Board A after teleporting (since the move was\n  valid on Board B, and the move overall was legal because the king is not\n  staying in check). See the above link for a more detailed argument on this.\n- **Castling**: A king and rook may only castle if neither has moved already,\n  the king is not in check, the squares they will move to are vacant on both\n  boards, and the king does not move through check (on Board A) or into check.\n  After the castle, both pieces will teleport to the other board.\n- **En passant**: A pawn may capture another pawn through en passant if your\n  pawn is on Board B and the enemy pawn advances two spaces, teleporting to the\n  space right next to yours on Board B. (This results in a situation that looks\n  like regular en passant.) Note that due to teleporting to the other board\n  after each move, this can only be achieved by a pawn that _does not_ advance\n  two squares on its first move. Also, if there is a piece on Board B where the\n  en passant move would go (i.e., your pawn can already capture a piece\n  normally), then en passant will not take place.\n- **Fifty move rule**: If both players have made 50 moves each where no piece\n  has been captured or no pawn moved, then a player may claim a draw. However,\n  to simplify this case, the game will be automatically ended with a draw\n  (rather than allowing a player to claim a draw). This therefore overshadows\n  the 75-move rule, where a draw is automatically applied after 75 moves by both\n  players with no captures or pawn movements.\n- **Threefold repetition rule**: If a board position appears three times in a\n  game (not necessarily in a row), then a player may claim a draw. However, to\n  simplify this case, the game will be automatically ended with a draw (rather\n  than allowing a player to claim a draw).\n\n## How to play\n\nTo start a game between two human players, you can easily just run the package\non the command line:\n\n```bash\n$ python -m alicechess\n```\n\nA window will come up where the game can be played.\n\n## Playing against bots\n\nTo play a game against a bot or between bots, you must write your own script.\nYou should initialize a `Game` object with the appropriate players, then call\neither the `start()` or `start_window()` method. To write your own bot, see the\n[Writing a bot](#writing-a-bot) section.\n\nHere is an example:\n\n```python\n"""\nPlays a game between a human and a bot that plays randomly.\n"""\n\nfrom alicechess import Game, HumanPlayer\nfrom alicechess.bots import RandomPlayer\n\nif __name__ == "__main__":\n    Game(white=HumanPlayer, black=RandomPlayer).start_window()\n```\n\nNote that the class names (not instances) are passed to the `Game` constructor.\n\nThe `start_window()` method will, as implied, start an interactive window where\nthe game can be played. However, you can also opt to use the `start()` method\ninstead, which will return the first `GameState` of the game, and then use\nanother way to ask the user for input and play the game; for instance, you could\nmake the game entirely textual with user input provided with the keyboard. See\nthe [API Documentation][docs] for more information.\n\nIn the interactive window, there is a 3 second delay for non-human player moves,\nto simulate realism. This can be changed by passing a value for\n`non_human_player_delay` to the `start_window()` method.\n\nIt is also possible for two bots to play against each other.\n\n### Writing a bot\n\nThe code is factored in a way to make it very easy for you to code your own bots\nto play against. Simply extend the `Player` class and implement the two abstract\nmethods for making a move and promoting a pawn. This class (not an instance) can\nthen be passed into the `Game` constructor to start a game. See the\n[API Documentation][docs] for more information.\n\nHere is an example:\n\n```python\n"""\nPlays a game between a human and a bot (that I wrote).\n"""\n\nfrom alicechess import Game, HumanPlayer, Player, PromoteType\n\nclass Bot(Player):\n    """A very good bot that I wrote."""\n\n    def make_move(self, game_state):\n        for piece in game_state.yield_player_pieces():\n            for move in piece.yield_moves():\n                return move\n\n    def promote(self, game_state):\n        return PromoteType.QUEEN\n\nif __name__ == "__main__":\n    Game(white=HumanPlayer, black=Bot).start_window()\n```\n\n[docs]: https://github.com/josephlou5/alicechess/blob/main/Documentation.md\n\n## Credit\n\nThank you to Artyom Lisitsyn for inspiring me to pursue this project and to\nTrung Phan for being my chess consultant and answering all my questions on rules\nand technicalities.\n',
    'author': 'Joseph Lou',
    'author_email': 'joseph.d.lou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/josephlou5/alicechess',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
