import random

from collections import namedtuple

from board import Board
from domino import Domino
from hand import Hand
from player import Player
from team import Team

class Game:

    Information = namedtuple('Information', 'winner team points starter')

    def __init__(self, players: list, team_one: Team, team_two: Team, 
                number: int = 1, starter: int = None):
        self.players = players
        self.board = Board()
        self.number = number
        self.starter = starter
        self.turn = starter
        self.subgame_str = list()
        self.moves = 0
        self.info = None
        self.dominoes_unused = set()
        self.stuck = False
        self.team_one = team_one
        self.team_two = team_two
        self.winners = True

    def run(self) -> dict():
        self._draw_dominoes()
        if self.starter is None:
            for player in self.players:
                if player.hand.has_double_six():
                    self.turn = player.identity
                    self.starter = player.identity
                    break
        while True:
            print("=" * 50)
            self._print_player_view(self.turn)
            if not self._move():
                print(f'Player {self.turn} passes.\n')
            self._save_step()
            if self._subgame_over():
                self._save_step()
                self._ending()
                return self.info
            if self.turn + 1 == 4:
                self.turn -= 4
            self.turn += 1

    @staticmethod
    def _dominoes_shuffle() -> list:
        dominoes = [
            Domino(left=i, right=j) 
            for i in range(7) 
            for j in range(i, 7)
            ]
        random.shuffle(dominoes)
        return dominoes

    def _draw_dominoes(self):
        dominoes = self._dominoes_shuffle()
        for i in range(4):
            hand = Hand()
            for j in range(7*i, 7*(i+1)):
                hand.add(dominoes[j])
                self.dominoes_unused.add(dominoes[j])
            self.players[i].hand = hand

    def _move(self) -> bool:
        player = self.players[self.turn]
        hand = player.hand
        if hand.has_domino(self.board.current_ends()) or self.moves == 0:
            self._put_domino(hand)
            self.moves += 1
            return True
        return False

    def _put_domino(self, hand: Hand) -> None:
        print(f'Player {self.turn} turn.')
        message = 'Please enter which domino you want to put: '
        while True:
            try:
                indx = int(input(message)) - 1
                domino = hand.dominoes[indx]
                if self.board.add_domino(domino=domino):
                    hand.remove(domino)
                    self.dominoes_unused.remove(domino)
                    break
                message = 'That is not a valid option. Reenter the position: '
            except IndexError as e:
                message = f'Position must be a number in (1,{len(hand.dominoes)})'

    def _subgame_over(self) -> bool:
        return (any([player.empty_hand() for player in self.players]) \
            or self._stuck_subgame()) and self.moves > 0

    def _stuck_subgame(self) -> bool:
        self.stuck = set(self.board.current_ends())\
            .intersection(self._dominoes_unused()).__len__() == 0
        return self.stuck

    def _dominoes_unused(self) -> set:
        dominoes_unused = set()
        for domino in self.dominoes_unused:
            dominoes_unused.add(domino.left)
            dominoes_unused.add(domino.right)
            if len(dominoes_unused) == 7:
                break
        return dominoes_unused

    def _ending(self) -> None:
        if not self.stuck:
            if self.players[self.turn] in self.team_one:
                winners = self.team_one
                losers = self.team_two
            elif self.players[self.turn] in self.team_two:
                winners = self.team_two
                losers = self.team_one
            points = self._team_points(team=losers)
            self._set_info_message(
                winner=self.turn,
                team=winners,
                points=points)
        else:
            points_team1 = self._team_points(self.team_one)
            points_team2 = self._team_points(self.team_two)
            if points_team1 > points_team2:
                self._set_info_message(winner=None, 
                                        team=self.team_two, 
                                        points=points_team1)
            elif points_team2 > points_team1:
                self._set_info_message(winner=None, 
                                        team=self.team_one, 
                                        points=points_team2)
            elif points_team1 == points_team2:
                self._set_info_message(winner=None,
                                        team=None,
                                        points=None)

    def _team_points(self, team: Team) -> int:
        return sum([player.hand.points 
                    for player in self.players if player in team])

    def _set_info_message(self, winner: int = None, team: Team = None, 
                            points: int = None) -> None:
        self.info = self.Information(winner=winner, team=team, 
                                    points=points, starter=self.starter)

    def _print_player_view(self, player_id: int) -> None:
        print(f'''
            Board:
                {self.board}
            Player: {self.players[player_id]}
            ''')

    def _save_step(self) -> None:
        step = f'''
            ====================== MOVE {self.moves} ======================

            Board:
            {str(self.board)}

            Player info:
            {str(self.players)}

            '''
        self.subgame_str.append(step)

    def __str__(self) -> str:
        return '\n'.join(self.subgame_str)

    def __repr__(self) -> str:
        return str(self)

if __name__ == "__main__":
    players = [Player(identity=i) for i in range(4)]
    team_one = Team(player1=players[0], player2=players[2])
    team_two = Team(player1=players[1], player2=players[3])
    game = Game(players=players, team_one=team_one, team_two=team_two)
    info = game.run()
    print('--' * 50)
    print(info)