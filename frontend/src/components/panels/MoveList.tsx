import { useEffect, useRef } from 'react';
import { useGameStore } from '../../state/gameStore';
import './panels.css';

export function MoveList() {
  const history = useGameStore((s) => s.history);
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [history.length]);

  const rows: { number: number; white?: string; black?: string }[] = [];
  history.forEach((move, i) => {
    if (i % 2 === 0) {
      rows.push({ number: move.moveNumber, white: move.san });
    } else {
      rows[rows.length - 1].black = move.san;
    }
  });

  return (
    <div className="panel">
      <div className="panel-header">Moves</div>
      <div className="move-list" ref={listRef}>
        {rows.length === 0 && <p className="panel-empty">No moves yet — make the first move on the board.</p>}
        {rows.map((row) => (
          <div className="move-row" key={row.number}>
            <span className="move-num">{row.number}.</span>
            <span className="move-san">{row.white}</span>
            <span className="move-san">{row.black ?? ''}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
