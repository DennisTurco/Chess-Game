import './pages.css';

const MOCK_GAMES = [
  { date: '2026-09-16', opponent: 'Engine · 1600 ELO', result: 'win', moves: 34, opening: 'Ruy Lopez' },
  { date: '2026-09-14', opponent: 'Engine · 1200 ELO', result: 'win', moves: 27, opening: "Queen's Gambit" },
  { date: '2026-09-12', opponent: 'Local player', result: 'draw', moves: 41, opening: 'Sicilian Defense' },
  { date: '2026-09-10', opponent: 'Engine · 1800 ELO', result: 'loss', moves: 22, opening: "King's Indian" },
  { date: '2026-09-08', opponent: 'Engine · 1200 ELO', result: 'win', moves: 30, opening: 'Italian Game' },
];

const RESULT_LABEL: Record<string, string> = { win: 'Win', loss: 'Loss', draw: 'Draw' };

export function HistoryPage() {
  const wins = MOCK_GAMES.filter((g) => g.result === 'win').length;
  const losses = MOCK_GAMES.filter((g) => g.result === 'loss').length;
  const draws = MOCK_GAMES.filter((g) => g.result === 'draw').length;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title serif">History</h1>
          <p className="page-subtitle">Sample data — this will reflect your real games once saved results are wired up.</p>
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-value">{MOCK_GAMES.length}</div>
          <div className="stat-label">Games played</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{wins}</div>
          <div className="stat-label">Wins</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{losses}</div>
          <div className="stat-label">Losses</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{draws}</div>
          <div className="stat-label">Draws</div>
        </div>
      </div>

      <table className="history-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Opponent</th>
            <th>Opening</th>
            <th>Moves</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {MOCK_GAMES.map((g, i) => (
            <tr key={i}>
              <td>{g.date}</td>
              <td>{g.opponent}</td>
              <td>{g.opening}</td>
              <td>{g.moves}</td>
              <td>
                <span className={`result-pill result-${g.result}`}>{RESULT_LABEL[g.result]}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
