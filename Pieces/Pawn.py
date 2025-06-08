import chess
from Entities.Pos import Pos
from Pieces.Piece import Piece

class Pawn(Piece):
    def __init__(self, board: chess.Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy: Pos) -> None:
        self.possible_moves = [[0 for _ in range(8)] for _ in range(8)]  # reset possibili mosse

        x, y = posxy.x, posxy.y
        board = self.board

        # Converte Pos (x,y) in square di python-chess (0..63)
        # python-chess usa notazione a1=0, h8=63:
        # square = chess.square(file, rank) dove file e rank da 0 a 7
        # file corrisponde a x, rank a y ma invertito (0=rank1/basso, 7=rank8/alto)
        square = chess.square(x, 7 - y)

        piece = board.piece_at(square)
        if piece is None:
            return  # niente pezzo da cui generare mosse

        direction = 1 if self.is_white_turn else -1  # nel chess.Board bianco muove verso rank crescenti

        # Movimento in avanti di 1
        forward_rank = (7 - y) + direction
        if 0 <= forward_rank <= 7:
            forward_square = chess.square(x, forward_rank)
            if board.piece_at(forward_square) is None:
                # contrassegna mossa valida in avanti
                self.possible_moves[7 - forward_rank][x] = 1

                # Movimento iniziale di 2 caselle
                start_rank = 1 if self.is_white_turn else 6
                if (7 - y) == start_rank:
                    forward_two_rank = forward_rank + direction
                    if 0 <= forward_two_rank <= 7:
                        forward_two_square = chess.square(x, forward_two_rank)
                        if board.piece_at(forward_two_square) is None:
                            self.possible_moves[7 - forward_two_rank][x] = 1

        # Catture diagonali
        for dx in [-1, 1]:
            capture_file = x + dx
            capture_rank = (7 - y) + direction
            if 0 <= capture_file <= 7 and 0 <= capture_rank <= 7:
                capture_square = chess.square(capture_file, capture_rank)
                target_piece = board.piece_at(capture_square)
                if target_piece is not None and target_piece.color != piece.color:
                    self.possible_moves[7 - capture_rank][capture_file] = 2
