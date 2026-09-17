import { Chess, type Move } from 'chess.js';
import type { MoveQuality, TutorTip } from '../types';

/**
 * Placeholder heuristic "coach" so the UI is fully playable before the
 * Python/Stockfish backend is wired in. Replace with a real call to the
 * engine's evaluation + comment endpoint later.
 */

const CENTER_SQUARES = new Set(['d4', 'd5', 'e4', 'e5']);

const HEADLINES: Record<MoveQuality, string[]> = {
  brilliant: ['Brilliant!', 'Stunning find!'],
  great: ['Great move', 'Strong choice'],
  good: ['Good move', 'Solid'],
  book: ['Book move', 'Well known theory'],
  inaccuracy: ['Slight inaccuracy', 'Not the sharpest'],
  mistake: ['Mistake', 'This lets the opponent back in'],
  blunder: ['Blunder!', 'This drops material'],
};

const COMMENTS: Record<MoveQuality, string[]> = {
  brilliant: [
    'A resource almost nobody finds over the board — it changes the evaluation completely.',
    'That sacrifice opens lines that will decide the game.',
  ],
  great: [
    'This keeps every piece coordinated and increases the pressure.',
    'A precise choice — it improves your position with no downside.',
  ],
  good: [
    'A reasonable, healthy move that keeps the position balanced.',
    'Nothing flashy, but it does not give the opponent anything either.',
  ],
  book: [
    'Still within well-known opening theory.',
    'A standard developing move for this structure.',
  ],
  inaccuracy: [
    'A more active piece placement was available here.',
    'This slightly loosens your position — watch the resulting weaknesses.',
  ],
  mistake: [
    'This allows the opponent a tactical opportunity.',
    'A more careful move was needed to keep the balance.',
  ],
  blunder: [
    'This hangs material — double-check captures before committing.',
    'The opponent can win material immediately after this.',
  ],
};

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

const PIECE_VALUES: Record<string, number> = { p: 1, n: 3, b: 3.25, r: 5, q: 9, k: 0 };

/** Rough material-based evaluation (pawns, White's perspective) used offline, before a real engine score is available. */
export function materialScore(chess: Chess): number {
  if (chess.isCheckmate()) return chess.turn() === 'w' ? -100 : 100;

  let score = 0;
  for (const row of chess.board()) {
    for (const cell of row) {
      if (!cell) continue;
      const value = PIECE_VALUES[cell.type] ?? 0;
      score += cell.color === 'w' ? value : -value;
    }
  }
  return score;
}

/**
 * Very rough local heuristic used only until real engine analysis is
 * connected: rewards captures/checks/center control, and randomly
 * sprinkles in inaccuracies so the panel feels alive during PvP too.
 */
export function evaluateMoveLocally(chessAfterMove: Chess, move: Move): TutorTip {
  let score = 0;

  if (move.captured) {
    const values: Record<string, number> = { p: 1, n: 3, b: 3, r: 5, q: 9 };
    score += (values[move.captured] ?? 0) * 2;
  }
  if (chessAfterMove.isCheck()) score += 3;
  if (chessAfterMove.isCheckmate()) score += 20;
  if (CENTER_SQUARES.has(move.to)) score += 2;
  if (move.san.includes('O-O')) score += 3;
  if (move.promotion) score += 6;

  score += Math.random() * 4 - 1.5;

  let quality: MoveQuality;
  if (chessAfterMove.isCheckmate() || score >= 14) quality = 'brilliant';
  else if (score >= 7) quality = 'great';
  else if (score >= 3) quality = 'good';
  else if (score >= 1) quality = 'book';
  else if (score >= -0.5) quality = 'inaccuracy';
  else if (score >= -2) quality = 'mistake';
  else quality = 'blunder';

  return {
    quality,
    headline: pick(HEADLINES[quality]),
    comment: pick(COMMENTS[quality]),
    score: materialScore(chessAfterMove),
  };
}

export function pickEngineMove(chess: Chess): Move | null {
  const moves = chess.moves({ verbose: true });
  if (moves.length === 0) return null;

  const scored = moves.map((m) => {
    let s = Math.random() * 3;
    if (m.captured) s += 4;
    if (m.san.includes('+')) s += 2;
    if (CENTER_SQUARES.has(m.to)) s += 1;
    return { m, s };
  });
  scored.sort((a, b) => b.s - a.s);
  return scored[0].m;
}
