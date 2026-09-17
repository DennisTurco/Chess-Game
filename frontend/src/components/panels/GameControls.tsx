import { Flag, RotateCcw, Plus } from 'lucide-react';
import { useGameStore } from '../../state/gameStore';
import { Button } from '../common/Button';
import './panels.css';

interface Props {
  onNewGame: () => void;
}

export function GameControls({ onNewGame }: Props) {
  const undo = useGameStore((s) => s.undo);
  const resign = useGameStore((s) => s.resign);
  const status = useGameStore((s) => s.status);
  const history = useGameStore((s) => s.history);

  return (
    <div className="game-controls">
      <Button variant="secondary" size="sm" icon={<RotateCcw size={15} />} onClick={undo} disabled={history.length === 0}>
        Undo
      </Button>
      <Button
        variant="danger"
        size="sm"
        icon={<Flag size={15} />}
        onClick={resign}
        disabled={status !== 'playing'}
      >
        Resign
      </Button>
      <Button variant="primary" size="sm" icon={<Plus size={15} />} onClick={onNewGame}>
        New game
      </Button>
    </div>
  );
}
