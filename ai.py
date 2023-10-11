from game import Game
from constants import *
from typing import List, Tuple
import random


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
