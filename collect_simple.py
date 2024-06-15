import json
import copy
import pandas as pd

from game.game import setup_config, start_poker
from baseline7 import setup_ai as baseline7_ai

from game.players import BasePokerPlayer
data = []
class CollectPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount 

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):

        winner = winners[0]["uuid"]

        hole_card = []
        for info in hand_info:
            if info["uuid"] == winner:
                hole_card.append(info["hand"]["hole"]["high"])
                hole_card.append(info["hand"]["hole"]["low"])

        if len(hole_card) == 0:
            return

        community_card = round_state["community_card"]

        player = []
        for seat in round_state["seats"]:
            player.append(seat["uuid"])

        for street in ['preflop', 'flop', 'turn', 'river']:
            if street in round_state["action_histories"]:
                for action in round_state["action_histories"][street]:
                    if action["uuid"] == winner and action["action"] not in ('SMALLBLIND', 'BIGBLIND'):
                        result = {
                            "street": street,
                            "hole_card_high": hole_card[0],
                            "hole_card_low": hole_card[1],
                            "community_card_1": community_card[0] if street != 'preflop' else None,
                            "community_card_2": community_card[1] if street != 'preflop' else None,
                            "community_card_3": community_card[2] if street != 'preflop' else None,
                            "community_card_4": community_card[3] if street in ['turn', 'river'] else None,
                            "community_card_5": community_card[4] if street == 'river' else None,
                            "action": action["action"]
                        }
                        data.append(result)

collect_ai = CollectPlayer()

config = setup_config(max_round=200, initial_stack=1000, small_blind_amount=5)
config.register_player(name="baseline7-1", algorithm=baseline7_ai())
config.register_player(name="baseline7-2", algorithm=baseline7_ai())
config.register_player(name="baseline7-3", algorithm=baseline7_ai())
config.register_player(name="baseline7-4", algorithm=baseline7_ai())
config.register_player(name="baseline7-5", algorithm=baseline7_ai())
config.register_player(name="collector", algorithm=collect_ai)

game_result = start_poker(config, verbose=1)

df = pd.DataFrame(data)
df.to_csv("./data/simple_data.csv", index=False)

print(json.dumps(game_result, indent=4))

