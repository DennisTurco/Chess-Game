import type { PieceSymbol, Color } from 'chess.js';

const LETTER: Record<PieceSymbol, string> = {
  p: 'p',
  n: 'N',
  b: 'B',
  r: 'R',
  q: 'Q',
  k: 'K',
};

export function pieceImageSrc(color: Color, type: PieceSymbol): string {
  return `/pieces/${color}${LETTER[type]}.png`;
}
