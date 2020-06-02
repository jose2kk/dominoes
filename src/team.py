from player import Player


# ASK ENAMNUEL AND JOHN CROSS ABOUT SELF.POINTS PROPERTY 
# WHICH I THINK COULD BE IMPLEMENTED DIFFERENTLY


class Team:
    
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.points = 0

    def __str__(self) -> str:
        return f'''
            Player1: {self.player1}
            Player2: {self.player2}
            '''

    def __repr__(self) -> str:
        return str(self)

    def __contains__(self, player: Player) -> bool:
        return player in (self.player1, self.player2)

    def __eq__(self, other) -> bool:
        return self.player1 == other.player1
