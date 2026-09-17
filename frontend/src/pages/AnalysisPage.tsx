import { useMemo, useState } from 'react';
import { Chess } from 'chess.js';
import { ChevronFirst, ChevronLast, ChevronLeft, ChevronRight } from 'lucide-react';
import { ChessBoard } from '../components/board/ChessBoard';
import { Button } from '../components/common/Button';
import { QualityBadge } from '../components/common/Badge';
import { evaluateMoveLocally } from '../lib/tutor';
import type { MoveQuality } from '../types';
import './pages.css';

const SAMPLE_PGN = '1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O';

interface AnalyzedMove {
  san: string;
  fen: string;
  quality: MoveQuality;
}

function analyzePgn(pgn: string): AnalyzedMove[] {
  const replay = new Chess();
  try {
    replay.loadPgn(pgn);
  } catch {
    return [];
  }
  const sanMoves = replay.history();

  const chess = new Chess();
  const result: AnalyzedMove[] = [];
  for (const san of sanMoves) {
    const move = chess.move(san);
    if (!move) break;
    const tip = evaluateMoveLocally(chess, move);
    result.push({ san: move.san, fen: chess.fen(), quality: tip.quality });
  }
  return result;
}

export function AnalysisPage() {
  const [pgn, setPgn] = useState(SAMPLE_PGN);
  const moves = useMemo(() => analyzePgn(pgn), [pgn]);
  const [index, setIndex] = useState(-1);

  const fen = index === -1 ? new Chess().fen() : moves[index]?.fen ?? new Chess().fen();
  const clampedIndex = Math.min(index, moves.length - 1);

  return (
    <div className="page analysis-page">
      <div className="page-header">
        <div>
          <h1 className="page-title serif">Analysis</h1>
          <p className="page-subtitle">Paste a PGN and step through it move by move with coach annotations.</p>
        </div>
      </div>

      <div className="analysis-layout">
        <div className="play-board-col">
          <ChessBoard fen={fen} interactive={false} orientation="w" />
          <div className="analysis-controls">
            <Button variant="secondary" size="sm" icon={<ChevronFirst size={15} />} onClick={() => setIndex(-1)}>
              Start
            </Button>
            <Button
              variant="secondary"
              size="sm"
              icon={<ChevronLeft size={15} />}
              onClick={() => setIndex((i) => Math.max(-1, i - 1))}
            >
              Prev
            </Button>
            <Button
              variant="secondary"
              size="sm"
              icon={<ChevronRight size={15} />}
              onClick={() => setIndex((i) => Math.min(moves.length - 1, i + 1))}
            >
              Next
            </Button>
            <Button
              variant="secondary"
              size="sm"
              icon={<ChevronLast size={15} />}
              onClick={() => setIndex(moves.length - 1)}
            >
              End
            </Button>
          </div>
        </div>

        <div className="play-side-col">
          <div className="panel">
            <div className="panel-header">Import PGN</div>
            <textarea
              className="pgn-input"
              value={pgn}
              onChange={(e) => {
                setPgn(e.target.value);
                setIndex(-1);
              }}
              placeholder="Paste a PGN move list here…"
            />
          </div>

          <div className="panel">
            <div className="panel-header">Moves</div>
            <div className="move-list">
              {moves.length === 0 && <p className="panel-empty">Could not parse this PGN — check the notation.</p>}
              {moves.map((m, i) => (
                <button
                  key={i}
                  className="move-row"
                  style={{
                    background: i === clampedIndex ? 'var(--accent-soft)' : undefined,
                    gridTemplateColumns: '28px 1fr auto',
                    alignItems: 'center',
                  }}
                  onClick={() => setIndex(i)}
                >
                  <span className="move-num">{Math.floor(i / 2) + 1}.</span>
                  <span className="move-san">{m.san}</span>
                  <QualityBadge quality={m.quality} />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
