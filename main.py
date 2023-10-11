from game import Game
from ai import AI
from constants import *
from typing import List, Tuple
import random


class GameLoop:
    def __init__(self):
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
            if self.game.turns >= TURN_LIMIT:
                self.game.state = TIE
            if self.game.pieces["WHITE" if self.game.turn == "BLACK" else "BLACK"] < 3:
                self.game.state = BLACK_WIN if self.game.turn == "BLACK" else WHITE_WIN

        print("Game over!")
        if self.game.state == TIE:
            print("It's a tie!")
        elif self.game.state == WHITE_WIN:
            print("White wins!")
        else:
            print("Black wins!")

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


if __name__ == "__main__":
    loop = GameLoop()
    loop.start()
