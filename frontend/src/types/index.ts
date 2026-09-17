export type GameMode = 'pvp' | 'pve';

export type PlayerColor = 'w' | 'b';

export type MoveQuality =
  | 'brilliant'
  | 'great'
  | 'good'
  | 'book'
  | 'inaccuracy'
  | 'mistake'
  | 'blunder';

export interface MoveRecord {
  san: string;
  uci: string;
  fenBefore: string;
  fenAfter: string;
  color: PlayerColor;
  moveNumber: number;
  captured?: string;
  quality?: MoveQuality;
  comment?: string;
  isCheck: boolean;
  isCapture: boolean;
  flags: string;
  /** Position evaluation after the move, in pawns, from White's perspective. */
  score?: number;
}

export interface TutorTip {
  quality: MoveQuality;
  headline: string;
  comment: string;
  /** Position evaluation, in pawns, from White's perspective. */
  score?: number;
}

export type BoardTheme = 'olive' | 'walnut' | 'slate' | 'coral';
export type PieceSet = 'classic';

export interface AppSettings {
  theme: 'dark' | 'light';
  boardTheme: BoardTheme;
  soundEnabled: boolean;
  showCoordinates: boolean;
  showLegalMoves: boolean;
  autoPromoteQueen: boolean;
  animationSpeed: 'off' | 'fast' | 'normal';
}

export interface EloOption {
  value: number;
  label: string;
}
