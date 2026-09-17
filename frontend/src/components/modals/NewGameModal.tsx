import { useState } from 'react';
import { Modal } from '../common/Modal';
import { Button } from '../common/Button';
import { useGameStore } from '../../state/gameStore';
import type { GameMode, PlayerColor } from '../../types';
import './modals.css';

const ELO_OPTIONS = [400, 600, 800, 1000, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000];

interface Props {
  open: boolean;
  onClose: () => void;
}

export function NewGameModal({ open, onClose }: Props) {
  const startGame = useGameStore((s) => s.startGame);
  const [mode, setMode] = useState<GameMode>('pve');
  const [elo, setElo] = useState(1200);
  const [color, setColor] = useState<PlayerColor>('w');

  const handleStart = () => {
    startGame(mode, elo, color);
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <h2 className="serif modal-title">New game</h2>
      <p className="modal-subtitle">Set up the mode and difficulty, then jump in.</p>

      <div className="modal-section">
        <span className="modal-label">Mode</span>
        <div className="segmented">
          <button className={mode === 'pvp' ? 'active' : ''} onClick={() => setMode('pvp')}>
            Player vs Player
          </button>
          <button className={mode === 'pve' ? 'active' : ''} onClick={() => setMode('pve')}>
            Player vs Engine
          </button>
        </div>
      </div>

      {mode === 'pve' && (
        <div className="modal-section">
          <span className="modal-label">Engine difficulty (ELO)</span>
          <select className="select" value={elo} onChange={(e) => setElo(Number(e.target.value))}>
            {ELO_OPTIONS.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="modal-section">
        <span className="modal-label">Play as</span>
        <div className="segmented">
          <button className={color === 'w' ? 'active' : ''} onClick={() => setColor('w')}>
            White
          </button>
          <button className={color === 'b' ? 'active' : ''} onClick={() => setColor('b')}>
            Black
          </button>
        </div>
      </div>

      <div className="modal-actions">
        <Button variant="ghost" onClick={onClose}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleStart}>
          Start game
        </Button>
      </div>
    </Modal>
  );
}
