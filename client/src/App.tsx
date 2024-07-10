import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import DashboardPage from './pages/dashboard';
import LoginPage from './pages/login';
import React from 'react';
import UsersPage from './pages/users';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/users" element={<UsersPage />} />
      </Routes>
    </Router>
  );
};

export default App;
