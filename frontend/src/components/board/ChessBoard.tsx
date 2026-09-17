import { Chess, type Color, type Square } from 'chess.js';
import { useEffect, useMemo, useRef, useState, type MouseEvent as ReactMouseEvent, type PointerEvent as ReactPointerEvent, type RefObject } from 'react';
import { QUALITY_ICONS } from '../common/Badge';
import { useGameStore } from '../../state/gameStore';
import type { MoveQuality } from '../../types';
import { useSettingsStore } from '../../state/settingsStore';
import { FILES, RANKS, squareFromPoint, squareToXY } from './boardGeometry';
import { pieceImageSrc } from './pieceImage';
import { applyMoveToPieces, piecesFromFen, type PieceInstance } from './pieceInstances';
import { PromotionDialog } from './PromotionDialog';
import './board.css';

interface ChessBoardProps {
  fen?: string;
  interactive?: boolean;
  orientation?: 'w' | 'b';
}

interface Arrow {
  from: Square;
  to: Square;
}

const DRAG_THRESHOLD = 4;
const CELL_PCT = 12.5;
const PIECE_PCT = 11;
const PIECE_INSET = (CELL_PCT - PIECE_PCT) / 2;
const CHIP_PCT = 4.6;
const CHIP_INSET = 0.9;

export function ChessBoard({ fen, interactive = true, orientation }: ChessBoardProps) {
  const storeFen = useGameStore((s) => s.fen);
  const history = useGameStore((s) => s.history);
  const playerColor = useGameStore((s) => s.playerColor);
  const selectedSquare = useGameStore((s) => s.selectedSquare);
  const legalTargets = useGameStore((s) => s.legalTargets);
  const lastMove = useGameStore((s) => s.lastMove);
  const hintMove = useGameStore((s) => s.hintMove);
  const pendingPromotion = useGameStore((s) => s.pendingPromotion);
  const selectSquareAction = useGameStore((s) => s.selectSquare);
  const beginDrag = useGameStore((s) => s.beginDrag);
  const attemptMove = useGameStore((s) => s.attemptMove);

  const boardTheme = useSettingsStore((s) => s.boardTheme);
  const showCoordinates = useSettingsStore((s) => s.showCoordinates);
  const showLegalMoves = useSettingsStore((s) => s.showLegalMoves);
  const animationSpeed = useSettingsStore((s) => s.animationSpeed);

  const isLive = fen === undefined;
  const displayFen = fen ?? storeFen;
  const chess = useMemo(() => new Chess(displayFen), [displayFen]);
  const board = useMemo(() => chess.board(), [chess]);
  const inCheckColor = chess.isCheck() ? chess.turn() : null;

  const flip = (orientation ?? playerColor) === 'b';
  const files = flip ? [...FILES].reverse() : FILES;
  const ranks = flip ? [...RANKS].reverse() : RANKS;

  const boardRef = useRef<HTMLDivElement>(null);

  // --- Animated piece layer -------------------------------------------------
  const [pieces, setPieces] = useState<PieceInstance[]>(() => piecesFromFen(displayFen));
  const prevHistoryLenRef = useRef(-1);

  useEffect(() => {
    if (isLive) {
      const newLen = history.length;
      if (newLen === 0 || newLen !== prevHistoryLenRef.current + 1) {
        setPieces(piecesFromFen(displayFen));
      } else {
        setPieces((prev) => applyMoveToPieces(prev, history[newLen - 1]));
      }
      prevHistoryLenRef.current = newLen;
    } else {
      setPieces(piecesFromFen(displayFen));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [displayFen, isLive, history.length]);

  // --- Drag & drop -----------------------------------------------------------
  const [dragSquare, setDragSquare] = useState<Square | null>(null);
  const [dragPos, setDragPos] = useState<{ x: number; y: number } | null>(null);
  const dragCandidateRef = useRef<{ square: Square; startX: number; startY: number; color: Color } | null>(null);
  const suppressNextClickRef = useRef(false);

  useEffect(() => {
    if (!interactive) return;

    function onMove(e: PointerEvent) {
      const cand = dragCandidateRef.current;
      if (!cand) return;
      const dx = e.clientX - cand.startX;
      const dy = e.clientY - cand.startY;
      if (dragSquare === null) {
        if (Math.hypot(dx, dy) < DRAG_THRESHOLD) return;
        if (!beginDrag(cand.square)) {
          dragCandidateRef.current = null;
          return;
        }
        setDragSquare(cand.square);
      }
      setDragPos({ x: e.clientX, y: e.clientY });
    }

    function onUp(e: PointerEvent) {
      const cand = dragCandidateRef.current;
      dragCandidateRef.current = null;
      if (!cand || dragSquare === null) return;

      setDragSquare(null);
      setDragPos(null);

      const rect = boardRef.current?.getBoundingClientRect();
      const target = rect ? squareFromPoint(rect, e.clientX, e.clientY, flip) : null;
      if (target && target !== cand.square) {
        suppressNextClickRef.current = true;
        attemptMove(cand.square, target);
      }
    }

    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    return () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
    };
  }, [interactive, dragSquare, flip, beginDrag, attemptMove]);

  function handlePiecePointerDown(e: ReactPointerEvent, square: Square, color: Color) {
    if (e.button !== 0) return; // only the primary/left button drags pieces; right button draws arrows
    if (!interactive) return;
    if (color !== chess.turn()) return;
    e.preventDefault();
    dragCandidateRef.current = { square, startX: e.clientX, startY: e.clientY, color };
  }

  function handlePieceClick(square: Square) {
    if (suppressNextClickRef.current) {
      suppressNextClickRef.current = false;
      return;
    }
    if (interactive) selectSquareAction(square);
  }

  // --- Right-click arrows ------------------------------------------------
  const [arrows, setArrows] = useState<Arrow[]>([]);
  const [highlighted, setHighlighted] = useState<Square[]>([]);
  const [draftArrow, setDraftArrow] = useState<{ from: Square; x: number; y: number } | null>(null);
  const rightDragRef = useRef<Square | null>(null);

  useEffect(() => {
    if (!isLive) return;
    setArrows([]);
    setHighlighted([]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [displayFen, isLive]);

  useEffect(() => {
    function onMove(e: MouseEvent) {
      if (!rightDragRef.current || !boardRef.current) return;
      setDraftArrow({ from: rightDragRef.current, x: e.clientX, y: e.clientY });
    }
    function onUp(e: MouseEvent) {
      const from = rightDragRef.current;
      rightDragRef.current = null;
      setDraftArrow(null);
      if (!from || !boardRef.current) return;
      const rect = boardRef.current.getBoundingClientRect();
      const to = squareFromPoint(rect, e.clientX, e.clientY, flip);
      if (!to) return;
      if (to === from) {
        setHighlighted((prev) => (prev.includes(from) ? prev.filter((s) => s !== from) : [...prev, from]));
      } else {
        setArrows((prev) => {
          const exists = prev.some((a) => a.from === from && a.to === to);
          return exists ? prev.filter((a) => !(a.from === from && a.to === to)) : [...prev, { from, to }];
        });
      }
    }
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, [flip]);

  function handleBoardMouseDown(e: ReactMouseEvent) {
    if (e.button !== 2) return;
    e.preventDefault();
    const rect = boardRef.current?.getBoundingClientRect();
    if (!rect) return;
    const square = squareFromPoint(rect, e.clientX, e.clientY, flip);
    if (square) rightDragRef.current = square;
  }

  const speedClass = animationSpeed === 'off' ? 'anim-off' : animationSpeed === 'fast' ? 'anim-fast' : '';
  const lastMoveQuality = isLive ? history.at(-1)?.quality : undefined;

  return (
    <div className="board-wrap" data-board-theme={boardTheme}>
      <div
        className={`board-grid ${speedClass}`}
        ref={boardRef}
        onMouseDown={handleBoardMouseDown}
        onContextMenu={(e) => e.preventDefault()}
      >
        {ranks.map((rank, rowIdx) =>
          files.map((file, colIdx) => {
            const square = `${file}${rank}` as Square;
            const isDark = (rowIdx + colIdx) % 2 === 1;
            const rankIndex = RANKS.indexOf(rank);
            const fileIndex = FILES.indexOf(file);
            const cell = board[rankIndex][fileIndex];

            const isSelected = selectedSquare === square;
            const isLegalTarget = legalTargets.includes(square);
            const isLastMove = lastMove && (lastMove.from === square || lastMove.to === square);
            const isKingInCheck = cell?.type === 'k' && cell.color === inCheckColor;
            const isMarked = highlighted.includes(square);

            return (
              <button
                key={square}
                className={[
                  'board-sq',
                  isDark ? 'dark' : 'light',
                  isSelected ? 'selected' : '',
                  isLastMove ? 'last-move' : '',
                  isKingInCheck ? 'in-check' : '',
                  isMarked ? 'marked' : '',
                ]
                  .filter(Boolean)
                  .join(' ')}
                onClick={() => interactive && selectSquareAction(square)}
                disabled={!interactive}
                type="button"
              >
                {showCoordinates && colIdx === 0 && <span className="coord coord-rank">{rank}</span>}
                {showCoordinates && rowIdx === 7 && <span className="coord coord-file">{file}</span>}
                {showLegalMoves && isLegalTarget && <span className={`move-marker ${cell ? 'capture' : 'empty'}`} />}
              </button>
            );
          }),
        )}

        <div className="piece-layer">
          {pieces.map((p) => {
            const { col, row } = squareToXY(p.square, flip);
            const isBeingDragged = dragSquare === p.square;
            return (
              <img
                key={p.id}
                src={pieceImageSrc(p.color, p.type)}
                className={`anim-piece ${isBeingDragged ? 'is-dragging-source' : ''}`}
                style={{ left: `${col * CELL_PCT + PIECE_INSET}%`, top: `${row * CELL_PCT + PIECE_INSET}%` }}
                draggable={false}
                onPointerDown={(e) => handlePiecePointerDown(e, p.square, p.color)}
                onClick={() => handlePieceClick(p.square)}
                alt={`${p.color}${p.type}`}
              />
            );
          })}
        </div>

        {lastMoveQuality && lastMove && (
          <MoveQualityMarker square={lastMove.to} quality={lastMoveQuality} flip={flip} />
        )}

        {dragSquare && dragPos && boardRef.current && (
          <img
            className="anim-piece drag-ghost"
            src={pieceImageSrc(chess.get(dragSquare)?.color ?? 'w', chess.get(dragSquare)?.type ?? 'p')}
            style={{
              left: dragPos.x - boardRef.current.getBoundingClientRect().left,
              top: dragPos.y - boardRef.current.getBoundingClientRect().top,
            }}
            draggable={false}
            alt=""
          />
        )}

        <ArrowLayer arrows={arrows} draft={draftArrow} hint={hintMove} boardRef={boardRef} flip={flip} />
      </div>

      {pendingPromotion && interactive && <PromotionDialog />}
    </div>
  );
}

function MoveQualityMarker({ square, quality, flip }: { square: Square; quality: MoveQuality; flip: boolean }) {
  const { col, row } = squareToXY(square, flip);
  const Icon = QUALITY_ICONS[quality];
  return (
    <span
      className={`quality-chip board-quality-chip badge-${quality}`}
      style={{
        left: `${col * CELL_PCT + (CELL_PCT - CHIP_PCT - CHIP_INSET)}%`,
        top: `${row * CELL_PCT + CHIP_INSET}%`,
      }}
    >
      <Icon size={12} strokeWidth={2.75} />
    </span>
  );
}

function ArrowLayer({
  arrows,
  draft,
  hint,
  boardRef,
  flip,
}: {
  arrows: Arrow[];
  draft: { from: Square; x: number; y: number } | null;
  hint: { from: Square; to: Square } | null;
  boardRef: RefObject<HTMLDivElement | null>;
  flip: boolean;
}) {
  const rect = boardRef.current?.getBoundingClientRect();

  function center(square: Square) {
    const { col, row } = squareToXY(square, flip);
    return { x: (col + 0.5) * 12.5, y: (row + 0.5) * 12.5 };
  }

  const draftLine =
    draft && rect
      ? {
          from: center(draft.from),
          to: { x: ((draft.x - rect.left) / rect.width) * 100, y: ((draft.y - rect.top) / rect.height) * 100 },
        }
      : null;

  if (arrows.length === 0 && !draftLine && !hint) return null;

  return (
    <svg className="arrow-layer" viewBox="0 0 100 100" preserveAspectRatio="none">
      <defs>
        <marker id="arrowhead" markerWidth="3" markerHeight="3" refX="1.4" refY="1.5" orient="auto">
          <path d="M0,0 L3,1.5 L0,3 Z" fill="var(--accent)" />
        </marker>
        <marker id="hint-arrowhead" markerWidth="3" markerHeight="3" refX="1.4" refY="1.5" orient="auto">
          <path d="M0,0 L3,1.5 L0,3 Z" fill="var(--info)" />
        </marker>
      </defs>
      {arrows.map((a, i) => {
        const from = center(a.from);
        const to = center(a.to);
        return (
          <line
            key={i}
            x1={from.x}
            y1={from.y}
            x2={to.x}
            y2={to.y}
            stroke="var(--accent)"
            strokeWidth={1.6}
            strokeLinecap="round"
            opacity={0.85}
            markerEnd="url(#arrowhead)"
          />
        );
      })}
      {draftLine && (
        <line
          x1={draftLine.from.x}
          y1={draftLine.from.y}
          x2={draftLine.to.x}
          y2={draftLine.to.y}
          stroke="var(--accent)"
          strokeWidth={1.6}
          strokeLinecap="round"
          opacity={0.5}
        />
      )}
      {hint &&
        (() => {
          const from = center(hint.from);
          const to = center(hint.to);
          return (
            <line
              className="hint-arrow"
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke="var(--info)"
              strokeWidth={1.6}
              strokeLinecap="round"
              opacity={0.85}
              markerEnd="url(#hint-arrowhead)"
            />
          );
        })()}
    </svg>
  );
}
