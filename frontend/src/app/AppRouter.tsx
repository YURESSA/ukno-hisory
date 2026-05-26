import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from '@/pages/public/HomePage';
import { AdminPage } from '@/pages/admin/AdminPage';

export const AppRouter = () => {
  return (
    <Router>
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/" element={<HomePage />} />
        
        {/* Маршрут админки */}
        <Route path="/admin" element={<AdminPage />} />

        <Route path="*" element={<HomePage />} />
      </Routes>
    </Router>
  );
};
