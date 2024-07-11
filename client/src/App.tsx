import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import CriticalRulesPage from './pages/critical-rules';
import DashboardPage from './pages/dashboard';
import LoginPage from './pages/login';
import NotFoundPage from './pages/not-found';
import React from 'react';
import UsersPage from './pages/users';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<DashboardPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/critical-rules" element={<CriticalRulesPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default App;
