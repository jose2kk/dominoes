import copy
import itertools
import random

from collections import namedtuple

from game import Game
from player import Player
from team import Team


class Round:

    RoundInformation = namedtuple('RoundInformation', 'winner score')

    def __init__(self, target_score: int = 100, turn: int = None):
        self.target_score = target_score
        self.players = self._init_players()
        self.team_one = Team(player1=self.players[0], player2=self.players[2])
        self.team_two = Team(player1=self.players[1], player2=self.players[3])
        self.turn = turn
        self.games = 0
        self.games_played = list()

    def run(self) -> None:
        while not self.game_over():
            self.games += 1
            game = Game(players=self.players, 
                        team_one=self.team_one, 
                        team_two=self.team_two, 
                        number=self.games,
                        starter=self.turn)
            info = game.run()
            if not info.team is None:
                self.process_game_result(game=game, info=info)
            self.turn = info.starter + 1 if info.starter < 3 else 0

    def game_over(self) -> bool:
        return max(self.team_one.points, self.team_two.points) >= self.target_score
    
    def get_winner(self) -> str:
        if self.team_one.points > self.team_two.points:
            return self.team_one
        return self.team_two

    def process_game_result(self, game: Game, info: namedtuple) -> None:
        if info.team == self.team_one:
            self.team_one.points += info.points
        elif info.team == self.team_two:
            self.team_two.points += info.points
        self._save_game(game=game)

    def _init_players(self) -> list:
        return [Player(identity=i) for i in range(4)]

    def _save_game(self, game: Game) -> None:
        self.games_played.append(game)

    def __str__(self) -> str:
        return f'''Something here.'''

    def __repr__(self) -> str:
        return str(self)

    def __contains__(self) -> bool:
        pass

if __name__ == "__main__":
    r = Round()
    r.run()