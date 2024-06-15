import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from game.players import BasePokerPlayer

def card_to_numeric(card):
    if isinstance(card, str):
        suit = card[0]
        value = card[1:]
        suit_dict = {'S': 1, 'H': 2, 'D': 3, 'C': 4}
        value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        if value in value_dict:
            value = value_dict[value]
        else:
            value = int(value)
        return suit_dict[suit] * 100 + value
    elif card is None:
        return 0
    else:
        return card

class SklearnPlayer(BasePokerPlayer):
    def __init__(self):
        df = pd.read_csv("./data/simple_data.csv")

        for col in ['hole_card_high', 'hole_card_low', 'community_card_1', 'community_card_2', 'community_card_3', 'community_card_4', 'community_card_5']:
            df[col] = df[col].apply(card_to_numeric)

        self.le_street = LabelEncoder()
        self.le_action = LabelEncoder()
        df['street'] = self.le_street.fit_transform(df['street'])
        df['action'] = self.le_action.fit_transform(df['action'])
        df = df.fillna(0)

        X = df.drop(columns=['action'])
        y = df['action']

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def declare_action(self, valid_actions, hole_card, round_state):
        data = []

        community_card = round_state['community_card']

        street = round_state['street']
        info = {
            "street": street,
            "hole_card_high": max(card_to_numeric(hole_card[0]) % 100, card_to_numeric(hole_card[1]) % 100),
            "hole_card_low": min(card_to_numeric(hole_card[0]) % 100, card_to_numeric(hole_card[1]) % 100),
            "community_card_1": community_card[0] if street != 'preflop' else None,
            "community_card_2": community_card[1] if street != 'preflop' else None,
            "community_card_3": community_card[2] if street != 'preflop' else None,
            "community_card_4": community_card[3] if street in ['turn', 'river'] else None,
            "community_card_5": community_card[4] if street == 'river' else None,
        }
        data.append(info)
        df = pd.DataFrame(data)

        for col in ['hole_card_high', 'hole_card_low', 'community_card_1', 'community_card_2', 'community_card_3', 'community_card_4', 'community_card_5']:
            df[col] = df[col].apply(card_to_numeric)

        df['street'] = self.le_street.fit_transform(df['street'])

        df = df.fillna(0)

        pred = self.model.predict(df)
        action = self.le_action.inverse_transform(pred)
        if action == 'FOLD':
            return 'fold', 0
        elif action == 'CALL':
            return 'call', valid_actions[1]["amount"]
        else:
            return 'raise', valid_actions[2]['amount']['min'] 

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
    return SklearnPlayer()

