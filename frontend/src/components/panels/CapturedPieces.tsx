import type { PieceSymbol } from 'chess.js';
import { useGameStore } from '../../state/gameStore';
import { pieceImageSrc } from '../board/pieceImage';
import './panels.css';

const VALUES: Record<string, number> = { p: 1, n: 3, b: 3, r: 5, q: 9 };
const ORDER = ['q', 'r', 'b', 'n', 'p'];

function sortCaptures(pieces: string[]) {
  return [...pieces].sort((a, b) => ORDER.indexOf(a) - ORDER.indexOf(b));
}

function materialDiff(list: string[]) {
  return list.reduce((sum, p) => sum + (VALUES[p] ?? 0), 0);
}

interface Props {
  color: 'w' | 'b';
}

export function CapturedPieces({ color }: Props) {
  const capturedByWhite = useGameStore((s) => s.capturedByWhite);
  const capturedByBlack = useGameStore((s) => s.capturedByBlack);

  const captured = color === 'w' ? capturedByWhite : capturedByBlack;
  const opponentCaptured = color === 'w' ? capturedByBlack : capturedByWhite;
  const advantage = materialDiff(captured) - materialDiff(opponentCaptured);

  return (
    <div className="captured-row">
      {sortCaptures(captured).map((piece, i) => (
        <img key={i} src={pieceImageSrc(color === 'w' ? 'b' : 'w', piece as PieceSymbol)} className="captured-icon" />
      ))}
      {advantage > 0 && <span className="material-advantage">+{advantage}</span>}
    </div>
  );
}
