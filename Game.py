import pygame
import logging
import sys
from typing import Optional
import pygame_menu.font as font_module
import chess

from Enums.Mode import Mode
from Move import Move
from MoveEmulator import MoveEvaluator
from Widgets.ButtonImage import ButtonImage
from Entities.Pos import Pos
from Entities.PosMove import PosMove
from Enums.Piece import Color

import GameManager

class Game:

    def __init__(self, color_side: Color = Color.WHITE, elo: Optional[int] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.color_side = color_side
        self.elo = elo if elo is not None else 20
        self.move_comment = ""
        self.move_history: list[str] = []

        if elo is None:
            self.mode = Mode.PVP
            self.elo = 20
        else:
            self.mode = Mode.PVE

        self.engine = MoveEvaluator(skill_level=self.elo)

        font_path = font_module.FONT_MUNRO
        self.normal_text = pygame.font.Font(font_path, 20)
        self.bold_text = pygame.font.SysFont(font_path, 35, bold=True)

        self.IMAGES = {}

        self.game()

    def game(self) -> None:
        self.logger.info(f"Starting game with color_side={self.color_side}, elo={self.elo}")

        self.screen: pygame.Surface = self.init_and_get_window()
        self.board = chess.Board()
        self.move = Move(self.board, self.screen)
        self.move_history: list[str] = []

        playerClicks = PosMove()
        possiblePositions: list[list[int]] = self.reset_possible_positions()

        player_turn = self._is_player_turn(True)

        self.loadImages()
        running = True
        self.buttons = self.draw_buttons()

        while running:
            self.screen.fill(pygame.Color('white'))
            self.refresh(possiblePositions)
            self.buttons = self.draw_buttons()

            if self.mode == Mode.PVE and not player_turn:
                engine_move = self.engine.get_best_move(self.board.fen()) # UCI move, ex. 'e2e4'
                if engine_move:
                    # Applica mossa dell'engine
                    self.move.apply_engine_move(engine_move)
                    self.move_history.append(engine_move)  # puoi trasformarla in notazione standard se vuoi
                player_turn = True
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    (running, playerClicks, possiblePositions, player_turn) = self.__handle_mouse_click(pos, playerClicks, possiblePositions, player_turn)

                if self.move.restart:
                    playerClicks, possiblePositions = self.restart_game()
                    player_turn = self._is_player_turn(True)
                    continue
                elif self.move.finished:
                    running = False

                self.refresh(possiblePositions)

    def __handle_mouse_click(self, pos: tuple[int, int], playerClicks: PosMove, possiblePositions: list[list[int]], player_turn: bool):

        if self.buttons["reset"].is_clicked(pos):
            return True, *self.restart_game(), self._is_player_turn(True)

        if self.buttons["menu"].is_clicked(pos):
            return False, playerClicks, possiblePositions, player_turn

        if pos[0] < GameManager.SIDEBAR_WIDTH:
            return True, playerClicks, possiblePositions, player_turn

        fen_before = self.board.fen()

        board_x = (pos[0] - GameManager.SIDEBAR_WIDTH) // GameManager.SQ_SIZE
        board_y = pos[1] // GameManager.SQ_SIZE
        clicked_pos = Pos(board_x, board_y)
        posxy = self._get_board_pos(clicked_pos)

        # Qui dobbiamo capire se nel quadrato c'è un pezzo
        square = chess.square(posxy.x, 7 - posxy.y)  # converto coordinate a indice square di python-chess
        piece = self.board.piece_at(square)

        if piece is not None:
            if playerClicks.initial_position is None or self.move.is_current_turn_piece(posxy):
                playerClicks.initial_position = posxy
                self.move.setPossibleMovements(posxy)
                possiblePositions = self.move.getPossiblePositions()
            elif playerClicks.initial_position == posxy:
                playerClicks.reset()
            else:
                playerClicks.final_position = posxy
                if self.move.captureRequest(playerClicks):
                    self._set_move_message(fen_before, playerClicks)
                    self.logger.info(f"Captured from {playerClicks.initial_position} to {playerClicks.final_position}")
                playerClicks.reset()
                possiblePositions = self.reset_possible_positions()
        elif playerClicks.initial_position:
            playerClicks.final_position = posxy
            if self.move.moveRequest(playerClicks):
                self._set_move_message(fen_before, playerClicks)
                self.logger.info(f"Moved from {playerClicks.initial_position} to {playerClicks.final_position}")
                player_turn = self._is_player_turn(not player_turn)
            playerClicks.reset()
            possiblePositions = self.reset_possible_positions()

        return True, playerClicks, possiblePositions, player_turn

    def _set_move_message(self, fen_before, player_clicks: PosMove) -> None:
        notation = self.get_move_notation(player_clicks)
        self.move_history.append(notation)
        uci_move = self.get_uci_move_notation(player_clicks)
        move_comment = self.engine.get_move_comment(fen_before, uci_move)
        self.logger.info(f"UCI move: {uci_move}")
        self.move_comment = f"{move_comment.quality}\n{move_comment.score} {move_comment.comment}"
        self.logger.info(f"Move comment: {self.move_comment.replace("\n", " - ")}")

    def _is_player_turn(self, player_turn: bool) -> bool:
        return self.elo is None or player_turn

    def restart_game(self):
        self.board = chess.Board()
        self.move = Move(self.board, self.screen)
        self.move_history.clear()
        playerClicks = PosMove()
        possiblePositions = self.reset_possible_positions()
        return playerClicks, possiblePositions

    def reset_possible_positions(self) -> list[list[int]]:
        return [[0 for _ in range(GameManager.DIMENSION)] for _ in range(GameManager.DIMENSION)]

    def loadImages(self):
        pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']

        for piece in pieces:
            image = f"assets/images/{piece}.png"
            try:
                self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(image), (GameManager.SQ_SIZE, GameManager.SQ_SIZE))
            except Exception as e:
                self.logger.error(f"{sys.argv[0]} -> error loading image {piece}: {e}")

    def init_and_get_window(self) -> pygame.Surface:
        pygame.init()
        pygame.display.set_caption(GameManager.APP_NAME)
        programIcon = pygame.image.load('assets/images/wK.png')
        pygame.display.set_icon(programIcon)
        screen = pygame.display.set_mode((GameManager.WINDOW_WIDTH, GameManager.HEIGHT))
        screen.fill(pygame.Color('white'))
        return screen

    def refresh(self, possiblePositions: list[list[int]]) -> None:
        self.drawGameState(possiblePositions)
        pygame.display.flip()

    def drawGameState(self, possiblePositions: list[list[int]]) -> None:
        self.drawSidebar()
        self.drawBoard()
        self.drawHighlight(possiblePositions)
        self.drawPieces()

    def drawBoard(self) -> None:
        colors = [pygame.Color('white'), pygame.Color('gray')]

        for row in range(GameManager.DIMENSION):
            for col in range(GameManager.DIMENSION):
                display_row = 7 - row if self.color_side == Color.BLACK else row
                display_col = 7 - col if self.color_side == Color.BLACK else col

                x = display_col * GameManager.SQ_SIZE + GameManager.SIDEBAR_WIDTH
                y = display_row * GameManager.SQ_SIZE
                color = colors[(row + col) % 2]

                pygame.draw.rect(self.screen, color, pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))

                # numbers to left
                if col == 0:
                    label_row = 8 - row if self.color_side == Color.WHITE else row + 1
                    text = self.normal_text.render(str(label_row), False, pygame.Color('black'))
                    self.screen.blit(text, (GameManager.SIDEBAR_WIDTH - 18, y + 4))

                # chars to down
                if row == 7:
                    label_col = chr(65 + col) if self.color_side == Color.WHITE else chr(72 - col)
                    text = self.normal_text.render(label_col, False, pygame.Color('black'))
                    self.screen.blit(text, (x + GameManager.SQ_SIZE // 2 - 6, GameManager.HEIGHT - 20))

    def draw_buttons(self) -> dict[str, ButtonImage]:
        if not hasattr(self, "buttons"):
            image_restart = pygame.image.load("assets/images/reset.png").convert_alpha()
            image_menu = pygame.image.load("assets/images/reset.png").convert_alpha()
            reset_button = ButtonImage(self.screen, 10, 400, image_restart, 0.08, 180, 255)
            menu_button = ButtonImage(self.screen, 10, 450, image_menu, 0.08, 180, 255)
            self.buttons = {"reset": reset_button, "menu": menu_button}

        self.buttons["reset"].update()
        self.buttons["reset"].draw()
        self.buttons["menu"].update()
        self.buttons["menu"].draw()

        return self.buttons

    def drawSidebar(self) -> None:
        pygame.draw.rect(self.screen, pygame.Color("lightgray"), pygame.Rect(0, 0, GameManager.SIDEBAR_WIDTH, GameManager.HEIGHT))

        # app name
        title = self.bold_text.render(GameManager.APP_NAME, False, pygame.Color("black"))
        self.screen.blit(title, (10, 10))

        # history moves
        label = self.normal_text.render("Moves:", False, pygame.Color("black"))
        self.screen.blit(label, (10, 40))

        y_offset = 70
        for i, move in enumerate(self.move_history[-15:]):  # show only the last 15 moves
            text = self.normal_text.render(move, False, pygame.Color("black"))
            self.screen.blit(text, (10, y_offset + i * 18))

        if "reset" in self.buttons:
            self.buttons["reset"].update()
            self.buttons["reset"].draw()
        if "menu" in self.buttons:
            self.buttons["menu"].update()
            self.buttons["menu"].draw()

        if hasattr(self, 'move_comment') and self.move_comment:
            comment_label = self.normal_text.render("Comment:", False, pygame.Color("black"))
            comment_text = self.normal_text.render(self.move_comment, False, pygame.Color("blue"))
            self.screen.blit(comment_label, (10, y_offset + 15 * 18 + 10))
            self.screen.blit(comment_text, (10, y_offset + 15 * 18 + 30))

    def drawHighlight(self, possiblePositions: list[list[int]]) -> None:
        if possiblePositions == [[], []]:
            return
        image_dot = pygame.transform.scale(pygame.image.load("assets/images/black_dot.png"), (GameManager.SQ_SIZE, GameManager.SQ_SIZE))
        image_circle = pygame.transform.scale(pygame.image.load("assets/images/black_circle.png"), (GameManager.SQ_SIZE, GameManager.SQ_SIZE))

        for i in range(GameManager.DIMENSION):
            for j in range(GameManager.DIMENSION):
                x = i * GameManager.SQ_SIZE + GameManager.SIDEBAR_WIDTH
                y = j * GameManager.SQ_SIZE

                if possiblePositions[i][j] == 1:
                    self.screen.blit(image_dot, pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))
                elif possiblePositions[i][j] == 2:
                    self.screen.blit(image_circle, pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))

    def drawPieces(self) -> None:
        # python-chess ha indice 0=a1 in basso a sinistra
        # noi vogliamo disegnare dalla (0,0) in alto a sinistra
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is None:
                continue
            color_prefix = 'w' if piece.color == chess.WHITE else 'b'
            piece_letter = piece.symbol().lower()
            # Mappatura simboli in file immagini (es. 'p' -> 'p', 'n'->'N' ecc)
            # la tua naming sembra bP, wN, ecc. quindi mappiamo:
            piece_map = {
                'p': 'p',
                'n': 'N',
                'b': 'B',
                'r': 'R',
                'q': 'Q',
                'k': 'K'
            }
            piece_name = color_prefix + piece_map[piece_letter]
            if piece_name in self.IMAGES:
                # Calcolo coordinate disegno:
                file = chess.square_file(square)  # 0-7 (a-h)
                rank = 7 - chess.square_rank(square)  # 0-7, invertito per disegno

                # Se lato nero, inverti
                draw_x = file if self.color_side == Color.WHITE else 7 - file
                draw_y = rank if self.color_side == Color.WHITE else 7 - rank

                self.screen.blit(self.IMAGES[piece_name], pygame.Rect(
                    draw_x * GameManager.SQ_SIZE + GameManager.SIDEBAR_WIDTH,
                    draw_y * GameManager.SQ_SIZE,
                    GameManager.SQ_SIZE,
                    GameManager.SQ_SIZE
                ))
            else:
                self.logger.error(f"Cannot find image for piece {piece_name}")

    def get_move_notation(self, playerClicks: PosMove) -> str:
        """Converts the move from PosMove to SAN notation"""
        try:
            from_square = chess.square(playerClicks.initial_position.x, 7 - playerClicks.initial_position.y)
            to_square = chess.square(playerClicks.final_position.x, 7 - playerClicks.final_position.y)
            move = chess.Move(from_square, to_square)
            if move in self.board.legal_moves:
                return self.board.san(move)
            else:
                return move.uci()
        except Exception as e:
            self.logger.error(f"Error generating move notation: {e}")
            return ""

    def get_uci_move_notation(self, playerClicks: PosMove) -> str:
        """Converts the move from PosMove to UCI notation (e.g., 'e2e4')"""
        try:
            from_square = chess.square(playerClicks.initial_position.x, 7 - playerClicks.initial_position.y)
            to_square = chess.square(playerClicks.final_position.x, 7 - playerClicks.final_position.y)
            move = chess.Move(from_square, to_square)
            return move.uci()
        except Exception as e:
            self.logger.error(f"Error generating UCI notation: {e}")
            return ""

    def _get_board_pos(self, clicked_pos: Pos) -> Pos:
        # Converte la posizione del click secondo il lato del giocatore
        if self.color_side == Color.WHITE:
            return clicked_pos
        else:
            return Pos(7 - clicked_pos.x, 7 - clicked_pos.y)
