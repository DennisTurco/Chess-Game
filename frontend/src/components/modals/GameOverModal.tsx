import { Modal } from '../common/Modal';
import { Button } from '../common/Button';
import { useGameStore } from '../../state/gameStore';
import './modals.css';

interface Props {
  onNewGame: () => void;
}

export function GameOverModal({ onNewGame }: Props) {
  const status = useGameStore((s) => s.status);
  const winner = useGameStore((s) => s.winner);
  const playerColor = useGameStore((s) => s.playerColor);
  const mode = useGameStore((s) => s.mode);

  const open = status !== 'idle' && status !== 'playing';

  let title = 'Game over';
  let subtitle = '';

  if (status === 'checkmate') {
    const playerWon = mode === 'pvp' ? true : winner === playerColor;
    title = mode === 'pvp' ? `${winner === 'w' ? 'White' : 'Black'} wins` : playerWon ? 'You won' : 'You lost';
    subtitle = 'Checkmate.';
  } else if (status === 'stalemate') {
    title = 'Draw';
    subtitle = 'Stalemate — no legal moves, but the king is not in check.';
  } else if (status === 'draw') {
    title = 'Draw';
    subtitle = 'Draw by repetition, the 50-move rule, or insufficient material.';
  } else if (status === 'resigned') {
    const playerWon = winner === playerColor;
    title = mode === 'pvp' ? `${winner === 'w' ? 'White' : 'Black'} wins by resignation` : playerWon ? 'Engine resigned' : 'You resigned';
  }

  return (
    <Modal open={open}>
      <h2 className="serif modal-title">{title}</h2>
      {subtitle && <p className="modal-subtitle">{subtitle}</p>}
      <div className="modal-actions">
        <Button variant="primary" onClick={onNewGame}>
          New game
        </Button>
      </div>
    </Modal>
  );
}
