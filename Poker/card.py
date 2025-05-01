from constants import SUITS_NAMES, RANKS
from typing_extensions import Self

class Card():
    """A class representing a playing card."""

    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.suit_name = SUITS_NAMES[suit]
        self.rank = rank
        self.value = RANKS.index(rank) + 1 # 1-13 13 being Ace

    def __next__(self):
        """Returns the next card of the same suit."""
        return Card(self.suit, RANKS[(RANKS.index(self.rank) + 1) % len(RANKS)])
    
    def __str__(self) -> str:
        """Returns the string representation of the card."""
        return f"{self.rank} of {self.suit_name}"
    
    def make_visual(self) -> str:
        """Returns the visual representation of the card."""
        row0 = f"┌─────┐\n"
        row1 = f"│{self.rank}    │\n" if self.rank != "10" else f"│{self.rank}   │\n"
        row2 = f"│  {self.suit}  │\n"
        row3 = f"│    {self.rank}│\n" if self.rank != "10" else f"│   {self.rank}│\n"
        row4 = f"└─────┘\n"
        return row0 + row1 + row2 + row3 + row4
    
    def make_hidden_visual(self) -> str:
        """Returns the visual representation of the card when hidden."""
        row0 = f"┌─────┐\n"
        row1 = f"│/////│\n"
        row2 = f"│/////│\n"
        row3 = f"│/////│\n"
        row4 = f"└─────┘\n"
        return row0 + row1 + row2 + row3 + row4
    
def main():
    card = Card("♠", "10")
    print(card.make_visual())
    print(card)
    next_card = next(card)
    print(next_card.make_visual())
    print(next_card)


if __name__ == "__main__":
    main()
    