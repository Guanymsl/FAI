from game.players import BasePokerPlayer
from game.engine.hand_evaluator import HandEvaluator
from game.engine.card import Card
import random

strength_to_rank = {

    "HIGHCARD": 0,
    "ONEPAIR": 1,
    "TWOPAIR": 2,
    "THREECARD": 3,
    "STRAIGHT": 4,
    "FLASH": 5,
    "FULLHOUSE": 6,
    "FOURCARD": 7,
    "STRAIGHTFLASH": 8

}

def card_to_numeric(card):
    value = card[1:]
    value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    if value in value_dict:
        value = value_dict[value]
    else:
        value = int(value)

    return value

class MontePlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        street = round_state['street']

        if street == 'preflop':
            return self.gto(valid_actions, hole_card, round_state)
        else:
            return self.monte_carlo(valid_actions, hole_card, round_state)

    def gto(self, valid_actions, hole_card, round_state):
        hole_num = (card_to_numeric(hole_card[0]), card_to_numeric(hole_card[1]))
        raise_amount = valid_actions[2]['amount']['max']
        call_amount = valid_actions[1]['amount']

        if hole_num[0] == hole_num[1] or min(hole_num[0], hole_num[1]) >= 10:
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

    def monte_carlo(self, valid_actions, hole_card, round_state):
        raise_amount = valid_actions[2]['amount']['max']
        call_amount = valid_actions[1]['amount']

        win_prob = self.monte_carlo_simulation(hole_card, round_state['community_card'], iterations=100)
        
        if win_prob > 0.7:
            if raise_amount == -1:
                return 'call', call_amount

            return 'raise', min(raise_amount, round_state['pot']['main']['amount'] * 3)

        if win_prob > 0.4:
            return 'call', call_amount
        
        if call_amount == 0:
            return 'call', 0

        return 'fold', 0

    def monte_carlo_simulation(self, hole_card, community_card, iterations=100):
        win_count = 0
        for _ in range(iterations):
            remaining_deck = [suit + rank for rank in '23456789TJQKA' for suit in 'CDHS']
            for card in hole_card + community_card:
                remaining_deck.remove(card)

            opponent_hole_card = random.sample(remaining_deck, 2)
            remaining_deck = [card for card in remaining_deck if card not in opponent_hole_card]
            rest_community_card = random.sample(remaining_deck, 5 - len(community_card))

            hole = [Card.from_str(card) for card in hole_card]
            opponent_hole = [Card.from_str(card) for card in opponent_hole_card]
            community = [Card.from_str(card) for card in community_card + rest_community_card]

            my_best_hand = HandEvaluator.gen_hand_rank_info(hole, community)['hand']['strength']
            opponent_best_hand = HandEvaluator.gen_hand_rank_info(opponent_hole, community)['hand']['strength']
            me = strength_to_rank[my_best_hand]
            you = strength_to_rank[opponent_best_hand]
            
            if me >= you:
                win_count += 1

        return win_count / iterations

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
    return MontePlayer()

