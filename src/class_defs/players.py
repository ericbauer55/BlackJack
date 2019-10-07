from __future__ import annotations
from typing import List, Dict, Optional, Callable
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, CardPile, CardHand, Suit

ActionSet = Dict[str, Dict[str, Callable]]


def get_valid_input(input_prompt: str, valid_input_list: List[str]) -> str:
    """
    This generically prompts the user to input a string that is in the discrete valid list
    :param input_prompt: string to prompt the user to input with
    :param valid_input_list: discrete list of valid string inputs
    :return: returns a valid item from the valid_input_list parameter
    """
    x = input(input_prompt)
    if x in valid_input_list:
        return x
    else:
        print("Input {0} is invalid.".format(x))
        return get_valid_input(input_prompt, valid_input_list)  # try again


class Player:
    # =========== Constructors ===========
    def __init__(self, name: str = '', chips: Optional[ChipStack] = None, hand: Optional[CardHand] = None,
                 pot: Optional[ChipStack] = None, action_set: Optional[ActionSet] = None) -> None:
        self.name: str = name
        if chips is None:
            chips = ChipStack()
        if hand is None:
            hand = CardHand()
        if pot is None:
            pot = ChipStack()
        self.pot = pot  # unless there is a shared pot object passed in, each player instance gets its own pot instance
        self.chips: ChipStack = chips  # empty stack unless otherwise specified
        self._player_hand: CardHand = hand
        if action_set is None:
            action_set = {'actions_basic':  # load only a basic set of instance methods for actions
                              {'view-hand': self.view_hand, 'draw': self.draw,
                               'discard': self.discard, 'transfer': self.transfer}
                          }
        self.action_set: ActionSet = action_set

    # =========== Helper Methods ===========
    @property
    def hand(self) -> List[Card]:
        """This is a shortcut for getting the list of cards stored in the player's CardHand object
        This prevents calls like player.hand.hand"""
        return self._player_hand.hand

    def dispatch_action(self, action_method: Callable):
        pass

    def hand_contains_values(self, values: List[str]) -> bool:
        """This function returns true if the hand contains at least one card that has a matching value"""
        if any([card.value in values for card in self.hand]):
            return True

    def hand_contains_suits(self, suits: List[Suit]) -> bool:
        """This function returns true if the hand contains at least one card that has a matching suit"""
        if any([card.suit in suits for card in self.hand]):
            return True



    # =========== Player Card Actions ===========
    def view_hand(self, player: Optional[Player] = None, all_visible: bool = False) -> None:
        # TODO: Players manage the visibility per Card of a Hand of Cards, it shouldn't be a state of Card
        # if no player is passed to this method, assume 'self' is the player
        if player is None:
            player = self
        print('{0} viewing {1}\'s Hand:'.format(self.name, player.name))
        print(player._player_hand.to_string(all_visible=all_visible))

    def draw(self, card_pile: CardPile, n_cards: int = 1, all_visible: bool = False) -> None:
        for _ in range(1, n_cards + 1):
            drawn = card_pile.draw()
            drawn.visible = all_visible
            self._player_hand.add_card(drawn)

    def discard(self, discard_pile: CardPile, card_names: List[str]) -> None:
        for name in card_names:
            discard_pile.add(self._player_hand.remove_card(name))

    def transfer(self, other_player: Player, card_names: List[str]) -> None:
        self._player_hand.transfer_cards(other_hand=other_player._player_hand, card_names=card_names)

    # =========== Player Chip Actions ===========
    def view_chips(self, player: Optional[Player] = None, all_visible: bool = False) -> None:
        # if no player is passed to this method, assume 'self' is the player
        if player is None:
            player = self
        print('{0} viewing {1}\'s Chip Stack:'.format(self.name, player.name))
        player.chips.view_stack(tabular=False)

    def payout_chips(self, destination_pot: ChipStack, chip_amounts: Dict[str, int]) -> None:
        """This is a great function to use when placing bets with a player"""
        self.pot.transfer_chips(destination_pot, chip_amounts)

    def payout_all(self, destination_pot: ChipStack) -> None:
        """This is a great function to use when moving around chip stacks after a hand"""
        chip_amounts = self.pot.stack.copy()
        self.pot.transfer_chips(destination_pot, chip_amounts)


if __name__ == '__main__':
    deck = CardPile.from_standard_deck()
    deck.shuffle()
    py1 = Player('Player 1')
    py2 = Player('Player 2')
    # print each player's hand out
    print('Initial Player Hands: ')
    py1.view_hand(all_visible=True)
    py2.view_hand(all_visible=True)
    print('\nDeck:', deck)

    # draw some cards into each Hand
    py1.draw(deck, n_cards=5)
    py2.draw(deck, n_cards=5)
    print('\nPlayer Hands After Drawing: ')
    py1.view_hand(all_visible=True)
    py2.view_hand(all_visible=True)
    print('\nDeck:', deck)

    # transfer some cards from player 1 to player 2's hand
    py1.transfer(py2, card_names=[card.name for card in py1.hand])
    print('\nPlayer Hands After Transferring: ')
    py1.view_hand(all_visible=True)
    py2.view_hand(all_visible=True)
