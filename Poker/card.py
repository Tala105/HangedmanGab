from constants import SUITS, RANKS
from typing_extensions import Self

class Card():
    """A class representing a playing card."""

    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        self.value = RANKS.index(rank) + 1 # 1-13 13 being Ace

    def __next__(self):
        """Returns the next card of the same suit."""
        if self.rank == "K":
            return Card(self.suit, "A")
        elif self.rank == "Q":
            return Card(self.suit, "K")
        elif self.rank == "J":
            return Card(self.suit, "Q")
        else:
            return Card(self.suit, RANKS[RANKS.index(self.rank) + 1])
        
    def __suited__(self, other: Self) -> bool:
        """Checks if two cards are of the same suit."""
        return self.suit == other.suit
    
    def __paired__(self, other: Self) -> bool:
        """Checks if two cards are of the same rank."""
        return self.rank == other.rank
    
    def make_visual(self) -> str:
        """Returns the visual representation of the card."""
        row0 = f"┌───────┐\n"
        row1 = f"│ {self.rank}    │\n" if self.rank != "10" else f"│ {self.rank}   │\n"
        row2 = f"│       │\n"
        row3 = f"│   {self.suit}   │\n"
        row4 = f"│     {self.rank} │\n" if self.rank != "10" else f"│   {self.rank}│\n"
        row5 = f"└───────┘\n"
        return row0 + row1 + row2 + row3 + row4 + row5
    
    