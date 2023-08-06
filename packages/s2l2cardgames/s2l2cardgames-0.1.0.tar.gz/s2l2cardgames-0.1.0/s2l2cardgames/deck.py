import random

class Deck:
    #トランプの柄と英数字を設定
    suits = ["♠", "♥", "♦", "♣"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    #生成時にカードすべてがそろうように生成
    def __init__(self):
        self.cards = [f"{suit}_{value}" for suit in self.suits for value in self.values]
        random.shuffle(self.cards)

    #カードを引く動作
    def draw(self):
        if len(self.cards) == 0:
            raise ValueError("デッキが空です.")
        return self.cards.pop()
    
    #残り枚数を確認
    def remaining_cards(self):
        return len(self.cards)
