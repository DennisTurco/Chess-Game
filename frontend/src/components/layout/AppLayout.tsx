import { useEffect } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { Swords, LineChart, GraduationCap, History, Settings, Moon, Sun, Crown } from 'lucide-react';
import { useSettingsStore } from '../../state/settingsStore';
import './layout.css';

const NAV_ITEMS = [
  { to: '/', label: 'Play', icon: Swords },
  { to: '/analysis', label: 'Analysis', icon: LineChart },
  { to: '/learn', label: 'Learn', icon: GraduationCap },
  { to: '/history', label: 'History', icon: History },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export function AppLayout() {
  const theme = useSettingsStore((s) => s.theme);
  const toggleTheme = useSettingsStore((s) => s.toggleTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  return (
    <div className="app-shell">
      <aside className="app-rail">
        <div className="app-brand">
          <Crown size={22} strokeWidth={1.75} />
          <div className="app-brand-text">
            <span className="app-brand-name serif">Caissa</span>
            <span className="app-brand-tag">chess tutor</span>
          </div>
        </div>

        <nav className="app-nav">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) => `app-nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} strokeWidth={1.75} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <button className="app-theme-toggle" onClick={toggleTheme} title="Toggle theme">
          {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          <span>{theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>
        </button>
      </aside>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
