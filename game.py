
class Game:
  def __init__(self, H_size, V_size, difficulty):
      self.H_size = H_size
      self.V_size = V_size
      self.difficulty = difficulty
      self.board = Board(H_size, V_size)
      self.turn = "white" 
      self.win =  "playing"
      self.piecesLeft = {"white": 0, "black": 0}
      self.phase = {"white" : "placing", "black" : "placing" } # placing, moving, flying


  def place(self, x, y):
    if self.board.place(x, y, self.turn):
      self.piecesLeft[self.turn] -= 1
      if self.piecesLeft[self.turn] == 0:
        self.phase[self.turn] = "moving"
      self.changeTurn()
      return True
    return False
  
  def move(self, x1, y1, x2, y2):
    if self.board.move(x1, y1, x2, y2, self.turn):
      self.changeTurn()
      return True
    return False
  
  def fly(self, x1, y1, x2, y2):

    if self.board.fly(x1, y1, x2, y2, self.turn):
      self.changeTurn()
      return True
    return False
  
  def changeTurn(self):
    if self.turn == "white":
      self.turn = "black"
    else:
      self.turn = "white"

  def checkWin(self):
    if self.piecesLeft["white"] == 2:
      self.win = "black"
      return True
    if self.piecesLeft["black"] == 2:
      self.win = "white"
      return True
    return False
  
  def checkPhase(self):

    if self.phase == "placing":
      if self.piecesLeft[self.turn] == 0:
        self.phase = "moving"
    elif self.phase == "moving":
      if self.piecesLeft[self.turn] == 3:
        self.phase = "flying"
    elif self.phase == "flying":
      if self.piecesLeft[self.turn] == 0:
        self.phase = "moving"

  def checkPiecesLeft(self):
    self.piecesLeft["white"] = 0
    self.piecesLeft["black"] = 0
    for row in self.board.board:
      for piece in row:
        if piece != None:
          self.piecesLeft[piece.color] += 1
  
  def check(self):
    self.checkPiecesLeft()
    self.checkPhase()
    self.checkWin()

  def printBoard(self):
    self.board.printBoard()

  def printPiecesLeft(self):

    print("White pieces left: " + str(self.piecesLeft["white"]))
    print("Black pieces left: " + str(self.piecesLeft["black"]))

  def printTurn(self):
    print("Turn: " + self.turn)

  def printPhase(self):
    print("Phase: " + self.phase)

  def printWin(self):
    print("Win: " + self.win)

  def printGame(self):
    self.printBoard()
    self.printPiecesLeft()
    self.printTurn()
    self.printPhase()
    self.printWin()

class Board:
  def __init__(self, H_size, V_size):
    self.H_size = H_size
    self.V_size = V_size
    self.board = [[None for x in range(H_size)] for y in range(V_size)]

  def place(self, x, y, color):
    if self.board[y][x] == None:
      self.board[y][x] = Piece(color)
      return True
    return False

  def move(self, x1, y1, x2, y2, color):
    if self.board[y1][x1] != None and self.board[y2][x2] == None and self.board[y1][x1].color == color:
      self.board[y2][x2] = self.board[y1][x1]
      self.board[y1][x1] = None
      return True
    return False

  def fly(self, x1, y1, x2, y2, color):
    if self.board[y1][x1] != None and self.board[y2][x2] == None and self.board[y1][x1].color == color:
      self.board[y2][x2] = self.board[y1][x1]
      self.board[y1][x1] = None
      return True
    return False

  def printBoard(self):
    for row in self.board:
      for piece in row:
        if piece == None:
          print(" ", end=" ")
        else:
          print(piece.color[0], end=" ")
      print()

class Piece:
  def __init__(self, color):
    self.color = color

  
# Path: main.py

