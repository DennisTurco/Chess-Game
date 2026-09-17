import { create } from 'zustand';
import type { AppSettings, BoardTheme } from '../types';

const STORAGE_KEY = 'chess-tutor:settings';

const defaultSettings: AppSettings = {
  theme: 'dark',
  boardTheme: 'olive',
  soundEnabled: true,
  showCoordinates: true,
  showLegalMoves: true,
  autoPromoteQueen: false,
  animationSpeed: 'normal',
};

function loadSettings(): AppSettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultSettings;
    return { ...defaultSettings, ...JSON.parse(raw) };
  } catch {
    return defaultSettings;
  }
}

function persist(settings: AppSettings) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    /* ignore */
  }
}

interface SettingsState extends AppSettings {
  setTheme: (theme: AppSettings['theme']) => void;
  toggleTheme: () => void;
  setBoardTheme: (theme: BoardTheme) => void;
  toggleSound: () => void;
  toggleCoordinates: () => void;
  toggleLegalMoves: () => void;
  toggleAutoPromote: () => void;
  setAnimationSpeed: (speed: AppSettings['animationSpeed']) => void;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  ...loadSettings(),
  setTheme: (theme) => {
    set({ theme });
    persist({ ...get(), theme });
  },
  toggleTheme: () => {
    const theme = get().theme === 'dark' ? 'light' : 'dark';
    set({ theme });
    persist({ ...get(), theme });
  },
  setBoardTheme: (boardTheme) => {
    set({ boardTheme });
    persist({ ...get(), boardTheme });
  },
  toggleSound: () => {
    const soundEnabled = !get().soundEnabled;
    set({ soundEnabled });
    persist({ ...get(), soundEnabled });
  },
  toggleCoordinates: () => {
    const showCoordinates = !get().showCoordinates;
    set({ showCoordinates });
    persist({ ...get(), showCoordinates });
  },
  toggleLegalMoves: () => {
    const showLegalMoves = !get().showLegalMoves;
    set({ showLegalMoves });
    persist({ ...get(), showLegalMoves });
  },
  toggleAutoPromote: () => {
    const autoPromoteQueen = !get().autoPromoteQueen;
    set({ autoPromoteQueen });
    persist({ ...get(), autoPromoteQueen });
  },
  setAnimationSpeed: (animationSpeed) => {
    set({ animationSpeed });
    persist({ ...get(), animationSpeed });
  },
}));
