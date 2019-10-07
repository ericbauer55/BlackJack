import random
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, CardPile, CardHand
from src.class_defs.players import Player, get_valid_input
from typing import Dict, List, Optional


class BlackJack:
    # =========== Constructors ===========
    def __init__(self):
        # Setup the Players
        self.dealer: Player = Player(name='dealer', chips=ChipStack.from_dealer_stack())
        self.dealer.chips.view_stack()
        self.players: Dict[str, Player] = {'human': Player('human', ChipStack.from_standard_stack())}
        self.dealt_in_players: List[str] = list(self.players.keys())  # deal-in all players initially
        # Setup the Decks
        self.draw_pile: CardPile = CardPile.from_standard_deck()
        self.draw_pile.shuffle()
        self.discard_pile: CardPile = CardPile()


    # =========== Helper Methods ===========
    @staticmethod
    def get_hand_value(player: Player) -> int:
        pass

    @staticmethod
    def is_bust(player: Player) -> bool:
        pass

    @staticmethod
    def is_blackjack(player: Player) -> bool:
        pass

    # =========== Game Actions ===========
    # These are the fundamental operations of a game
    def init_hand(self, buy_in: int=1):
        """This initializes a hand of blackjack with a minimum buy-in of :param buy_in dollars."""
        # zeroth check to make sure buy_in denom is in the standard chip denoms
        buy_in_key = ChipStack.get_chip_string(buy_in)
        if buy_in_key not in ChipStack.get_empty_stack().keys():
            raise KeyError('The buy-in value of \'{}\' is not in the standard denominations'.format(buy_in_key))
        # first check if all players want to buy-in to the hand
        self.dealt_in_players = list(self.players.keys())  # deal in all players initially
        self.take_bets(min_bet=buy_in)
        # second deal hands to all players that are still dealt-in
        self.deal_cards()
        # lastly check for any naturals or busts before moving to game loop
        for player_name in self.dealt_in_players:
            if BlackJack.is_blackjack(self.players[player_name]):
                # Dealer pays out to the player
                # Remove player from dealt_in list
                pass
            if BlackJack.is_bust(self.players[player_name]):
                # Player pays out to dealer
                # Remove player from dealt_in list
                pass


    def take_bets(self, min_bet: int = 1) -> None:
        """This function checks if each dealt-in player wants to place a bet, with some minimum imposed"""
        for player_name, player_obj in self.players.items():  # the dealer doesn't have to buy-in; they are the house
            # check if player even has the buy-in amount
            valid_bets: List[str]

    def deal_cards(self, players: List[Player], n_cards: int = 1):
        """
        This function deals :param n_cards to each player in the list :param players
        If the draw pile doesn't have enough cards left in it for all players, the remainder will be dealt
        and the discard pile will be shuffled in.
        """
        pass

    # =========== Control Flow Actions ===========
    # These are the functions that solicit user input and control the order of game operations

if __name__ == '__main__':
    game = BlackJack()