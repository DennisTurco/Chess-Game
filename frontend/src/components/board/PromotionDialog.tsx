import { useGameStore } from '../../state/gameStore';
import { pieceImageSrc } from './pieceImage';
import type { PieceSymbol } from 'chess.js';

const CHOICES: PieceSymbol[] = ['q', 'r', 'b', 'n'];

export function PromotionDialog() {
  const pendingPromotion = useGameStore((s) => s.pendingPromotion);
  const chess = useGameStore((s) => s.chess);
  const resolvePromotion = useGameStore((s) => s.resolvePromotion);
  const cancelPromotion = useGameStore((s) => s.cancelPromotion);

  if (!pendingPromotion) return null;
  const color = chess.turn();

  return (
    <div className="promotion-overlay" onMouseDown={(e) => e.target === e.currentTarget && cancelPromotion()}>
      <div className="promotion-card">
        <p className="promotion-title">Promote to</p>
        <div className="promotion-choices">
          {CHOICES.map((piece) => (
            <button key={piece} className="promotion-choice" onClick={() => resolvePromotion(piece)}>
              <img src={pieceImageSrc(color, piece)} alt={piece} />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
