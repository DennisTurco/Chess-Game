type SoundKind = 'move' | 'capture' | 'check';

const cache: Partial<Record<SoundKind, HTMLAudioElement>> = {};

function getAudio(kind: SoundKind): HTMLAudioElement {
  if (!cache[kind]) {
    const src = kind === 'capture' ? '/sounds/capture.wav' : '/sounds/move.wav';
    cache[kind] = new Audio(src);
  }
  return cache[kind]!;
}

export function playSound(kind: SoundKind) {
  try {
    const enabled = JSON.parse(localStorage.getItem('chess-tutor:settings') ?? '{}').soundEnabled;
    if (enabled === false) return;
    const audio = getAudio(kind);
    audio.currentTime = 0;
    void audio.play().catch(() => {});
  } catch {
    /* ignore */
  }
}
