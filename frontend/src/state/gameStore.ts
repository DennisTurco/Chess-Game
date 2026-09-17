import { Chess, type Square } from 'chess.js';
import { create } from 'zustand';
import { evaluateMoveLocally, pickEngineMove } from '../lib/tutor';
import { checkBackendHealth, fetchBestMove, fetchMoveComment } from '../lib/api';
import type { GameMode, MoveRecord, PlayerColor, TutorTip } from '../types';
import { playSound } from '../lib/sound';

export type GameStatus = 'idle' | 'playing' | 'checkmate' | 'draw' | 'stalemate' | 'resigned';

interface PendingPromotion {
  from: Square;
  to: Square;
}

interface GameState {
  chess: Chess;
  fen: string;
  mode: GameMode;
  elo: number;
  playerColor: PlayerColor;
  status: GameStatus;
  winner: PlayerColor | null;
  history: MoveRecord[];
  viewIndex: number; // for stepping back through history (analysis)
  selectedSquare: Square | null;
  legalTargets: Square[];
  lastMove: { from: Square; to: Square } | null;
  pendingPromotion: PendingPromotion | null;
  tutorTip: TutorTip | null;
  /** Current position evaluation, in pawns, from White's perspective (for the eval bar). */
  evalScore: number;
  hintMove: { from: Square; to: Square } | null;
  capturedByWhite: string[];
  capturedByBlack: string[];
  whiteMs: number;
  blackMs: number;
  clockRunning: boolean;
  backendAvailable: boolean | null; // null = not checked yet
  moveToken: number;

  checkBackend: () => void;
  startGame: (mode: GameMode, elo: number, playerColor: PlayerColor) => void;
  selectSquare: (square: Square) => void;
  beginDrag: (square: Square) => boolean;
  attemptMove: (from: Square, to: Square, promotion?: string) => void;
  resolvePromotion: (piece: string) => void;
  cancelPromotion: () => void;
  undo: () => void;
  resign: () => void;
  requestHint: () => void;
  goToMove: (index: number) => void;
  tick: (ms: number) => void;
}

const initialClock = 10 * 60 * 1000;

function boardStatus(chess: Chess): { status: GameStatus; winner: PlayerColor | null } {
  if (chess.isCheckmate()) {
    const winner: PlayerColor = chess.turn() === 'w' ? 'b' : 'w';
    return { status: 'checkmate', winner };
  }
  if (chess.isStalemate()) return { status: 'stalemate', winner: null };
  if (chess.isDraw()) return { status: 'draw', winner: null };
  return { status: 'playing', winner: null };
}

export const useGameStore = create<GameState>((set, get) => ({
  chess: new Chess(),
  fen: new Chess().fen(),
  mode: 'pvp',
  elo: 1200,
  playerColor: 'w',
  status: 'idle',
  winner: null,
  history: [],
  viewIndex: -1,
  selectedSquare: null,
  legalTargets: [],
  lastMove: null,
  pendingPromotion: null,
  tutorTip: null,
  evalScore: 0,
  hintMove: null,
  capturedByWhite: [],
  capturedByBlack: [],
  whiteMs: initialClock,
  blackMs: initialClock,
  clockRunning: false,
  backendAvailable: null,
  moveToken: 0,

  checkBackend: () => {
    checkBackendHealth().then((ok) => set({ backendAvailable: ok }));
  },

  startGame: (mode, elo, playerColor) => {
    const chess = new Chess();
    set((s) => ({
      chess,
      fen: chess.fen(),
      mode,
      elo,
      playerColor,
      status: 'playing',
      winner: null,
      history: [],
      viewIndex: -1,
      selectedSquare: null,
      legalTargets: [],
      lastMove: null,
      pendingPromotion: null,
      tutorTip: null,
      evalScore: 0,
      hintMove: null,
      capturedByWhite: [],
      capturedByBlack: [],
      whiteMs: initialClock,
      blackMs: initialClock,
      clockRunning: true,
      moveToken: s.moveToken + 1,
    }));

    get().checkBackend();

    if (mode === 'pve' && playerColor === 'b') {
      setTimeout(() => get().attemptMove('e2' as Square, 'e4' as Square), 400);
    }
  },

  selectSquare: (square) => {
    const { chess, selectedSquare, status } = get();
    if (status !== 'playing') return;

    if (selectedSquare === square) {
      set({ selectedSquare: null, legalTargets: [] });
      return;
    }

    const piece = chess.get(square);
    if (selectedSquare) {
      const targets = get().legalTargets;
      if (targets.includes(square)) {
        get().attemptMove(selectedSquare, square);
        return;
      }
    }

    if (piece && piece.color === chess.turn()) {
      const moves = chess.moves({ square, verbose: true });
      set({ selectedSquare: square, legalTargets: moves.map((m) => m.to as Square), hintMove: null });
    } else {
      set({ selectedSquare: null, legalTargets: [] });
    }
  },

  /** Unconditionally selects a square (no toggle-off), for starting a drag. Returns whether it is draggable. */
  beginDrag: (square) => {
    const { chess, status } = get();
    if (status !== 'playing') return false;
    const piece = chess.get(square);
    if (!piece || piece.color !== chess.turn()) return false;
    const moves = chess.moves({ square, verbose: true });
    set({ selectedSquare: square, legalTargets: moves.map((m) => m.to as Square), hintMove: null });
    return true;
  },

  attemptMove: (from, to, promotion) => {
    const { chess } = get();
    const piece = chess.get(from);
    const isPromotion =
      !promotion && piece?.type === 'p' && ((piece.color === 'w' && to[1] === '8') || (piece.color === 'b' && to[1] === '1'));

    if (isPromotion && !useSettingsAutoPromote()) {
      set({ pendingPromotion: { from, to }, selectedSquare: null, legalTargets: [] });
      return;
    }

    const finalPromotion = promotion ?? (isPromotion ? 'q' : undefined);

    let move;
    try {
      move = chess.move({ from, to, promotion: finalPromotion });
    } catch {
      set({ selectedSquare: null, legalTargets: [] });
      return;
    }
    if (!move) {
      set({ selectedSquare: null, legalTargets: [] });
      return;
    }

    const { status, winner } = boardStatus(chess);
    const tip = evaluateMoveLocally(chess, move);

    const record: MoveRecord = {
      san: move.san,
      uci: move.from + move.to + (move.promotion ?? ''),
      fenBefore: move.before,
      fenAfter: move.after,
      color: move.color as PlayerColor,
      moveNumber: Math.ceil(chess.history().length / 2),
      captured: move.captured,
      quality: tip.quality,
      comment: tip.comment,
      isCheck: chess.isCheck(),
      isCapture: !!move.captured,
      flags: move.flags,
      score: tip.score,
    };

    const capturedByWhite = [...get().capturedByWhite];
    const capturedByBlack = [...get().capturedByBlack];
    if (move.captured) {
      if (move.color === 'w') capturedByWhite.push(move.captured);
      else capturedByBlack.push(move.captured);
    }

    playSound(move.captured ? 'capture' : chess.isCheck() ? 'check' : 'move');

    const token = get().moveToken + 1;

    set({
      fen: chess.fen(),
      history: [...get().history, record],
      viewIndex: -1,
      selectedSquare: null,
      legalTargets: [],
      pendingPromotion: null,
      lastMove: { from, to },
      status,
      winner,
      tutorTip: tip,
      evalScore: tip.score ?? get().evalScore,
      hintMove: null,
      capturedByWhite,
      capturedByBlack,
      clockRunning: status === 'playing',
      moveToken: token,
    });

    const { mode, playerColor, elo, backendAvailable } = get();

    // Refine the instant local tip with the real engine's verdict once it lands.
    if (backendAvailable !== false) {
      fetchMoveComment(record.fenBefore, record.uci, elo)
        .then((realTip) => {
          if (get().moveToken !== token) return; // a newer move/undo happened meanwhile
          set({ tutorTip: realTip, evalScore: realTip.score ?? get().evalScore });
          set((s) => ({
            history: s.history.map((m) =>
              m === record ? { ...m, quality: realTip.quality, comment: realTip.comment, score: realTip.score } : m,
            ),
          }));
          if (get().backendAvailable !== true) set({ backendAvailable: true });
        })
        .catch(() => {
          if (get().backendAvailable !== false) set({ backendAvailable: false });
        });
    }

    if (status === 'playing' && mode === 'pve' && chess.turn() !== playerColor) {
      const requestEngineMove = async () => {
        await new Promise((r) => setTimeout(r, 400 + Math.random() * 300));
        if (get().moveToken !== token) return;

        let from: string | undefined;
        let to: string | undefined;
        let promo: string | undefined;

        if (backendAvailable !== false) {
          try {
            const { uci } = await fetchBestMove(get().fen, elo);
            from = uci.slice(0, 2);
            to = uci.slice(2, 4);
            promo = uci.slice(4) || undefined;
            if (get().backendAvailable !== true) set({ backendAvailable: true });
          } catch {
            if (get().backendAvailable !== false) set({ backendAvailable: false });
          }
        }

        if (!from || !to) {
          const local = pickEngineMove(get().chess);
          if (!local) return;
          from = local.from;
          to = local.to;
          promo = local.promotion;
        }

        if (get().moveToken !== token) return;
        get().attemptMove(from as Square, to as Square, promo);
      };

      void requestEngineMove();
    }
  },

  resolvePromotion: (piece) => {
    const pending = get().pendingPromotion;
    if (!pending) return;
    get().attemptMove(pending.from, pending.to, piece);
  },

  cancelPromotion: () => set({ pendingPromotion: null }),

  undo: () => {
    const { chess, mode } = get();
    chess.undo();
    if (mode === 'pve') chess.undo();
    const history = get().history.slice(0, mode === 'pve' ? -2 : -1);
    set((s) => ({
      fen: chess.fen(),
      history,
      viewIndex: -1,
      selectedSquare: null,
      legalTargets: [],
      tutorTip: history.at(-1)?.comment
        ? { quality: history.at(-1)!.quality!, headline: '', comment: history.at(-1)!.comment!, score: history.at(-1)!.score }
        : null,
      evalScore: history.at(-1)?.score ?? 0,
      lastMove: null,
      status: 'playing',
      winner: null,
      hintMove: null,
      moveToken: s.moveToken + 1,
    }));
  },

  resign: () => {
    const { playerColor } = get();
    set({ status: 'resigned', winner: playerColor === 'w' ? 'b' : 'w', clockRunning: false });
  },

  requestHint: () => {
    const { chess, fen, elo, backendAvailable } = get();
    const applyLocal = () => {
      const move = pickEngineMove(chess);
      if (move) set({ hintMove: { from: move.from as Square, to: move.to as Square } });
    };

    if (backendAvailable === false) {
      applyLocal();
      return;
    }

    fetchBestMove(fen, elo)
      .then(({ uci }) => {
        if (get().backendAvailable !== true) set({ backendAvailable: true });
        set({ hintMove: { from: uci.slice(0, 2) as Square, to: uci.slice(2, 4) as Square } });
      })
      .catch(() => {
        set({ backendAvailable: false });
        applyLocal();
      });
  },

  goToMove: (index) => set({ viewIndex: index }),

  tick: (ms) => {
    const { clockRunning, chess, whiteMs, blackMs } = get();
    if (!clockRunning) return;
    if (chess.turn() === 'w') {
      set({ whiteMs: Math.max(0, whiteMs - ms) });
    } else {
      set({ blackMs: Math.max(0, blackMs - ms) });
    }
  },
}));

function useSettingsAutoPromote(): boolean {
  try {
    const raw = localStorage.getItem('chess-tutor:settings');
    if (!raw) return false;
    return !!JSON.parse(raw).autoPromoteQueen;
  } catch {
    return false;
  }
}
