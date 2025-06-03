import chess
import chess.engine
import os

class MoveEvaluator:
    def __init__(self, path_to_engine: str = "./assets/engines/fairy-stockfish_x86-64.exe", skill_level: int = -5):
        if not os.path.exists(path_to_engine):
            raise FileNotFoundError(f"Engine not found at: {path_to_engine}")
        self.engine = chess.engine.SimpleEngine.popen_uci(path_to_engine)
        self.set_skill_level(skill_level)

    def set_skill_level(self, level: int):
        level = max(-5, min(level, 20))
        self.engine.configure({"Skill Level": level})

    def get_best_move(self, fen: str, time_limit: float = 0.5) -> str:
        board = chess.Board(fen)
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        if result.move is None:
            raise Exception("Error trying to evaluate the best move")
        return result.move.uci()

    def get_position_score(self, fen: str, time_limit: float = 0.5) -> float:
        board = chess.Board(fen)
        info = self.engine.analyse(board, chess.engine.Limit(time=time_limit))
        score = info["score"].white()
        if score.is_mate():
            mate_score = 100000 if score.mate() > 0 else -100000
            return mate_score
        return score.score(mate_score=100000)

    def get_position_evaluation(self, fen: str, time_limit: float = 0.5) -> str:
        score = self.get_position_score(fen, time_limit)
        if score > 100:
            return "White is clearly better"
        elif score > 20:
            return "White has a slight advantage"
        elif score < -100:
            return "Black is clearly better"
        elif score < -20:
            return "Black has a slight advantage"
        else:
            return "The position is balanced"

    def evaluate_move_quality(self, fen_before: str, move_uci: str, time_limit: float = 0.5) -> str:
        board = chess.Board(fen_before)
        if move_uci not in [m.uci() for m in board.legal_moves]:
            return "Illegal move"

        eval_before = self.get_position_score(fen_before, time_limit)

        # Apply the move
        move = chess.Move.from_uci(move_uci)
        board.push(move)
        eval_after = self.get_position_score(board.fen(), time_limit)

        eval_diff = eval_after - eval_before
        if board.turn == chess.BLACK:
            eval_diff *= -1  # Adjust for turn

        # Evaluation thresholds (you can tweak these)
        if eval_diff >= 150:
            return "Brilliant move"
        elif eval_diff >= 50:
            return "Great move"
        elif eval_diff >= -30:
            return "Good move"
        elif eval_diff >= -100:
            return "Inaccuracy"
        elif eval_diff >= -300:
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
    quality = engine.evaluate_move_quality(fen_before, move_uci=move)
    print(f"Move {move}: {quality}")
    # Also get best move and evaluation for context
    best_move = engine.get_best_move(fen_before)
    comment = engine.get_position_evaluation(fen_before)
    print("Suggested best move:", best_move)
    print("Position comment:", comment)
    engine.close()

if __name__ == "__main__":
    main()