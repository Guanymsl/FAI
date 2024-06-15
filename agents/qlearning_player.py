import random
import os
import json
from game.players import BasePokerPlayer

ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1

Q_TABLE = {}
Q_TABLE_FILE = 'q_table.json'

def load_q_table():
    global Q_TABLE
    if os.path.exists(Q_TABLE_FILE):
        try:
            with open(Q_TABLE_FILE, 'r') as f:
                loaded_q_table = json.load(f)
                Q_TABLE = {tuple(tuple(x) if isinstance(x, list) else x for x in json.loads(k)): v for k, v in loaded_q_table.items()}
            print("Q-table loaded from file.")
        except (json.JSONDecodeError, SyntaxError) as e:
            print(f"Error loading Q-table: {e}")
            Q_TABLE = {}

def save_q_table():
    try:
        with open(Q_TABLE_FILE, 'w') as f:
            saveable_q_table = {json.dumps(k): v for k, v in Q_TABLE.items()}
            json.dump(saveable_q_table, f)
        print("Q-table saved to file.")
    except Exception as e:
        print(f"Error saving Q-table: {e}")

class QLearningPlayer(BasePokerPlayer):
    def __init__(self):
        super().__init__()
        self.last_state = None
        self.last_action = None
        self.hole_card = None

    def declare_action(self, valid_actions, hole_card, round_state):
        state = self.get_state(hole_card, round_state)
        action, amount = self.choose_action(state, valid_actions)
        self.last_state = state
        self.last_action = action
        return action, amount

    def choose_action(self, state, valid_actions):
        if random.random() < EPSILON:
            chosen_action = random.choice(valid_actions)
        else:
            q_values = [self.get_q_value(state, action['action']) for action in valid_actions]
            max_q_value = max(q_values)
            best_actions = [valid_actions[i] for i, q in enumerate(q_values) if q == max_q_value]
            chosen_action = random.choice(best_actions)

        action = chosen_action['action']
        amount = chosen_action['amount']['min'] 
        return action, amount

    def get_q_value(self, state, action):
        return Q_TABLE.get((state, action), 0)

    def update_q_table(self, reward, new_state):
        if self.last_state is not None and self.last_action is not None:
            old_q_value = self.get_q_value(self.last_state, self.last_action)
            future_rewards = [self.get_q_value(new_state, a) for a in ['fold', 'call', 'raise']]
            best_future_q = max(future_rewards, default=0)
            new_q_value = old_q_value + ALPHA * (reward + GAMMA * best_future_q - old_q_value)
            Q_TABLE[(self.last_state, self.last_action)] = new_q_value

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.hole_card = hole_card
        load_q_table()

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        reward = 1 if any(winner['uuid'] == self.uuid for winner in winners) else -1
        new_state = self.get_state(self.hole_card, round_state)
        self.update_q_table(reward, new_state)
        save_q_table()

    def get_state(self, hole_card, round_state):
        hole_card_str = ''.join(sorted(hole_card))
        community_card_str = ''.join(sorted(round_state['community_card']))
        street = round_state['street']
        pot = round_state['pot']['main']['amount']

        state = (hole_card_str, community_card_str, street, pot)
        return state

def setup_ai():
    return QLearningPlayer()

