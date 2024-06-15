from game.players import BasePokerPlayer

class AllinPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        return 'raise', valid_actions[2]['amount']['max']

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
    return AllinPlayer()

