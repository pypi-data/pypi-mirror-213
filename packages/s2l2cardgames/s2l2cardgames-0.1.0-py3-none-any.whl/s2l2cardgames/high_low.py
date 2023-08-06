from .deck import Deck

class HighLow:
    def __init__(self):
        self.deck = Deck()

    def draw_card(self):
        return self.deck.draw()

    #カードの柄を切り離して比較する    
    def compare_cards(self, card1, card2):
        suit1, rank1 = card1.split("_")
        suit2, rank2 = card2.split("_")
        if rank1 == 'A':
            value1 = 14
        elif rank1 == 'K':
            value1 = 13
        elif rank1 == 'Q':
            value1 = 12
        elif rank1 == 'J':
            value1 = 11
        else:
            value1 = int(rank1)

        if rank2 == 'A':
            value2 = 14
        elif rank2 == 'K':
            value2 = 13
        elif rank2 == 'Q':
            value2 = 12
        elif rank2 == 'J':
            value2 = 11
        else:
            value2 = int(rank2)

        if value1 > value2:
            return "high"
        elif value1 < value2:
            return "low"
        else:
            return "tie"

    #high か lowの入力をする
    def player_guess(self):
        guess = input("このカードは次引くカードよりもどう予想しますか？ (high/low): ").lower()
        while guess not in ["high", "low"]:
            print("入力が誤りです. 'high' か 'low'で入力してください.")
            guess = input("このカードは次引くカードよりもどう予想しますか？ (high/low): ").lower()
        return guess