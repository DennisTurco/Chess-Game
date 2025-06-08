import chess
import pygame
import logging
from Entities.Pos import Pos
from Entities.PosMove import PosMove
from Menus.PromotionMenu import PromotionMenu
from Menus.MessageBox import MessageBox

class Move:
    def __init__(self, board: chess.Board, screen: pygame.Surface):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.board = board
        self.screen = screen
        self.finished = False
        self.restart = False

        self.sound_move = pygame.mixer.Sound("sounds/move.wav")
        self.sound_capture = pygame.mixer.Sound("sounds/capture.wav")

    def apply_move(self, playerClicks: PosMove) -> bool:
        """Applies a move given the playerClicks (start and end position).
        Returns True if the move is valid and applied, False otherwise.
        """
        if playerClicks.initial_position is None or playerClicks.final_position is None:
            return False

        # Convert coordinates (x,y) to algebraic (e.g. 'e2', 'e4')
        start_square = self._pos_to_algebraic(playerClicks.initial_position)
        end_square = self._pos_to_algebraic(playerClicks.final_position)

        # Build the UCI move
        uci_move = start_square + end_square

        # Control if promotion required (if it is pawn coming to the bottom).
        promotion_piece = self._check_promotion(playerClicks)

        if promotion_piece:
            uci_move += promotion_piece  # es. 'q', 'r', 'b', 'n'

        move = chess.Move.from_uci(uci_move)

        if move in self.board.legal_moves:
            self.board.push(move)
            self._play_sound(move)
            self._check_game_over()
            return True
        else:
            return False

    def _pos_to_algebraic(self, pos: Pos) -> str:
        """pos.x is column 0-7 (a-h), pos.y is row 0-7 (from above)
        python-chess uses 0=a1 at bottom left, so need to reverse y"""
        file = chr(ord('a') + pos.x)
        rank = str(8 - pos.y)
        return file + rank

    def _check_promotion(self, playerClicks: PosMove) -> str | None:
        initial_pos = playerClicks.initial_position
        final_pos = playerClicks.final_position
        piece = self.board.piece_at(chess.parse_square(self._pos_to_algebraic(initial_pos)))
        if piece is None or piece.piece_type != chess.PAWN:
            return None

        if (piece.color == chess.WHITE and final_pos.y == 0) or (piece.color == chess.BLACK and final_pos.y == 7):
            menu = PromotionMenu()
            return menu.show(self.screen)
        return None

    def _play_sound(self, move: chess.Move):
        if self.board.is_capture(move):
            self.sound_capture.play()
        else:
            self.sound_move.play()

    def _check_game_over(self):
        if self.board.is_checkmate():
            self.finished = True
            messageBox = MessageBox()
            white_won = (self.board.turn == chess.BLACK)  # turno prossimo ma game finito
            self.restart = messageBox.ask_restart(white_won, self.screen)
        elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
            self.finished = True
            messageBox = MessageBox()
            self.restart = messageBox.ask_restart(None, self.screen)  # stalmate

    def restart_game(self) -> None:
        self.board.reset()
        self.finished = False
        self.restart = False

    def apply_engine_move(self, uci_move: str) -> None:
        move = chess.Move.from_uci(uci_move)
        if move in self.board.legal_moves:
            self.board.push(move)
            self._play_sound(move)
            self._check_game_over()

    def is_current_turn_piece(self, pos: Pos) -> bool:
        square = chess.parse_square(self._pos_to_algebraic(pos))
        piece = self.board.piece_at(square)
        return piece is not None and piece.color == self.board.turn

    def setPossibleMovements(self, pos: Pos):
        self.possible_positions = [[0]*8 for _ in range(8)]
        square = chess.parse_square(self._pos_to_algebraic(pos))
        for move in self.board.legal_moves:
            if move.from_square == square:
                to_file = chess.square_file(move.to_square)
                to_rank = 7 - chess.square_rank(move.to_square)
                self.possible_positions[to_file][to_rank] = 1

    def getPossiblePositions(self):
        return getattr(self, "possible_positions", [[0]*8 for _ in range(8)])

    def moveRequest(self, posMove: PosMove) -> bool:
        from_square = chess.square(posMove.initial_position.x, 7 - posMove.initial_position.y)
        to_square = chess.square(posMove.final_position.x, 7 - posMove.final_position.y)
        move = chess.Move(from_square, to_square)
        if move in self.board.legal_moves and not self.board.is_capture(move):
            self.board.push(move)
            return True
        return False

    def captureRequest(self, posMove: PosMove) -> bool:
        from_square = chess.square(posMove.initial_position.x, 7 - posMove.initial_position.y)
        to_square = chess.square(posMove.final_position.x, 7 - posMove.final_position.y)
        move = chess.Move(from_square, to_square)
        if move in self.board.legal_moves and self.board.is_capture(move):
            self.board.push(move)
            return True
        return False