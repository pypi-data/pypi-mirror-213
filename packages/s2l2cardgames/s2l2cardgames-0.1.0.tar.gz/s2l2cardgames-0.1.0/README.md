# S2L2 Card Games Library

A simple Python library to play various card games, including High-Low, and Blackjack.

## Installation

Install the package using pip:

`pip install s2l2cardgames`


## Usage


### High-Low
```python
from s2l2cardgames.high_low import HighLow

game = HighLow()
game.start_game()

# Draw cards, compare cards, etc.
```
### Blackjack
```python
from s2l2cardgames.blackjack import Blackjack

game = Blackjack()
game.start_game()

# Add players, deal cards, hit, stand, etc.
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.