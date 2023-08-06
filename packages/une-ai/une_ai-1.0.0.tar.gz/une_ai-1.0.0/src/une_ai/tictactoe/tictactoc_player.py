import numpy as np
from une_ai.models import Agent, GridMap
from .tictactoe_game_environment import TicTacToeGameEnvironment

class TicTacToePlayer(Agent):

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)
    
    def add_all_sensors(self):
        self.add_sensor(
            'game-board-sensor',
            GridMap(3, 3, None),
            lambda v: isinstance(v, GridMap) and v.get_height() == 3 and v.get_width() == 3
        )
    
    def add_all_actuators(self):
        self.add_actuator(
            'marker',
            None,
            TicTacToeGameEnvironment.VALID_BOX
        )
    
    def add_all_actions(self):
        valid_box = TicTacToeGameEnvironment.VALID_BOX
        for i in range(0, 3):
            for j in range(0, 3):
                self.add_action(
                    'mark-{0}-{1}'.format(i, j),
                    lambda r=i, c=j: {'marker': (r, c)} if valid_box((r, c)) else {}
                )