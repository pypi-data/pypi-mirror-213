from abc import ABC, abstractmethod, abstractstaticmethod
from .environment import Environment
from .agent import Agent

class GameEnvironment(Environment):

    def __init__(self, environment_name):
        super().__init__(environment_name)

        self._players = {}
    
    def add_player(self, player):
        assert isinstance(player, Agent), "A player must be an instance of an Agent subclass."

        player_name = player.who_am_I()
        self._players[player_name] = player

        return player_name
    
    @abstractmethod
    def get_game_state(self):
        pass

    @abstractstaticmethod
    def get_legal_actions(game_state):
        pass

    @abstractstaticmethod
    def is_terminal(game_state):
        pass

    @abstractstaticmethod
    def transition_result(game_state, action):
        pass

    @abstractstaticmethod
    def turn(game_state):
        pass

    @abstractstaticmethod
    def payoff(game_state, player_name):
        pass