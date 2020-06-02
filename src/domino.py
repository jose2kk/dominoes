

class Domino:

    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    @property
    def points(self):
        return self.left + self.right

    def flip(self) -> None:
        self.left, self.right = self.right, self.left

    def is_double_six(self) -> bool:
        return self.left == 6 and self.right == 6

    def __str__(self) -> str:
        return f'[{self.left}|{self.right}]'

    def __repr__(self) -> str:
        return str(self)

    def __contains__(self, val: int) -> bool:
        return val in (self.left, self.right)
