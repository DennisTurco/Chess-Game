import { HashRouter, Routes, Route } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';
import { PlayPage } from './pages/PlayPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { LearnPage } from './pages/LearnPage';
import { HistoryPage } from './pages/HistoryPage';
import { SettingsPage } from './pages/SettingsPage';

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<PlayPage />} />
          <Route path="analysis" element={<AnalysisPage />} />
          <Route path="learn" element={<LearnPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}
