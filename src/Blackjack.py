import random
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, CardPile, CardHand
from src.class_defs.players import Player, get_valid_input
from typing import Dict, List, Optional, Tuple
import time

class BlackJack:
    # =========== Constructors ===========
    def __init__(self):
        # Setup the Players
        self.dealer: Player = Player(name='dealer', chips=ChipStack.from_dealer_stack())
        self.players: Dict[str, Player] = {'human': Player('human', ChipStack.from_standard_stack())}
        self.dealt_in_players: List[str] = list(self.players.keys())  # deal-in all players initially
        # Setup the Decks
        self.draw_pile: CardPile = CardPile.from_standard_deck()
        self.draw_pile.shuffle()
        self.discard_pile: CardPile = CardPile()


    # =========== Helper Methods ===========
    @staticmethod
    def pause(message: str = ''):
        print(message + '...')
        time.sleep(2)

    @staticmethod
    def get_hand_value(player: Player) -> Tuple[int]:
        """This returns the sum total value of the player's hand
        Aces are 2 or 11, hence this could return a tuple"""
        total: List[int] = [0]
        # check to how many aces are in the hand
        n_aces: int = ['A' if x.value == 'A' else '' for x in player.hand].count('A')
        ACE_VALUES: Tuple[int, int] = (2, 11)
        # figure out the value of cards that aren't aces
        for card in player.hand:
            if card.value in ['J', 'Q', 'K']:
                # face cards being worth 10
                total[0] += 10
            elif card.value == 'A':
                # skip the aces, we'll account for them next
                continue
            else:
                # otherwise add the pip value of the card
                total[0] += int(card.value)
        if n_aces == 0:
            return tuple(total)
        # next figure out the potential values of the hand with all the aces
        n_combs = 2 ** n_aces
        total *= n_combs  # duplicate the base sum 2^n_aces times
        for i in range(n_combs):
            # if n_combs = 4, then this loops over [0, 1, 2, 3] = 0b[00, 01, 10, 11]
            # Each bit place of 0bXX represents the option of one ace's value,
            # where ACE_VALUES[0] = 2, ACE_VALUES[1] = 11
            ace_values: List[int] = [ACE_VALUES[(i >> k) and 1] for k in range(0, n_combs)]
            total[i] += sum(ace_values)

        return tuple(total)

    @staticmethod
    def is_bust(player: Player) -> bool:
        """If all of the possible values are above 21, then the player has busted"""
        hand_values: Tuple[int] = BlackJack.get_hand_value(player)
        if all([value > 21 for value in hand_values]):
            return True
        else:
            return False

    @staticmethod
    def is_blackjack(player: Player) -> Tuple[bool, float]:
        """If any of the possible values are equal to 21, then the player has gotten blackjack
        If there was a Blackjack, then the payout rate is 1:1 is Ace + 10-card, or 3:2 otherwise"""
        hand_values: Tuple[int] = BlackJack.get_hand_value(player)
        if any([value == 21 for value in hand_values]):
            blackjack = True
            # if player.hand contains an ace & a 10 or J,K,Q then return 1.0
            if player.hand_contains_values(['A']) and player.hand_contains_values(['10', 'J', 'Q', 'K']):
                payout_rate = 1.0
            else:
                payout_rate = 1.5
        else:
            blackjack, payout_rate = False, 0
        return blackjack, payout_rate

    # =========== Game Actions ===========
    # These are the fundamental operations of a game
    def take_bets(self, min_bet: int = 1) -> None:
        """This function checks if each dealt-in player wants to place a bet, with some minimum imposed"""
        #for player_name, player_obj in self.players.items():  # the dealer doesn't have to buy-in; they are the house
        #    # check if player even has the buy-in amount
        #    valid_bets: List[str]
        pass

    def deal_cards(self, players: List[Player], n_cards: int = 1, n_visible: Optional[int] = None) -> None:
        """
        This function deals :param n_cards to each player in the list :param players. This is specified this way so that
        the dealer can deal to himself separately from players
        If the draw pile doesn't have enough cards left in it for all players, the remainder will be dealt
        and the discard pile will be shuffled in.
        """
        for player in players:
            for i in range(n_cards):
                # check to see if draw pile still has cards in it
                if self.draw_pile.n_items == 0:
                    # if not, shuffle discard pile into draw pile and continue
                    for _ in range(self.discard_pile.n_items):
                        self.draw_pile.add(self.discard_pile.draw())
                    self.draw_pile.shuffle()

                visible: bool = True if n_visible > 0 else False  # flag to see if this card is visible
                player.draw(self.draw_pile, n_cards=1, all_visible=visible)
                n_visible -= 1

    def check_for_payout(self, player: Player) -> bool:
        """
        This function checks to see if a single player (not a dealer) has gotten blackjack or busted.
        If they have, then return out_of_game=True for 'removal from dealt-in players logic'
        """
        out_of_game: bool = False
        (is_blackjack, payout_rate) = BlackJack.is_blackjack(player)
        if is_blackjack:
            # Dealer pays out to the player
            # assume rounding down is house cut
            payout_value: int = int(payout_rate * player.pot.stack_value)
            n_payout_chips: Dict[str, int] = ChipStack.get_chips_from_amount(payout_value, denom_pref='high')
            self.dealer.payout_chips(player.pot, n_payout_chips)
            # Remove player from dealt_in list
            self.dealt_in_players.remove(player.name)
            print('{0} has gotten blackjack and wins ${1}'.format(player.name, payout_value))
            out_of_game = True
        elif BlackJack.is_bust(player):
            # Player pays out to dealer
            player.payout_all(self.dealer.pot)
            # Remove player from dealt_in list
            self.dealt_in_players.remove(player.name)
            print('{0} has busted and loses ${1}'.format(player.name, player.pot.stack_value))
            out_of_game = True
        return out_of_game

    def check_for_payouts(self, end_of_hand: bool = False) -> None:
        """
        This function checks to see all players have gotten blackjack or busted.
        If they have, then they are removed from the dealt-in players list and payouts go accordingly.
        Additionally, if its the end of the hand, the scores vs. the dealer are checked and paid put
        """
        max_dealer_hand_value: int = max(BlackJack.get_hand_value(self.dealer))
        dealer_busted: bool = True if max_dealer_hand_value > 21 else False
        for player_name in self.dealt_in_players:
            if end_of_hand:
                # This will be used later for checking payouts at the end of a hand
                max_player_hand_value: int = max(BlackJack.get_hand_value(self.players[player_name]))

            out_of_game = self.check_for_payout(self.players[player_name])
            if out_of_game:
                continue  # don't continue to check other conditions

            if end_of_hand and (max_player_hand_value > max_dealer_hand_value or dealer_busted):
                # Dealer pays out to the player
                # assume rounding down is house cut
                payout_value: int = int(1.5 * self.players[player_name].pot.stack_value)
                n_payout_chips: Dict[str, int] = ChipStack.get_chips_from_amount(payout_value, denom_pref='high')
                self.dealer.payout_chips(self.players[player_name].pot, n_payout_chips)
                # Remove player from dealt_in list
                self.dealt_in_players.remove(player_name)
                # Print the results
                self.players[player_name].view_hand(self.dealer, all_visible=True)
                if dealer_busted:
                    print('Dealer busts so {0} wins ${1}'.format(player_name, payout_value))
                else:
                    print('{0} beat the dealer and wins ${1}'.format(player_name, payout_value))
            elif end_of_hand and not dealer_busted and (max_player_hand_value < max_dealer_hand_value):
                # Player pays out to dealer
                self.players[player_name].payout_all(self.dealer.pot)
                # Remove player from dealt_in list
                self.dealt_in_players.remove(player_name)
                # Print the results
                self.players[player_name].view_hand(self.dealer, all_visible=True)
                print('Dealer did not bust and beats {0}\'s hand. {0} loses ${1}'.format(player_name, payout_value))


    # =========== Control Flow Actions ===========
    # These are the functions that solicit user input and control the order of game operations
    def play(self) -> None:
        BlackJack.pause('[Starting New Hand]'.center(50, '=') + '\n')
        self._init_hand()
        BlackJack.pause('[Going to Hit or Stand]'.center(50, '=') + '\n')
        self._loop_hand()
        BlackJack.pause('[Finishing the Hand]'.center(50, '=') + '\n')
        self._finish_hand()

    def _init_hand(self, buy_in: int = 1):
        """This initializes a hand of blackjack with a minimum buy-in of :param buy_in dollars."""
        # zeroth check to make sure buy_in denom is in the standard chip denoms
        buy_in_key = ChipStack.get_chip_string(buy_in)
        if buy_in_key not in ChipStack.get_empty_stack().keys():
            raise KeyError('The buy-in value of \'{}\' is not in the standard denominations'.format(buy_in_key))
        # first check if all players want to buy-in to the hand
        self.dealt_in_players = list(self.players.keys())  # deal in all players initially
        self.take_bets(min_bet=buy_in)
        # second deal hands to all players that are still dealt-in
        self.deal_cards(list(self.players.values()), n_cards=2, n_visible=2)  # two face up
        self.deal_cards([self.dealer], n_cards=1, n_visible=1)  # one face up
        self.deal_cards([self.dealer], n_cards=1, n_visible=0)  # one face down
        # print out the hands for all players and their bets
        for player_name in self.dealt_in_players:
            self.players[player_name].view_hand(all_visible=True)
        self.dealer.view_hand()
        # lastly check for any naturals or busts before moving to game loop
        self.check_for_payouts(end_of_hand=False)
        return  # move to the next state of gameplay

    def _loop_hand(self) -> None:
        """This runs the game in the looping state until an exit condition (all players 'stay') is reached"""
        # get the actions of each player
        actions: List[str] = [''] * len(self.players.keys())
        for i, player_name in enumerate(self.dealt_in_players):
            out_of_game: bool = False
            while actions[i] != 'stand' and not out_of_game:
                if player_name == 'human':
                    actions[i] = get_valid_input('Would you like to hit or stand?\n>', ['hit', 'stand'])
                else:
                    # TODO: implement get_card_action for NPC subclass of player
                    #actions[i] = self.players[player_name].get_card_action(game='blackjack')
                    pass
                if actions[i] == 'hit':
                    self.deal_cards([self.players[player_name]], n_cards=1, n_visible=1)
                    self.players[player_name].view_hand()
                    out_of_game = self.check_for_payout(self.players[player_name])
        return  # move to the next state of gameplay

    def _finish_hand(self) -> None:
        """After exit condition for looping state is reached, this method finishes the hand"""
        # get the hit/stay actions of the dealer after all other players have stayed
        # Dealer turns up their face down card
        self.dealer.view_hand(all_visible=True)
        # Continue hitting until value of hand is 17 or more
        # NOTE: aces count as 11 if doing so brings hand value to 17 or more (but not over 21)
        dealer_stands: bool = False
        while not dealer_stands:
            BlackJack.pause()
            hand_values: Tuple[int] = BlackJack.get_hand_value(self.dealer)
            if len(hand_values) < 2:  # dealer has no aces to consider
                if hand_values[0] >= 17:
                    print('The dealer has 17 or more and must stand.')
                    dealer_stands = True
                else:
                    print('The dealer only has {} and must hit.'.format(hand_values[0]))
                    dealer_stands = False
                    self.dealer.draw(self.draw_pile, n_cards=1, all_visible=True)
                    self.dealer.view_hand(all_visible=True)
            else:  # dealer has aces to consider
                if any([17 <= x <= 21 for x in hand_values]):
                    print('The dealer has 17 or more and must stand.')
                    dealer_stands = True
                else:
                    hand_values = tuple([x for x in hand_values if x < 17])  # remove the values that would bust
                    if len(hand_values) == 0:
                        print('The dealer has 17 or more and must stand.')
                        dealer_stands = True
                    else:
                        print('The dealer only has {} and must hit.'.format(min(hand_values)))
                        dealer_stands = False
                        self.dealer.draw(self.draw_pile, n_cards=1, all_visible=True)
                        self.dealer.view_hand(all_visible=True)

        # if the dealer busts, that is handled in the payouts phase next:
        self.check_for_payouts(end_of_hand=True)


if __name__ == '__main__':
    game = BlackJack()
    game.play()
