import { useSettingsStore } from '../state/settingsStore';
import { Toggle } from '../components/common/Toggle';
import type { BoardTheme } from '../types';
import './pages.css';

const BOARD_THEMES: { id: BoardTheme; light: string; dark: string }[] = [
  { id: 'olive', light: '#ece7dc', dark: '#7c8b78' },
  { id: 'walnut', light: '#e8d3ab', dark: '#9a6b3f' },
  { id: 'slate', light: '#dfe4ea', dark: '#5b6b7c' },
  { id: 'coral', light: '#fbe9df', dark: '#c97b62' },
];

export function SettingsPage() {
  const settings = useSettingsStore();

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title serif">Settings</h1>
          <p className="page-subtitle">Personalize the board, sound and interface. Saved locally in your browser.</p>
        </div>
      </div>

      <div className="settings-section">
        <p className="settings-section-title">Appearance</p>
        <div className="settings-row">
          <div>
            <div className="settings-row-label">Dark mode</div>
            <div className="settings-row-desc">Switch between a light and dark interface.</div>
          </div>
          <Toggle checked={settings.theme === 'dark'} onChange={settings.toggleTheme} />
        </div>
        <div className="settings-row">
          <div>
            <div className="settings-row-label">Board theme</div>
            <div className="settings-row-desc">Choose the color of the squares.</div>
          </div>
          <div className="board-theme-grid">
            {BOARD_THEMES.map((t) => (
              <button
                key={t.id}
                className={`board-theme-swatch ${settings.boardTheme === t.id ? 'active' : ''}`}
                onClick={() => settings.setBoardTheme(t.id)}
                title={t.id}
              >
                <span style={{ background: t.light }} />
                <span style={{ background: t.dark }} />
                <span style={{ background: t.dark }} />
                <span style={{ background: t.light }} />
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="settings-section">
        <p className="settings-section-title">Gameplay</p>
        <div className="settings-row">
          <div>
            <div className="settings-row-label">Show coordinates</div>
            <div className="settings-row-desc">Display file and rank labels around the board.</div>
          </div>
          <Toggle checked={settings.showCoordinates} onChange={settings.toggleCoordinates} />
        </div>
        <div className="settings-row">
          <div>
            <div className="settings-row-label">Highlight legal moves</div>
            <div className="settings-row-desc">Show dots and rings for the selected piece's legal moves.</div>
          </div>
          <Toggle checked={settings.showLegalMoves} onChange={settings.toggleLegalMoves} />
        </div>
        <div className="settings-row">
          <div>
            <div className="settings-row-label">Always promote to queen</div>
            <div className="settings-row-desc">Skip the promotion dialog and always choose a queen.</div>
          </div>
          <Toggle checked={settings.autoPromoteQueen} onChange={settings.toggleAutoPromote} />
        </div>
      </div>

      <div className="settings-section">
        <p className="settings-section-title">Sound</p>
        <div className="settings-row">
          <div>
            <div className="settings-row-label">Move sounds</div>
            <div className="settings-row-desc">Play a sound on moves and captures.</div>
          </div>
          <Toggle checked={settings.soundEnabled} onChange={settings.toggleSound} />
        </div>
      </div>
    </div>
  );
}
