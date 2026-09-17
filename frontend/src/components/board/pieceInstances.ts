import { Chess, type Color, type PieceSymbol, type Square } from 'chess.js';
import type { MoveRecord } from '../../types';

export interface PieceInstance {
  id: string;
  type: PieceSymbol;
  color: Color;
  square: Square;
}

/** Fresh, unanimated piece list read straight off a FEN. Used on mount, new game, undo, and jumps. */
export function piecesFromFen(fen: string): PieceInstance[] {
  const chess = new Chess(fen);
  const pieces: PieceInstance[] = [];
  let i = 0;
  for (const row of chess.board()) {
    for (const cell of row) {
      if (!cell) continue;
      pieces.push({ id: `p${i++}`, type: cell.type, color: cell.color, square: cell.square as Square });
    }
  }
  return pieces;
}

/**
 * Moves the matching piece instance(s) for one played move, preserving ids so
 * the board can animate the transition instead of popping to the new FEN.
 */
export function applyMoveToPieces(pieces: PieceInstance[], record: MoveRecord): PieceInstance[] {
  const from = record.uci.slice(0, 2) as Square;
  const to = record.uci.slice(2, 4) as Square;
  const promotion = record.uci.slice(4) as PieceSymbol | '';

  let next = pieces;

  if (record.flags.includes('e')) {
    const capturedSquare = (to[0] + from[1]) as Square;
    next = next.filter((p) => p.square !== capturedSquare);
  } else if (record.isCapture) {
    next = next.filter((p) => p.square !== to);
  }

  next = next.map((p) => (p.square === from ? { ...p, square: to, type: promotion || p.type } : p));

  if (record.flags.includes('k') || record.flags.includes('q')) {
    const kingside = record.flags.includes('k');
    const rank = record.color === 'w' ? '1' : '8';
    const rookFrom = `${kingside ? 'h' : 'a'}${rank}` as Square;
    const rookTo = `${kingside ? 'f' : 'd'}${rank}` as Square;
    next = next.map((p) => (p.square === rookFrom ? { ...p, square: rookTo } : p));
  }

  return next;
}
