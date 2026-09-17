import { BookOpen, Puzzle, Target, Swords, Shield, Crown } from 'lucide-react';
import './pages.css';

const LESSONS = [
  {
    icon: BookOpen,
    title: 'Opening principles',
    desc: 'Control the center, develop your pieces, and castle early. The foundation for every game.',
    tag: 'Fundamentals',
  },
  {
    icon: Puzzle,
    title: 'Tactical patterns',
    desc: 'Forks, pins, skewers and discovered attacks — recognize them before they cost you material.',
    tag: 'Tactics',
  },
  {
    icon: Target,
    title: 'Endgame technique',
    desc: 'King and pawn endings, opposition, and the rule of the square.',
    tag: 'Endgame',
  },
  {
    icon: Swords,
    title: 'Attacking the king',
    desc: 'Build an attack safely: open lines, bring pieces closer, and time the sacrifice.',
    tag: 'Middlegame',
  },
  {
    icon: Shield,
    title: 'Defensive resources',
    desc: 'Prophylaxis, piece trades, and fortress positions to hold a difficult position.',
    tag: 'Strategy',
  },
  {
    icon: Crown,
    title: 'Famous games',
    desc: 'Walk through legendary games annotated move by move.',
    tag: 'History',
  },
];

export function LearnPage() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title serif">Learn</h1>
          <p className="page-subtitle">Lessons the tutor will unlock as it learns your playing style.</p>
        </div>
      </div>

      <div className="card-grid">
        {LESSONS.map(({ icon: Icon, title, desc, tag }) => (
          <div className="info-card" key={title}>
            <span className="info-card-icon">
              <Icon size={20} strokeWidth={1.75} />
            </span>
            <span className="info-card-tag">{tag}</span>
            <span className="info-card-title">{title}</span>
            <p className="info-card-desc">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
