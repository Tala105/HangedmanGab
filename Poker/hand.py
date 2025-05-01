from card import Card
from constants import SUITS, RANKS, HAND_VALUES

class Hand:
    """A class representing a hand of cards."""

    def __init__(self, cards: list[Card]):
        self.cards = cards

    def hand_value(self) -> str:
        """Calculates the value of the hand."""
        same_ranks: dict[str, int] = {}
        same_suits: dict[str, int] = {}
        sequence: int = 0
        straight_flush: int = 0
        
        self.cards.sort(key=lambda card: RANKS.index(card.rank), reverse=True)
        for i, card in enumerate(self.cards[1:]):
            last_card = self.cards[i-1]            
            # Check "Flush"
            if last_card.suit == card.suit:
                same_suits[card.suit] = same_suits.get(card.suit, 0) + 1    
            # Check "Straight"
            if card.rank == next(last_card).rank:
                sequence += 1
                # Check "Straight Flush"
                if card.suit == last_card.suit:
                    straight_flush += 1
            # Check "Pair"(Also eliminates the sequence being broken by repetition)
            elif last_card.rank == card.rank:
                same_ranks[card.rank] = same_ranks.get(card.rank, 0) + 1
            else:
                sequence = 0    
        
        sorted_parity_check = sorted(same_ranks.items(), key=lambda item: item[1], reverse=True)
        sorted_flush_check = sorted(same_suits.items(), key=lambda item: item[1], reverse=True)
        
        if straight_flush == 4:
            return 'Straight Flush'
        if sequence == 4:
            return 'Straight'
        if sorted_flush_check[0][1] == 5:
            return 'Flush'
        if sorted_parity_check[0][1] == 4:
            return 'Four of a Kind'
        if sorted_parity_check[0][1] == 3 and sorted_parity_check[1][1] == 2:
            return 'Full House'
        if sorted_parity_check[0][1] == 3:
            return 'Three of a Kind'
        if sorted_parity_check[0][1] == 2 and sorted_parity_check[1][1] == 2:
            return 'Two Pair'
        if sorted_parity_check[0][1] == 2:
            return 'Pair'
        if sorted_parity_check[0][1] == 1 and sorted_flush_check[0][1] == 1:
            return 'High Card'
        raise ValueError("No valid hand found")
    
    @property
    def sorted_hand(self) -> list[Card]:
        """Returns the hand sorted by rank."""
        return sorted(self.cards, key=lambda card: RANKS.index(card.rank), reverse=True)

    def __winning_hand__(self, other: 'Hand') -> str:
        """Compares two hands and returns the winning hand."""
        self_value = HAND_VALUES[self.hand_value()]
        other_value = HAND_VALUES[other.hand_value()]
        
        if self_value > other_value:
            return "Player 1 wins!"
        elif self_value < other_value:
            return "Player 2 wins!"
        else:
            if self.sorted_hand[0].value > other.sorted_hand[0].value:
                return "Player 1 wins!"
            elif self.sorted_hand[0].value < other.sorted_hand[0].value:
                return "Player 2 wins!"
            else:
                return "It's a tie!"