from card import Card
import random
from constants import RANKS, SUITS, HAND_VALUES

class Hand:
    """A class representing a hand of cards."""

    def __init__(self, cards: list[Card], id: int, name: str = "Player", chips: int = 1000, status: str = "betting"):
        self.id = id
        self.name = name
        self.cards = cards
        self.chips = chips
        self.status = status
        self.betted: int = 0
        self.hand_priority: tuple[int, int] = (0, 0)

    def hand_value(self) -> str:
        """Calculates the value of the hand."""
        same_ranks: dict[str, int] = {rank: 0 for rank in RANKS}
        same_suits: dict[str, int] = {suit: 0 for suit in SUITS}
        sequence: int = 0
        straight_flush: int = 0
        
        self.cards.sort(key=lambda card: RANKS.index(card.rank), reverse=True)
        for i, card in enumerate(self.cards[1:], start=1):
            last_card = self.cards[i-1]
            # Check "Pairity"
            if last_card.rank == card.rank:
                same_ranks[card.rank] = same_ranks.get(card.rank, 0) + 1
            # Check "Flush"
            if last_card.suit == card.suit:
                same_suits[card.suit] = same_suits.get(card.suit, 0) + 1    
            # Check "Straight"
            if next(card).rank == last_card.rank:
                sequence += 1
                # Check "Straight Flush"
                if card.suit == last_card.suit:
                    straight_flush += 1            
            elif card.rank != last_card.rank:
                sequence = 0
                straight_flush = 0

        sorted_parity_check = sorted(same_ranks.items(), key=lambda item: item[1], reverse=True)
        sorted_flush_check = sorted(same_suits.items(), key=lambda item: item[1], reverse=True)
        
        if straight_flush == 4:
            return 'Straight Flush'
        if sequence == 4:
            return 'Straight'
        if sorted_flush_check and sorted_flush_check[0][1] == 4:
            return 'Flush'
        if sorted_parity_check[0][1] == 3:
            return 'Four of a Kind'
        if sorted_parity_check[0][1] == 2 and sorted_parity_check[1][1] == 1:
            return 'Full House'
        if sorted_parity_check[0][1] == 2:
            return 'Three of a Kind'
        if sorted_parity_check[0][1] == 1 and sorted_parity_check[1][1] == 1:
            return 'Two Pair'
        if sorted_parity_check[0][1] == 1:
            return 'Pair'
        if sorted_parity_check[0][1] == 0:
            return 'High Card'
        raise ValueError("No valid hand found")

    def evaluate_hand(self) -> None:
        """Evaluates the hand and assigns a priority value."""
        hand_value = HAND_VALUES[self.hand_value()]
        secondary_value = RANKS.index(self.sorted_hand[0].rank)
        self.hand_priority = (hand_value, secondary_value)
        
    
    def make_visual(self, num_cards=None) -> str:
        """Returns the visual representation of the hand."""
        if num_cards is None:
            num_cards = len(self.cards)
        card_visuals = [card.make_hidden_visual().splitlines() for card in self.cards[num_cards:]]            
        card_visuals.extend([card.make_visual().splitlines() for card in self.cards[:num_cards]])
        stacked_rows = [''] * len(card_visuals[0])
        for i, visual in enumerate(card_visuals):
            for j, line in enumerate(visual):
                if i < len(card_visuals) - 1:
                    if j == len(card_visuals[0])// 2:
                        stacked_rows[j] += line[:2] + line[3] # Middle line shows suit
                    else:
                        stacked_rows[j] += line[:3] # Half card for first cards
                else:
                        stacked_rows[j] += line # Full card visual for last card
        return '\n'.join(stacked_rows)
    
    @property
    def sorted_hand(self) -> list[Card]:
        """Returns the hand sorted by rank."""
        return sorted(self.cards, key=lambda card: RANKS.index(card.rank), reverse=True)
    
            
def main():
    hands = {
    "high_card": [Card("♠", "2"), Card("♥", "3"), Card("♠", "4"), Card("♠", "5"), Card("♠", "6")],
    "pair": [Card("♠", "10"), Card("♠", "10")],
    "two_pair": [Card("♠", "10"), Card("♠", "10"), Card("♥", "J"), Card("♠", "J")],
    "three_kind": [Card("♠", "10"), Card("♠", "10"), Card("♥", "10")],
    "straight": [Card("♠", "10"), Card("♠", "J"), Card("♥", "Q"), Card("♠", "K"), Card("♠", "A")],
    "flush": [Card("♠", "A"), Card("♠", "3"), Card("♠", "4"), Card("♠", "5"), Card("♠", "6")],
    "full_house": [Card("♠", "10"), Card("♠", "10"), Card("♥", "10"), Card("♠", "J"), Card("♠", "J")],
    "four_kind": [Card("♠", "10"), Card("♦", "10"), Card("♥", "10"), Card("♣", "10")],
    "straight_flush": [Card("♠", "10"), Card("♠", "J"), Card("♠", "Q"), Card("♠", "K"), Card("♠", "A")]
    }

    test_keys = ["high_card", "pair", "two_pair", "three_kind", "straight", "flush", "full_house", "four_kind", "straight_flush"]
    
    for i, key in enumerate(test_keys):
        hand = hands[key]
        player_hand = Hand(hand, f"Player{i+1}")
        print(f"{player_hand.name}'s hand ({key}):\n{player_hand.make_visual()}")
        print(f"Hand value: {player_hand.hand_value()}")
        print("-" * 20)

if __name__ == "__main__":
    main()