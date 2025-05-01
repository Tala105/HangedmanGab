from hand import Hand
from card import Card
from random import shuffle

class Table:
    def __init__(self, cards: list[str], num_players: int):
        """A class representing the table in a poker game."""
        self.cards = cards
        self.num_players = num_players
        self.deck = self.create_deck()
        self.players = self.create_players()
        self.community_cards = self.create_community_cards()

    def create_deck(self) -> list[Card]:
        """Creates a deck of cards."""
        suits = ["♠", "♥", "♦", "♣"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        sorted_deck = [Card(suit, rank) for suit in suits for rank in ranks]
        shuffle(sorted_deck)
        return sorted_deck
    
    def create_players(self) -> list[Hand]:
        """Creates players with hands."""
        players = []
        for _ in range(self.num_players):
            hand_cards = [self.deck.pop(), self.deck.pop()]
            players.append(Hand(hand_cards))
        return players
    
    def create_community_cards(self) -> list[Card]:
        """Creates community cards."""
        community_cards = []
        for _ in range(5):
            community_cards.append(self.deck.pop())
        return community_cards
