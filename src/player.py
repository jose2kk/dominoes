from domino import Domino
from hand import Hand


class Player:

    def __init__(self, identity: int):
        self.identity = identity
        self.hand = None

    @property
    def points(self) -> int:
        return hand.points if self.hand else None
    
    def update_hand(self, domino: Domino) -> None:
        self.hand.remove(domino)

    def empty_hand(self) -> bool:
        return self.hand.empty()

    def __str__(self) -> str:
        return f'''
            identity: {str(self.identity)}
            hand: {str(self.hand)}
            '''

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.identity == other.identity

# if __name__ == "__main__":
#     p = Player(1)
#     print(p.points)