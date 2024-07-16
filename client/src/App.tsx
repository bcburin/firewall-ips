import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import CriticalRulesPage from './pages/critical-rules';
import DashboardPage from './pages/dashboard';
import FirewallRulesPage from './pages/firewall-rules';
import LoginPage from './pages/login';
import MainLayout from './layout/main';
import NotFoundPage from './pages/not-found';
import React from 'react';
import UsersPage from './pages/users';

const withMainLayout = (page: JSX.Element) => {
  return (
    <MainLayout>
      {page}
    </MainLayout>
  );
}

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={withMainLayout(<DashboardPage />)} />
        <Route path="/dashboard" element={withMainLayout(<DashboardPage />)} />
        <Route path="/users" element={withMainLayout(<UsersPage />)} />
        <Route path="/critical-rules" element={withMainLayout(<CriticalRulesPage />)} />
        <Route path="/firewall-rules" element={withMainLayout(< FirewallRulesPage />)} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default App;
