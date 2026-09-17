import './evalbar.css';

interface EvalBarProps {
  score: number;
  /** Flip like the board, so each side's fill grows from its own edge. */
  flip?: boolean;
}

function formatEval(score: number): string {
  if (Math.abs(score) >= 50) return score > 0 ? 'M' : '-M';
  const rounded = score.toFixed(1);
  return score > 0 ? `+${rounded}` : rounded;
}

export function EvalBar({ score, flip = false }: EvalBarProps) {
  const whiteWinProb = 1 / (1 + Math.exp(-0.4 * score));
  const whitePct = Math.min(97, Math.max(3, whiteWinProb * 100));
  const blackPct = 100 - whitePct;
  const label = formatEval(score);

  const top = flip
    ? { className: 'eval-bar-white', pct: whitePct }
    : { className: 'eval-bar-black', pct: blackPct };
  const bottom = flip
    ? { className: 'eval-bar-black', pct: blackPct }
    : { className: 'eval-bar-white', pct: whitePct };

  return (
    <div className="eval-bar" title={`Evaluation: ${label}`}>
      <div className={top.className} style={{ height: `${top.pct}%` }} />
      <div className={bottom.className} style={{ height: `${bottom.pct}%` }} />
      <span className="eval-bar-label" style={{ top: `${top.pct}%` }}>
        {label}
      </span>
    </div>
  );
}
