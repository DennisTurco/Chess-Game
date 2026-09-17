import { useEffect, useState } from 'react';
import { ChessBoard } from '../components/board/ChessBoard';
import { EvalBar } from '../components/board/EvalBar';
import { PlayerBar } from '../components/panels/PlayerBar';
import { MoveList } from '../components/panels/MoveList';
import { TutorPanel } from '../components/panels/TutorPanel';
import { GameControls } from '../components/panels/GameControls';
import { NewGameModal } from '../components/modals/NewGameModal';
import { GameOverModal } from '../components/modals/GameOverModal';
import { useGameStore } from '../state/gameStore';
import './pages.css';

export function PlayPage() {
  const status = useGameStore((s) => s.status);
  const tick = useGameStore((s) => s.tick);
  const checkBackend = useGameStore((s) => s.checkBackend);
  const evalScore = useGameStore((s) => s.evalScore);
  const playerColor = useGameStore((s) => s.playerColor);
  const [modalOpen, setModalOpen] = useState(status === 'idle');

  useEffect(() => {
    if (status === 'idle') setModalOpen(true);
  }, [status]);

  useEffect(() => {
    checkBackend();
  }, [checkBackend]);

  useEffect(() => {
    const interval = setInterval(() => tick(200), 200);
    return () => clearInterval(interval);
  }, [tick]);

  return (
    <div className="page play-page">
      <div className="page-header">
        <div>
          <h1 className="page-title serif">Play</h1>
          <p className="page-subtitle">Every move gets a coach's comment — great for learning as you go.</p>
        </div>
      </div>

      <div className="play-layout">
        <div className="play-board-col">
          <PlayerBar side="top" />
          <div className="board-row">
            <EvalBar score={evalScore} flip={playerColor === 'b'} />
            <ChessBoard />
          </div>
          <PlayerBar side="bottom" />
          <GameControls onNewGame={() => setModalOpen(true)} />
        </div>

        <div className="play-side-col">
          <TutorPanel />
          <MoveList />
        </div>
      </div>

      <NewGameModal open={modalOpen} onClose={() => setModalOpen(false)} />
      <GameOverModal onNewGame={() => setModalOpen(true)} />
    </div>
  );
}
