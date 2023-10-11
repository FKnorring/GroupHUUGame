from typing import List, Tuple, Union
from constants import *


def generateBoard(size: int) -> List[List[str]]:
    return [[EMPTY] * size for _ in range(size)]


class Game:
    def __init__(self, size=8, pieces=9) -> None:
        self.size = size
        self.board = generateBoard(size)
        self.hands = {"WHITE": pieces, "BLACK": pieces}
        self.pieces = {"WHITE": pieces, "BLACK": pieces}
        self.phase = {"WHITE": PLACING, "BLACK": PLACING}
        self.mils = {"WHITE": [], "BLACK": []}
        self.state = PLAYING
        self.turn = "WHITE"
        self.turns = 0

    def isValidMove(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> bool:
        if not self.isWithinBoard(coord1) or not self.isWithinBoard(coord2):
            return False

        if not self.isEmptySquare(coord2):
            return False

        if self.phase[self.turn] == MOVING:
            if not self.isAdjacentSquare(coord1, coord2):
                return False

        if not self.isPieceOfSameColor(coord1) and self.phase[self.turn] != PLACING:
            return False

        return True

    def makeMove(
        self, coord1: Tuple[int, int], coord2: Tuple[int, int]
    ) -> Union[bool, List[List[Tuple[int, int]]]]:
        if not self.isValidMove(coord1, coord2):
            return False

        mils = None

        if self.phase[self.turn] == PLACING:
            self.placePiece(coord2)
            self.hands[self.turn] -= 1
            if self.hands[self.turn] == 0:
                self.phase[self.turn] = MOVING
            mils = self.createdMils(coord2)
        else:
            if self.isPieceInMil(coord1):
                self.removeMil(coord1)
            self.removePiece(coord1)
            self.placePiece(coord2)
            mils = self.createdMils(coord2)

        return True if mils == None else mils

    def createMil(self, mil: List[Tuple[int, int]], toRemove: Tuple[int, int]) -> bool:
        if (
            self.isPieceOfSameColor(toRemove)
            or self.isPieceInMil(toRemove)
            or self.isEmptySquare(toRemove)
        ):
            return False

        self.placeMil(mil)
        self.mils[self.turn].append(mil)
        self.pieces["BLACK" if self.turn == "WHITE" else "WHITE"] -= 1
        self.removePiece(toRemove)

        return True

    def isWithinBoard(self, coord: Tuple[int, int]) -> bool:
        x, y = coord
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def isEmptySquare(self, coord: Tuple[int, int]) -> bool:
        x, y = coord
        return self.board[x][y] == EMPTY

    def isAdjacentSquare(
        self, coord1: Tuple[int, int], coord2: Tuple[int, int]
    ) -> bool:
        x1, y1 = coord1
        x2, y2 = coord2
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def isPieceOfSameColor(self, coord: Tuple[int, int]) -> bool:
        x, y = coord
        if self.turn == "WHITE":
            return self.board[x][y] in [WHITE, WHITE_MIL]
        else:
            return self.board[x][y] in [BLACK, BLACK_MIL]

    def isPieceInMil(self, coord: Tuple[int, int]) -> bool:
        x, y = coord
        return self.board[x][y] in [WHITE_MIL, BLACK_MIL]

    def placeMil(self, mil: List[Tuple[int, int]]) -> None:
        piece = WHITE_MIL if self.turn == "WHITE" else BLACK_MIL
        for x, y in mil:
            self.board[x][y] = piece

    def removeMil(self, coord: Tuple[int, int]) -> None:
        piece = WHITE if self.turn == "WHITE" else BLACK
        mil = None
        milIndex = None
        for i, m in enumerate(self.mils[self.turn]):
            if coord in m:
                mil = m
                milIndex = i
                break
        else:
            return

        for x, y in mil:
            self.board[x][y] = piece

        self.mils[self.turn].pop(milIndex)

    def placePiece(self, coord: Tuple[int, int]) -> None:
        x, y = coord
        self.board[x][y] = WHITE if self.turn == "WHITE" else BLACK

    def removePiece(self, coord: Tuple[int, int]) -> None:
        x, y = coord
        self.board[x][y] = EMPTY

    def switchTurn(self) -> None:
        self.turn = "WHITE" if self.turn == "BLACK" else "BLACK"
        self.turns += 1

    def createdMils(
        self, coord: Tuple[int, int]
    ) -> Union[None, List[List[Tuple[int, int]]]]:
        piece = WHITE if self.turn == "WHITE" else BLACK
        mils = []
        x, y = coord

        # Check horizontally
        for i in range(-2, 1):
            if 0 <= y + i < self.size - 2 and all(
                self.board[x][y + j] == piece for j in range(i, i + 3)
            ):
                mils.append([(x, y + j) for j in range(i, i + 3)])

        # Check vertically
        for i in range(-2, 1):
            if 0 <= x + i < self.size - 2 and all(
                self.board[x + j][y] == piece for j in range(i, i + 3)
            ):
                mils.append([(x + j, y) for j in range(i, i + 3)])

        return mils if mils else None

    def printBoard(self) -> None:
        print(f"  {' '.join([str(i+1) for i in range(self.size)])}")
        for i, row in enumerate(self.board):
            print(f"{chr(i + ord('a'))} {' '.join(row)}")

    def getValidMoves(self) -> List[Tuple[int, int]]:
        phase = self.phase[self.turn]
        moves = []
        if phase == PLACING:
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == EMPTY:
                        moves.append(((0, 0), (i, j)))
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == WHITE if self.turn == "WHITE" else BLACK:
                        for x in range(i - 1, i + 2):
                            for y in range(j - 1, j + 2):
                                if self.isValidMove((i, j), (x, y)):
                                    moves.append(((i, j), (x, y)))
        return moves

    def getRemovablePieces(self, color) -> List[Tuple[int, int]]:
        pieces = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == color and not self.isPieceInMil((i, j)):
                    pieces.append((i, j))
        return pieces
