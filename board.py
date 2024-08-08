from typing import List

from literal_types import Type


class Board:
    _DIRECTIONS = (
        (0, 1),
        (0, -1),
        (1, 1),
        (1, 0),
        (1, -1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
    )

    X_LINES = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    def __init__(self) -> None:
        self.board: List[List[Type.CELL]] = [[" " for _ in range(8)] for _ in range(8)]
        self.board[4][3] = self.board[3][4] = "X"
        self.board[3][3] = self.board[4][4] = "O"
        self.puttable_places = []
        self.x_lines_rev = {v: k for k, v in self.X_LINES.items()}

    def __is_xy_within_board_range(self, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    def __is_self_stone(self, x: int, y: int, player: Type.PLAYER) -> bool:
        return self.board[x][y] == player

    def __is_empty_place(self, x: int, y: int) -> bool:
        return self.board[x][y] == " " or self.board[x][y] == "A"

    def get(self) -> List[List[Type.CELL]]:
        return self.board

    def draw(self) -> None:
        column_headers = " ".join(self.X_LINES.keys())
        print("  ", column_headers)

        for y in range(8):
            print(f"{y + 1} |", end="")
            for x in range(8):
                print(f"{self.board[x][y]}|", end="")
            print()

        print(f"おける場所：{self.puttable_places}")

    def put_stone(self, x: int, y: int, player: Type.PLAYER) -> None:
        self.board[x][y] = player

    def can_put_stone(self, x: int, y: int, player: Type.PLAYER) -> bool:
        if not self.__is_empty_place(x, y):
            return False

        for dx, dy in self._DIRECTIONS:
            around_x, around_y = x + dx, y + dy
            if self.__is_xy_within_board_range(
                around_x, around_y
            ) and not self.__is_self_stone(around_x, around_y, player):
                while self.__is_xy_within_board_range(around_x, around_y):
                    if self.__is_empty_place(around_x, around_y):
                        break
                    if self.__is_self_stone(around_x, around_y, player):
                        return True
                    around_x += dx
                    around_y += dy
        return False

    def update_puttable_places(self, player: Type.PLAYER) -> None:
        self.puttable_places = []
        for y in range(8):
            for x in range(8):
                if self.board[x][y] == "A":
                    self.board[x][y] = " "
                if self.can_put_stone(x, y, player):
                    self.board[x][y] = "A"
                    new_puttable_place = (self.x_lines_rev.get(x), y + 1)
                    self.puttable_places.append(new_puttable_place)

    def flip_stones(self, x: int, y: int, player: Type.PLAYER) -> None:
        for dx, dy in self._DIRECTIONS:
            around_x, around_y = x + dx, y + dy
            flip_squares = set()

            while self.__is_xy_within_board_range(around_x, around_y):
                if self.__is_empty_place(around_x, around_y):
                    break
                if self.__is_self_stone(around_x, around_y, player):
                    for fx, fy in flip_squares:
                        self.board[fx][fy] = player
                    break
                flip_squares.add((around_x, around_y))
                around_x += dx
                around_y += dy

    def has_place(self) -> bool:
        return bool(self.puttable_places)

    def count_stones(self, player: Type.PLAYER) -> int:
        return sum(row.count(player) for row in self.board)
