from board import Board
from reversi import Reversi


if __name__ == "__main__":
    board = Board()
    reversi = Reversi(board=board)
    reversi.start()
    reversi.end()
