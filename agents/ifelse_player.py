from game.players import BasePokerPlayer
from game.engine.hand_evaluator import HandEvaluator
from game.engine.card import Card

def card_to_numeric(card):
    value = card[1:]
    value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    if value in value_dict:
        value = value_dict[value]

    else:
        value = int(value)

    return value

class IfelsePlayer(BasePokerPlayer):
    def __init__(self):
        self.br = 1000
        self.state = None

    def declare_action(self, valid_actions, hole_card, round_state):
        hole_num = (card_to_numeric(hole_card[0]), card_to_numeric(hole_card[1]))
        pot = round_state['pot']['main']['amount']
        raise_amount = valid_actions[2]['amount']['max']
        call_amount = valid_actions[1]['amount']

        if self.state == 'WIN':
            return 'fold', 0

        if round_state['street'] == 'preflop':
            if hole_num[0] == hole_num[1] or min(hole_num[0], hole_num[1]) >= min(10 , self.round - self.current_round + (self.br - 1001) // 50 + 1):
                if raise_amount == -1:
                    return 'call', call_amount

                return 'raise', raise_amount

            if min(hole_num[0], hole_num[1]) <= 5:
                if call_amount == 0:
                    return 'call', 0

                return 'fold', 0

            if call_amount <= self.blind * 6:
                return 'call', call_amount
            
            return 'fold', 0

        else:
            hole = [Card.from_str(card) for card in hole_card]
            community = [Card.from_str(card) for card in round_state['community_card']]
            evaluation = HandEvaluator.gen_hand_rank_info(hole, community)
            print(evaluation)
            strength = evaluation['hand']['strength']
            hand_high = evaluation['hand']['high']
            hand_low = evaluation['hand']['low']
            hole_high = evaluation['hole']['high']
            hole_low = evaluation['hole']['low']

            if strength in ['STRAIGHT', 'FLASH', 'FULLHOUSE', 'FOURCARD', 'STRAIGHTFLASH']:
                if raise_amount == -1:
                    return 'call', call_amount

                return 'raise', min(raise_amount, pot * 3)

            else:
                if hand_high == hole_high or hand_high == hole_low:
                    if strength == 'THREECARD':
                        if raise_amount == -1:
                            return 'call', call_amount
                        return 'raise', min(raise_amount, pot * 2)

                    if strength == 'TWOPAIR':
                        if hand_high + hand_low >= 20:
                            if raise_amount == -1:
                                return 'call', call_amount
                            return 'raise', min(raise_amount, pot)

                    if strength == 'ONEPAIR':
                        if hand_high >= 13:
                            return 'call', call_amount

                if hole_high == hole_low:
                    return 'call', call_amount 
                
                if call_amount == 0:
                    return 'call', 0

                return 'fold', 0

    def receive_game_start_message(self, game_info):
        self.player_num = game_info['player_num']
        self.stack = game_info['rule']['initial_stack']
        self.round = game_info['rule']['max_round']
        self.blind = game_info['rule']['small_blind_amount']

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.current_round = round_count
        
        print(self.br)
        if (self.round - self.current_round) % 2 == 0:
            if self.br - self.blind * (3 * (self.round - self.current_round) / 2) >= self.stack * self.player_num / 2:
                self.state = 'WIN'
        else:
            if self.br - self.blind * (3 * (self.round - self.current_round) // 2 + 2) >= self.stack * self.player_num / 2:
                self.state = 'WIN'

    def receive_street_start_message(self, street, round_state):
        for player in round_state['seats']:
            if player['name'] == 'Ifelse':
                self.br = player['stack']

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return IfelsePlayer()

