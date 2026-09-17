import { Bot, User } from 'lucide-react';
import { useGameStore } from '../../state/gameStore';
import { CapturedPieces } from './CapturedPieces';
import './panels.css';

function formatClock(ms: number) {
  const total = Math.ceil(ms / 1000);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

interface Props {
  side: 'top' | 'bottom';
}

export function PlayerBar({ side }: Props) {
  const playerColor = useGameStore((s) => s.playerColor);
  const mode = useGameStore((s) => s.mode);
  const elo = useGameStore((s) => s.elo);
  const whiteMs = useGameStore((s) => s.whiteMs);
  const blackMs = useGameStore((s) => s.blackMs);
  const fen = useGameStore((s) => s.fen);
  const turn = fen.split(' ')[1];

  const isTopWhite = playerColor === 'b';
  const color: 'w' | 'b' = side === 'top' ? (isTopWhite ? 'w' : 'b') : isTopWhite ? 'b' : 'w';
  const isEngine = mode === 'pve' && color !== playerColor;
  const ms = color === 'w' ? whiteMs : blackMs;
  const isActive = turn === color;

  return (
    <div className={`player-bar ${isActive ? 'active' : ''}`}>
      <div className="player-identity">
        <span className={`player-avatar ${color}`}>{isEngine ? <Bot size={16} /> : <User size={16} />}</span>
        <div className="player-meta">
          <span className="player-name">
            {isEngine ? `Engine · ${elo} ELO` : 'You'} <span className="player-color-dot">{color === 'w' ? '○' : '●'}</span>
          </span>
          <CapturedPieces color={color} />
        </div>
      </div>
      <span className="player-clock mono">{formatClock(ms)}</span>
    </div>
  );
}
