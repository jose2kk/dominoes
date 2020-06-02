from domino import Domino


class Hand:

    def __init__(self):
        self.dominoes = list()

    @property
    def points(self) -> int:
        return sum([domino.points for domino in self.dominoes])

    def empty(self) -> bool:
        return self.dominoes.__len__() == 0

    def add(self, domino: Domino) -> None:
        self.dominoes.append(domino)

    def uniques(self) -> set:
        uniques = set()
        for domino in self.dominoes:
            uniques.add(domino.left)
            uniques.add(domino.right)
            if len(uniques) == 7:
                break
        return uniques

    def remove(self, domino: Domino) -> None:
        self.dominoes.pop(self.dominoes.index(domino))

    def has_domino(self, ends: tuple()) -> bool:
        return self.uniques().intersection(set(ends)).__len__() > 0

    def has_double_six(self) -> bool:
        return any([domino.is_double_six() for domino in self.dominoes])

    def restart_hand(self) -> None:
        self.dominoes = list()

    def __str__(self) -> str:
        return ' : '.join([str(domino) for domino in self.dominoes])

    def __repr__(self) -> str:
        return str(self)
