import { Lightbulb, Sparkles } from 'lucide-react';
import { useMemo } from 'react';
import { useGameStore } from '../../state/gameStore';
import type { MoveRecord, PlayerColor } from '../../types';
import { QualityBadge } from '../common/Badge';
import { Button } from '../common/Button';
import './panels.css';

function CoachSide({ color, move }: { color: PlayerColor; move: MoveRecord | undefined }) {
  return (
    <div className="coach-side">
      <div className="coach-side-header">
        <span className={`coach-side-dot ${color}`} />
        <span>{color === 'w' ? 'White' : 'Black'}</span>
        {move && <span className="coach-side-san mono">{move.san}</span>}
      </div>
      {move ? (
        <>
          {move.quality && <QualityBadge quality={move.quality} />}
          <p className="tutor-comment">{move.comment}</p>
        </>
      ) : (
        <p className="panel-empty">No move played yet.</p>
      )}
    </div>
  );
}

export function TutorPanel() {
  const history = useGameStore((s) => s.history);
  const requestHint = useGameStore((s) => s.requestHint);
  const hintMove = useGameStore((s) => s.hintMove);
  const status = useGameStore((s) => s.status);
  const backendAvailable = useGameStore((s) => s.backendAvailable);

  const lastWhiteMove = useMemo(() => [...history].reverse().find((m) => m.color === 'w'), [history]);
  const lastBlackMove = useMemo(() => [...history].reverse().find((m) => m.color === 'b'), [history]);

  return (
    <div className="panel tutor-panel">
      <div className="panel-header">
        <Sparkles size={15} />
        <span>Coach</span>
        <span className={`backend-dot ${backendAvailable ? 'on' : backendAvailable === false ? 'off' : ''}`} />
        <span className="backend-label">
          {backendAvailable === null ? 'Checking engine…' : backendAvailable ? 'Stockfish connected' : 'Offline mode'}
        </span>
      </div>

      {history.length === 0 ? (
        <p className="panel-empty">
          Play a move and your coach will comment on it here, separately for White and Black. This feedback is a
          placeholder until the Stockfish backend is connected.
        </p>
      ) : (
        <div className="coach-columns">
          <CoachSide color="w" move={lastWhiteMove} />
          <CoachSide color="b" move={lastBlackMove} />
        </div>
      )}

      <Button
        variant="secondary"
        size="sm"
        icon={<Lightbulb size={15} />}
        onClick={requestHint}
        disabled={status !== 'playing' || !!hintMove}
        fullWidth
      >
        {hintMove ? 'Hint shown on board' : 'Suggest a move'}
      </Button>
    </div>
  );
}
