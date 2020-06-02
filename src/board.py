from domino import Domino


class Board:

    def __init__(self):
        self.board = list()
        self.dominoes_on_board = set()
        self.left = None
        self.right = None

    def _add_first(self, domino: Domino) -> None:
        self.board.append(domino)
        self.right = self.board[-1].right
        self.left = self.board[0].left

    def _add_right(self, domino: Domino) -> None:
        if not domino.left == self.right:
            domino.flip()
        self.board += [domino]
        self.right = self.board[-1].right

    def _add_left(self, domino: Domino) -> None:
        if not domino.right == self.left:
            domino.flip()
        self.board = [domino] + self.board
        self.left = self.board[0].left

    def add_domino(self, domino: Domino) -> bool:
        if self.board:
            if self.right in domino or self.left in domino:
                if self.right in domino and self.left in domino:
                    end = 'r'
                    if not self.right == self.left:
                        message = '[r|R] for right, other would be left: '
                        end = input(message).lower()
                    if end == 'r':
                        self._add_right(domino=domino)
                    else:
                        self._add_left(domino=domino)
                elif self.right in domino:
                    self._add_right(domino=domino)
                elif self.left in domino:
                    self._add_left(domino=domino)
                self.dominoes_on_board.add(domino)
                return True
            return False
        self._add_first(domino=domino)
        self.dominoes_on_board.add(domino)
        return True

    def current_ends(self) -> tuple:
        return (self.left, self.right)

    def __str__(self) -> str:
        return str(self.board)

    def __repr__(self) -> str:
        return str(self)

    def __contains__(self, domino: Domino) -> bool:
        return domino in self.board