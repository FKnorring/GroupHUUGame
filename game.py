from typing import List, Tuple, Union
from constants import EMPTY, WHITE, WHITE_MIL, WHITE_WIN, BLACK, BLACK_MIL, BLACK_WIN, PLACING, MOVING, FLYING, PLAYING, TIE

def generateBoard(size: int) -> List[List[str]]:
  return [[EMPTY] * size for _ in range(size)]


class Game():
  def __init__(self, size = 8, pieces = 9, difficulty = "EASY") -> None:
    self.size = size
    self.board = generateBoard(size)
    self.hands = { "WHITE": pieces, "BLACK": pieces }
    self.pieces = { "WHITE": pieces, "BLACK": pieces }
    self.phase = { "WHITE": PLACING, "BLACK": PLACING }
    self.state = PLAYING
    self.turn = "WHITE"
    self.turns = 0
    self.ai = AI(difficulty)

  def isValidMove(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> bool:
    pass

  def makeMove(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> Union[None, List[List[Tuple[int, int]]]]:
    pass

  def createMil(self, mil: List[Tuple[int, int]], toRemove: Tuple[int, int]) -> bool:
    pass

  def isWithinBoard(self, coord: Tuple[int, int]) -> bool:
    x, y = coord
    return x >= 0 and x < self.size and y >= 0 and y < self.size

  def isEmptySquare(self, coord: Tuple[int, int]) -> bool:
    x, y = coord
    return self.board[x][y] == EMPTY

  def isAdjacentSquare(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> bool:
    pass

  def isMoveBreakingMil(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> bool:
    pass

  def isPieceInMil(self, coord: Tuple[int, int]) -> bool:
    pass

  def placeMil(self, milStart: Tuple[int, int], milEnd: Tuple[int, int]) -> None:
    pass

  def removeMil(self, milStart: Tuple[int, int], milEnd: Tuple[int, int]) -> None:
    pass

  def placePiece(self, coord: Tuple[int, int]) -> None:
    pass

  def removePiece(self, coord: Tuple[int, int]) -> None:
    pass

  

class AI():
  pass