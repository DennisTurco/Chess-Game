import type { Square } from 'chess.js';

export const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
export const RANKS = ['8', '7', '6', '5', '4', '3', '2', '1'];

/** Display column/row (0-7, top-left origin) for a square, honoring board flip. */
export function squareToXY(square: Square, flip: boolean): { col: number; row: number } {
  const file = square[0];
  const rank = square[1];
  const col = FILES.indexOf(file);
  const row = RANKS.indexOf(rank);
  return {
    col: flip ? 7 - col : col,
    row: flip ? 7 - row : row,
  };
}

export function xyToSquare(col: number, row: number, flip: boolean): Square {
  const c = flip ? 7 - col : col;
  const r = flip ? 7 - row : row;
  return `${FILES[c]}${RANKS[r]}` as Square;
}

/** Resolves the square under a pointer/mouse position, or null if outside the board. */
export function squareFromPoint(rect: DOMRect, clientX: number, clientY: number, flip: boolean): Square | null {
  const x = clientX - rect.left;
  const y = clientY - rect.top;
  if (x < 0 || y < 0 || x >= rect.width || y >= rect.height) return null;
  const col = Math.min(7, Math.max(0, Math.floor((x / rect.width) * 8)));
  const row = Math.min(7, Math.max(0, Math.floor((y / rect.height) * 8)));
  return xyToSquare(col, row, flip);
}
