# Caissa — Chess Tutor (frontend)

React + TypeScript UI for the chess tutor project, built with Vite.

This replaces the old pygame UI. It is currently **standalone**: all chess
rules run client-side via [chess.js](https://github.com/jhlywa/chess.js),
and the "engine" moves plus the coach comments in `src/lib/tutor.ts` are
local heuristic placeholders. Swap them out once the Python/Stockfish
backend is wired up (e.g. via a REST/WebSocket API called from
`state/gameStore.ts`).

## Structure

- `src/state` — zustand stores: `gameStore` (chess.js game state, moves,
  captures, clocks) and `settingsStore` (theme, board skin, toggles;
  persisted to `localStorage`).
- `src/components/board` — the board, pieces, promotion dialog.
- `src/components/panels` — move list, coach/tutor panel, captured pieces,
  player bars, game controls.
- `src/components/modals` — new game and game-over dialogs.
- `src/pages` — Play, Analysis (PGN viewer), Learn, History, Settings.
- `src/lib/tutor.ts` — placeholder move-quality heuristic and "engine".

## Run

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```
