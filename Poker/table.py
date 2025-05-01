from random import shuffle
from hand import Hand
from card import Card
from constants import SUITS, RANKS, HAND_VALUES
class Table:
    def __init__(self, cards: list[str], num_players: int, base_chips: int = 1000):
        """A class representing the table in a poker game."""
        self.cards = cards
        self.num_players = num_players
        self.base_chips = base_chips
        self.round = 0
        self.pots: list[int] = [0]
        self.blind: int = 10
        self.min_bet = self.blind
        self.deck: list[Card] = self.create_deck()
        self.players: list[Hand] = self.create_players()
        self.community_cards: Hand = self.create_community_cards()

    def create_deck(self) -> list[Card]:
        """Creates a deck of cards."""
        sorted_deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        shuffle(sorted_deck)
        return sorted_deck
    
    def create_players(self) -> list[Hand]:
        """Creates players with hands."""
        players = []
        for i in range(self.num_players):
            hand_cards = [self.deck.pop(), self.deck.pop()]
            players.append(Hand(hand_cards, f"Player{i+1}", self.base_chips))
        return players
    
    def create_community_cards(self) -> Hand:
        """Creates community cards."""
        community_cards = []
        for _ in range(5):
            community_cards.append(self.deck.pop())
        return Hand(community_cards, "Community Cards", 0)

    def winning_hand(self, hand1: Hand, hand2: Hand) -> str:
        """Compares two hands and returns the winning hand."""
        hand1_value = HAND_VALUES[hand1.hand_value()]
        hand2_value = HAND_VALUES[hand2.hand_value()]
        
        if hand1_value > hand2_value:
            winner = hand1.name
        elif hand1_value < hand2_value:
            winner = hand2.name
        else:
            if hand1.sorted_hand[0].value > hand2.sorted_hand[0].value:
                winner = hand1.name
            elif hand1.sorted_hand[0].value < hand2.sorted_hand[0].value:
                winner = hand2.name
            else:
                winner = "Tie"
        return winner


    def fold(self, i: int) -> None:
        """Handles the fold action."""
        player = self.players[i]
        print(f"{player.name} folds. Remaining chips: {player.chips}")
        player.status = "folded"
        
    def all_in(self, i: int) -> None:
        """Handles the all-in action."""
        player = self.players[i]
        if player.chips > 0:
            self.pots[len(self.pots)] += player.chips
            self.min_bet = max(self.min_bet, player.chips)
            print(f"{player.name} goes all-in with {player.chips} chips, Minimum bet is now {self.min_bet}.")
            player.chips = 0
            player.status = "all-in"
        else:
            print(f"{player.name} is already all-in.")
        
    def call(self, i: int) -> None:
        """Handles the call action."""
        player = self.players[i]
        if player.chips >= self.min_bet:
            player.chips -= self.min_bet
            self.pots[len(self.pots)] += self.min_bet
            print(f"{player.name} calls the bet of {self.min_bet}. Remaining chips: {player.chips}")
        else:
            print(f"{player.name} does not have enough chips to call. Remaining chips: {player.chips}")
            input("Do you want to go all-in? (y/n): ")
            if input().lower() == 'y':
                self.all_in(i)
            else:
                self.fold(i)
    
    def raise_bet(self, i: int, amount: int) -> None:
        """Handles the raise action."""
        player = self.players[i]
        if amount == player.chips:
            self.all_in(i)
            return
        player.chips -= amount
        self.pots[len(self.pots)] += amount
        self.min_bet = amount
        print(f"{player.name} raises the bet by {amount}. Remaining chips: {player.chips}")
        
    
    def betting_round(self):
        """Simulates a betting round."""
        for i, player in enumerate(self.players):
            print(f"{player.name}'s turn to bet.")
            print(player.make_visual())
            print(f"Current pot: {sum(self.pots)}, Minimum bet: {self.min_bet}")
            actions = ["call", "raise", "all-in", "fold"]
            while True:
                action = input("Choose action (call, raise, all-in, fold): ").lower()
                if action == "raise":
                    while True:
                        amount = int(input("Enter the amount to raise: "))
                        if amount > self.min_bet and amount <= player.chips:
                            self.raise_bet(i, amount)
                            break
                        else:
                            print(f"Invalid amount. You must raise more than {self.min_bet} and less than or equal to your chips ({player.chips}).")
                    break
                elif action in actions:
                    getattr(self, action)(i)
                    break
                else:
                    print("Invalid action. Please try again.")
        self.round += 1
        self.min_bet = self.blind


    def show_community_card(self) -> str:
        """Returns the community cards of the current round."""
        cards_per_round = {0:0, 1:3, 2:4, 3:5}
        card_on_table = cards_per_round[self.round]
        return self.community_cards.make_visual(num_cards=card_on_table)
    

