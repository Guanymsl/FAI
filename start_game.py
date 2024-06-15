import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
from agents.allin_player import setup_ai as allin_ai
from agents.aof_player import setup_ai as aof_ai
from agents.ifelse_player import setup_ai as ifelse_ai
from agents.sklearn_player import setup_ai as sklearn_ai
from agents.qlearning_player import setup_ai as qlearning_ai
from agents.monte import setup_ai as monte_ai

from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai

iterations = 10
win = []
for num in range(1, 8):
    cnt = 0
    for _ in range(iterations):
        config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
        if num == 1:
            config.register_player(name="Baseline1", algorithm=baseline1_ai())
        if num == 2:
            config.register_player(name="Baseline2", algorithm=baseline2_ai())
        if num == 3:
            config.register_player(name="Baseline3", algorithm=baseline3_ai())
        if num == 4:
            config.register_player(name="Baseline4", algorithm=baseline4_ai())
        if num == 5:
            config.register_player(name="Baseline5", algorithm=baseline5_ai())
        if num == 6:
            config.register_player(name="Baseline6", algorithm=baseline6_ai())
        if num == 7:
            config.register_player(name="Baseline7", algorithm=baseline7_ai())

        #config.register_player(name="Allin", algorithm=allin_ai())
        #config.register_player(name="AOF", algorithm=aof_ai())
        #config.register_player(name="Ifelse", algorithm=ifelse_ai())
        #config.register_player(name="Sklearn", algorithm=sklearn_ai())
        #config.register_player(name="Qlearning", algorithm=qlearning_ai())
        config.register_player(name="Monte", algorithm=monte_ai())
    
        game_result = start_poker(config)
        for player in game_result['players']:
            if player['name'] == 'Monte' and player['stack'] > 1000:
                cnt += 1

    win.append(cnt)

for i in range(len(win)):
    print(f"Baseline{i + 1}: {win[i]} / {iterations}")
