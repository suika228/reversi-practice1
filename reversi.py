from literal_types import Type
from game import Game


class Reversi:
    players: dict[Type.PLAYER, str] = {"X": "黒", "O": "白"}

    def __init__(self, board):
        self.game = Game()
        self.board = board

    def __input_coordinate(self, player: Type.PLAYER) -> None:
        while True:
            try:
                x_key = input("X座標 (a-h): ")
                x = self.board.X_LINES[x_key]
                y = int(input("Y座標 (1-8): ")) - 1
                if not 0 <= y <= 7:
                    raise ValueError

                if self.board.can_put_stone(x, y, player):
                    self.board.put_stone(x, y, player)
                    self.board.flip_stones(x, y, player)
                    break

                print("置けません")
            except KeyError:
                print("無効なX座標です。やり直してください。")
            except ValueError:
                print("無効なY座標です。やり直してください。")

    def start(self) -> None:
        was_prev_turn_skipped = False
        while True:
            self.game.switch_player()
            player = self.game.player
            self.board.update_puttable_places(player)

            if not self.board.has_place():
                if was_prev_turn_skipped:
                    break
                was_prev_turn_skipped = True
                print("スキップ")
                continue

            was_prev_turn_skipped = False
            self.board.draw()
            print(f"{self.players.get(player)}のターンです")
            self.__input_coordinate(player)

    def end(self) -> None:
        black_count = self.board.count_stones("X")
        white_count = self.board.count_stones("O")
        self.board.draw()
        print("終わり")
        print(f"黒の数は{black_count}、白の数は{white_count}")
        if black_count > white_count:
            print("黒の勝ちです")
        elif white_count > black_count:
            print("白の勝ちです")
        else:
            print("引き分けです")
