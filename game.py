from typing import List, Tuple, Union
import random
from constants import (
    EMPTY,
    WHITE,
    WHITE_MIL,
    WHITE_WIN,
    BLACK,
    BLACK_MIL,
    BLACK_WIN,
    PLACING,
    MOVING,
    FLYING,
    PLAYING,
    TIE,
)


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


class GameLoop:
    def __init__(self):
        self.game = Game()
        self.game = Game()
        while True:
            difficulty = input("Enter AI difficulty (easy/medium/hard): ")
            if difficulty in ["easy", "medium", "hard"]:
                break
            print("Invalid difficulty. Please enter 'easy', 'medium', or 'hard'.")
        self.ai = AI(difficulty)

    def start(self):
        while self.game.state == PLAYING:
            self.game.printBoard()
            print(f"Turn: {self.game.turns}")
            print(f"It's {self.game.turn}'s turn!")
            print(f"Phase: {self.game.phase[self.game.turn]}")
            if self.game.hands[self.game.turn]:
                print(f"Pieces on hand: {self.game.hands[self.game.turn]}")
            print(f"Pieces left: {self.game.pieces[self.game.turn]}")
            print(f"Evaluation: {self.ai.heuristic(self.game)}")

            if self.game.turn == "WHITE":
                coord1 = (
                    self.get_coordinate("Enter the starting coordinate: ")
                    if self.game.phase[self.game.turn] != PLACING
                    else (0, 0)
                )
                coord2 = self.get_coordinate("Enter the destination coordinate: ")
                result = self.game.makeMove(coord1, coord2)

                if result == False:
                    print("Invalid move. Try again.")
                    continue

                # Handle mil creation if needed
                if isinstance(result, list):
                    if len(result) > 1:
                        self.print_mils(result)
                        mil = input(f"Select mil 1-{len(result)}: ")
                        while (
                            not mil.isdigit() or int(mil) <= 0 or int(mil) > len(result)
                        ):
                            mil = input(f"Select mil 1-{len(result)}: ")
                        mil = int(mil) - 1
                    else:
                        mil = 0
                    to_remove = self.get_coordinate(
                        "Enter the opponent piece to remove: "
                    )
                    self.game.createMil(result[mil], to_remove)

            else:  # AI's turn
                (x1, y1), (x2, y2) = self.ai.generateMove(self.game)
                result = self.game.makeMove((x1, y1), (x2, y2))
                if result == False:
                    print("Invalid move. Try again.")
                    continue
                elif isinstance(result, list):
                    self.print_mils(result)
                    mil = random.randint(0, len(result) - 1)
                    to_remove = random.choice(result[mil])
                    self.game.createMil(result[mil], to_remove)

            self.game.switchTurn()
            self.check_game_over()

    def get_coordinate(self, prompt: str) -> Tuple[int, int]:
        while True:
            try:
                res = input(prompt)
                x, y = ord(res[0]) - ord("a"), int(res[1]) - 1
                return (x, y)
            except ValueError:
                print("Invalid input. Please enter coordinates in the format a1.")

    def print_mils(self, mils: List[List[Tuple[int, int]]]):
        print("Mils created:")
        for i, mil in enumerate(mils):
            print(f"{i + 1}: {mil}")

    def get_rules(self) -> str:
        return """
            GAME RULES
            
            The goal of the game is to reduce the opponents number of pieces to two. Pieces 
            are placed on a grid board and once a player only have two pieces left, the game 
            is over and the player with more pieces wins. The game is drawn after 300 turns.
            
            Capture: 
                - A capture is the action of removing a piece from the opponent. 
                  The piece cannot be a part of a mil.
                - Captures can occur during any phase of the game
                
            Mil: 
                - A mil is a formation consisting of three pieces from the 
                  same player ordered in a row or column on the board
                - A piece cannot be part of more than one mil at a time, even 
                  though it might be part of a row and a column for instance
                - Mils can be formed during any phase of the game
                - After creating a mil, the player may perform a capture.
            
            Phase 1 (Placing phase):
                - The players each take a turn to put a piece on any vacant spot on the board
                - The phase ends when all of the players pieces are placed on the board
                
            Phase 2 (Moving phase):
                - During this phase, the players take turn in moving their pieces to adjacent 
                  vacant spots on the board
                - Pieces may not be moved diagonally, only horizontal and vertical moves 
                  are allowed
                - The phase ends when a player only have three pieces left
                
            Phase 3 (Flying phase):
                - In the end phase of the game, players may move pieces to any vacant spot 
                  on the board during their turn (called 'flying')
                - The game is over when a player is reduced to only two pieces.
        """

    def check_game_over(self):
        # Placeholder for game over checking logic
        pass


class AI:
    def __init__(self, difficulty: str) -> None:
        self.difficulty = difficulty

    def generateMove(self, game: Game) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        if self.difficulty == "easy":
            return self.generateRandomMove(game)
        depth = 3 if self.difficulty == "medium" else 5
        _, move = self.minimax(game, depth, False)
        return move

    def generateRandomMove(self, game: Game) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        moves = game.getValidMoves()
        return random.choice(moves)

    def heuristic(self, game: Game) -> int:
        PIECE_FACTOR = 1
        MIL_PROXIMITY = 2
        MIL_FACTOR = 10
        score = 0

        # 1. Number of pieces
        score += game.pieces["WHITE"] * PIECE_FACTOR
        score -= game.pieces["BLACK"] * PIECE_FACTOR

        # 3. Two pieces in a row
        for i in range(game.size):
            for j in range(game.size - 1):
                if game.board[i][j] == game.board[i][j + 1] == WHITE:
                    score += MIL_PROXIMITY
                elif game.board[i][j] == game.board[i][j + 1] == BLACK:
                    score -= MIL_PROXIMITY

                if game.board[j][i] == game.board[j + 1][i] == WHITE:
                    score += MIL_PROXIMITY
                elif game.board[j][i] == game.board[j + 1][i] == BLACK:
                    score -= MIL_PROXIMITY

        # 4. If a player has a mil
        score += len(game.mils["WHITE"]) * MIL_FACTOR
        score -= len(game.mils["BLACK"]) * MIL_FACTOR

        return score

    def minimax(
        self,
        game: Game,
        depth: int,
        maximizing: bool,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
    ) -> Tuple[float, Tuple[Tuple[int, int], Tuple[int, int]]]:
        if depth == 0 or game.state != PLAYING:
            return self.heuristic(game), None

        best_move = None

        if maximizing:
            max_eval = float("-inf")
            for move in game.getValidMoves():
                game_copy = self.copy_game(game)
                result = game_copy.makeMove(*move)

                # Check if a mil has been created
                if isinstance(result, list):
                    best_remove_eval = float("-inf")
                    for remove_piece in game_copy.getRemovablePieces("BLACK"):
                        game_copy_after_remove = self.copy_game(game_copy)
                        game_copy_after_remove.createMil(result[0], remove_piece)
                        remove_eval, _ = self.minimax(
                            game_copy_after_remove, depth - 1, False, alpha, beta
                        )
                        if remove_eval > best_remove_eval:
                            best_remove_eval = remove_eval
                    eval_value = best_remove_eval
                else:
                    eval_value, _ = self.minimax(
                        game_copy, depth - 1, False, alpha, beta
                    )

                if eval_value > max_eval:
                    max_eval = eval_value
                    best_move = move
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for move in game.getValidMoves():
                game_copy = self.copy_game(game)
                result = game_copy.makeMove(*move)
                if isinstance(result, list):
                    best_remove_eval = float("inf")
                    for remove_piece in game_copy.getRemovablePieces("WHITE"):
                        game_copy_after_remove = self.copy_game(game_copy)
                        game_copy_after_remove.createMil(result[0], remove_piece)
                        remove_eval, _ = self.minimax(
                            game_copy_after_remove, depth - 1, True, alpha, beta
                        )
                        if remove_eval < best_remove_eval:
                            best_remove_eval = remove_eval
                    eval_value = best_remove_eval
                else:
                    eval_value, _ = self.minimax(
                        game_copy, depth - 1, True, alpha, beta
                    )
                if eval_value < min_eval:
                    min_eval = eval_value
                    best_move = move
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def copy_game(self, game: Game) -> Game:
        new_game = Game(game.size, game.pieces["WHITE"])
        new_game.board = [row.copy() for row in game.board]
        new_game.hands = game.hands.copy()
        new_game.pieces = game.pieces.copy()
        new_game.phase = game.phase.copy()
        new_game.mils = {
            "WHITE": game.mils["WHITE"].copy(),
            "BLACK": game.mils["BLACK"].copy(),
        }
        new_game.state = game.state
        new_game.turn = game.turn
        new_game.turns = game.turns
        return new_game


if __name__ == "__main__":
    loop = GameLoop()
    loop.start()
