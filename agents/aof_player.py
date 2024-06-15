from game.players import BasePokerPlayer

def card_to_numeric(card):
    value = card[1:]
    value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    if value in value_dict:
        value = value_dict[value]
    else:
        value = int(value)
    return value

class AOFPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        hole_card_num = (card_to_numeric(hole_card[0]), card_to_numeric(hole_card[1]))
        if hole_card_num[0] == hole_card_num[1] or (hole_card_num[0] >= 10 and hole_card_num[1] >= 10):
            return 'raise', valid_actions[2]['amount']['max']

        return 'fold', 0

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return AOFPlayer()
