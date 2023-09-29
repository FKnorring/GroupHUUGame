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
    self.mils = { "WHITE": [], "BLACK": []}
    self.state = PLAYING
    self.turn = "WHITE"
    self.turns = 0
    self.ai = AI(difficulty)

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

  def makeMove(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> Union[bool, List[List[Tuple[int, int]]]]:
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
    if self.isPieceOfSameColor(toRemove) or self.isPieceInMil(toRemove) or self.isEmptySquare(toRemove):
      return False
    
    self.placeMil(mil)
    self.mils[self.turn].append(mil)
    self.pieces[self.turn] -= 1
    self.removePiece(toRemove)

    return True

  def isWithinBoard(self, coord: Tuple[int, int]) -> bool:
    x, y = coord
    return x >= 0 and x < self.size and y >= 0 and y < self.size

  def isEmptySquare(self, coord: Tuple[int, int]) -> bool:
    x, y = coord
    return self.board[x][y] == EMPTY

  def isAdjacentSquare(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> bool:
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

  def createdMils(self, coord: Tuple[int, int]) -> Union[None, List[List[Tuple[int, int]]]]:
    piece = WHITE if self.turn == "WHITE" else BLACK
    mils = []
    x, y = coord
    for i in range(3):
      if all([self.board[x][j] == piece for j in range(x-i, x-i+3)]):
        mils.append([(x, j) for j in range(x-i, x-i+3)])
      if all([self.board[j][y] == piece for j in range(y-i, y-i+3)]):
        mils.append([(j, y) for j in range(y-i, y-i+3)])
    return mils if len(mils) > 0 else None
  
  def printBoard(self) -> None:
    print("  0 1 2 3 4 5 6 7")
    for i, row in enumerate(self.board):
      print(f"{i} {' '.join(row)}")

class GameLoop:
    def __init__(self):
        self.game = Game()

    def start(self):
        while self.game.state == PLAYING:
            self.game.printBoard()
            print(f"It's {self.game.turn}'s turn!")
            
            if True:  # Assuming the player is WHITE
                coord1 = self.get_coordinate("Enter the starting coordinate (x,y): ") if self.game.phase[self.game.turn] != PLACING else (0,0)
                coord2 = self.get_coordinate("Enter the destination coordinate (x,y): ")
                result = self.game.makeMove(coord1, coord2)
                
                if result == False:
                    print("Invalid move. Try again.")
                    continue

                # Handle mil creation if needed
                if isinstance(result, list):
                    self.print_mils(result)
                    mil = input(f"Select mil 0-{len(result)-1}")
                    while not mil.isdigit() or int(mil) < 0 or int(mil) >= len(result):
                        mil = input(f"Select mil 0-{len(result)-1}")
                    mil = int(mil)
                    to_remove = self.get_coordinate("Enter the opponent piece to remove (x,y): ")
                    self.game.createMil(result[mil], to_remove)

            else:  # AI's turn
                # Placeholder for AI logic
                pass

            self.game.switchTurn()
            self.check_game_over()

    def get_coordinate(self, prompt: str) -> Tuple[int, int]:
        while True:
            try:
                x, y = map(int, input(prompt).split(','))
                return (x, y)
            except ValueError:
                print("Invalid input. Please enter coordinates in the format x,y.")

    def print_mils(self, mils: List[List[Tuple[int, int]]]):
        print("Mils created:")
        for i, mil in enumerate(mils):
            print(f"{i}: {mil}")

    def check_game_over(self):
        # Placeholder for game over checking logic
        pass
    

class AI():
  def __init__(self, difficulty: str) -> None:
    self.difficulty = difficulty

if __name__ == "__main__":
    loop = GameLoop()
    loop.start()

