import { BookOpen, CircleAlert, CircleCheck, Gem, Skull, Star, TriangleAlert } from 'lucide-react';
import type { ComponentType } from 'react';
import type { MoveQuality } from '../../types';
import './common.css';

const LABELS: Record<MoveQuality, string> = {
  brilliant: 'Brilliant',
  great: 'Great',
  good: 'Good',
  book: 'Book',
  inaccuracy: 'Inaccuracy',
  mistake: 'Mistake',
  blunder: 'Blunder',
};

export const QUALITY_ICONS: Record<MoveQuality, ComponentType<{ size?: number; strokeWidth?: number }>> = {
  brilliant: Gem,
  great: Star,
  good: CircleCheck,
  book: BookOpen,
  inaccuracy: TriangleAlert,
  mistake: CircleAlert,
  blunder: Skull,
};

export function QualityBadge({ quality }: { quality: MoveQuality }) {
  const Icon = QUALITY_ICONS[quality];
  return (
    <span className={`badge badge-${quality}`}>
      <Icon size={13} strokeWidth={2.25} />
      {LABELS[quality]}
    </span>
  );
}

/** Small round chip for overlaying a square, e.g. on the destination of the last move. */
export function MoveQualityChip({ quality }: { quality: MoveQuality }) {
  const Icon = QUALITY_ICONS[quality];
  return (
    <span className={`quality-chip badge-${quality}`}>
      <Icon size={11} strokeWidth={2.75} />
    </span>
  );
}
