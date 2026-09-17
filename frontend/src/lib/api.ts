import type { MoveQuality, TutorTip } from '../types';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:5000';

const QUALITY_MAP: Record<string, MoveQuality> = {
  'Brilliant move': 'brilliant',
  'Great move': 'great',
  'Good move': 'good',
  Inaccuracy: 'inaccuracy',
  Mistake: 'mistake',
  Blunder: 'blunder',
  'Illegal move': 'good',
};

export class ApiError extends Error {}

async function postJson<T>(path: string, body: unknown, timeoutMs = 4000): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new ApiError(detail.error ?? `Request to ${path} failed (${res.status})`);
    }
    return (await res.json()) as T;
  } finally {
    clearTimeout(timer);
  }
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
}

export interface BestMoveResponse {
  uci: string;
  skill: number;
}

export async function fetchBestMove(fen: string, elo: number, timeLimit = 0.5): Promise<BestMoveResponse> {
  return postJson<BestMoveResponse>('/api/best-move', { fen, elo, timeLimit }, 6000);
}

interface MoveCommentResponse {
  score: number;
  quality: string;
  comment: string;
  best: string;
}

export async function fetchMoveComment(fenBefore: string, move: string, elo: number): Promise<TutorTip> {
  const data = await postJson<MoveCommentResponse>('/api/move-comment', { fenBefore, move, elo }, 6000);
  return {
    quality: QUALITY_MAP[data.quality] ?? 'good',
    headline: data.quality,
    comment: `${data.comment} (eval ${data.score > 0 ? '+' : ''}${data.score.toFixed(2)})`,
    score: data.score,
  };
}
