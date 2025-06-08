import chess
import chess.engine
import os

from MoveComment import MoveComment

class MoveEvaluator:
    def __init__(self, path_to_engine: str = "./assets/engines/fairy-stockfish_x86-64.exe", skill_level: int = -5):
        if not os.path.exists(path_to_engine):
            raise FileNotFoundError(f"Engine not found at: {path_to_engine}")
        self.engine = chess.engine.SimpleEngine.popen_uci(path_to_engine)
        self._set_skill_level(skill_level)

    def _set_skill_level(self, level: int):
        level = max(-5, min(level, 20))
        self.engine.configure({"Skill Level": level})

    def get_best_move(self, fen: str, time_limit: float = 0.1) -> str:
        board = chess.Board(fen)
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        if result.move is None:
            raise Exception("Error trying to evaluate the best move")
        return result.move.uci()

    def get_move_comment(self, fen_before: str, move_uci: str, time_limit: float = 0.1) -> MoveComment:
        score = self._get_position_score(fen_before, time_limit)
        quality = self._evaluate_move_quality(fen_before, move_uci=move_uci, time_limit=time_limit)
        comment = self._get_position_evaluation(score)
        best_move = self.get_best_move(fen_before, time_limit)
        return MoveComment(score, quality, comment, best_move)

    def _get_position_score(self, fen: str, time_limit: float = 0.1) -> float:
        board = chess.Board(fen)
        info = self.engine.analyse(board, chess.engine.Limit(time=time_limit))
        score = info["score"].white()
        if score.is_mate():
            mate_score = 100000 if score.mate() > 0 else -100000
            return mate_score
        return score.score(mate_score=100000) / 100.0

    def _get_position_evaluation(self, score) -> str:
        if score > 1.0:
            return "White is clearly better"
        elif score > 0.2:
            return "White has a slight advantage"
        elif score < -1.0:
            return "Black is clearly better"
        elif score < -0.2:
            return "Black has a slight advantage"
        else:
            return "The position is balanced"

    def _evaluate_move_quality(self, fen_before: str, move_uci: str, time_limit: float = 0.1) -> str:
        board = chess.Board(fen_before)
        player = board.turn  # True for White, False for Black

        if move_uci not in [m.uci() for m in board.legal_moves]:
            return "Illegal move"

        eval_before = self._get_position_score(fen_before, time_limit)

        # Apply the move
        move = chess.Move.from_uci(move_uci)
        board.push(move)
        eval_after = self._get_position_score(board.fen(), time_limit)

        eval_diff = eval_after - eval_before
        if not player:
            eval_diff *= -1  # Invert if the move was made by Black

        # Now correctly evaluate quality
        if eval_diff >= 1.5:
            return "Brilliant move"
        elif eval_diff >= 0.5:
            return "Great move"
        elif eval_diff >= -0.3:
            return "Good move"
        elif eval_diff >= -1.0:
            return "Inaccuracy"
        elif eval_diff >= -3.0:
            return "Mistake"
        else:
            return "Blunder"

    def close(self):
        self.engine.quit()


def main():
    engine = MoveEvaluator()
    fen_before = "r1bqkbnr/pppp1ppp/2n5/4p3/1b2P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 4"
    move = "c2c3"  # Let's say the user made this move

    # Get move quality
    comment: MoveComment = engine.get_move_comment(fen_before, move)
    print(f"Move {move}: {comment.quality}")
    print("Position comment:", comment.comment)
    print("Suggested best move:", comment.best)
    engine.close()

if __name__ == "__main__":
    main()