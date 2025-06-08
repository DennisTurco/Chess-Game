import chess

class Board:
    def __init__(self, fen=None):
        if fen is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(fen)

    def move_piece(self, uci_move: str) -> bool:
        """Apply a UCI format move (es. e2e4). Return True if valid"""
        move = chess.Move.from_uci(uci_move)
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def board_to_fen(self) -> str:
        return self.board.fen()

    def is_flipped(self) -> bool:
        return False

    def restartBoard(self) -> None:
        self.board.reset()

    def get_piece_at(self, square: chess.Square):
        if isinstance(square, str):
            square = chess.parse_square(square)
        piece = self.board.piece_at(square)
        return piece  # chess.Piece object or None

    def turn(self):
        return self.board.turn  # True = White, False = Black
