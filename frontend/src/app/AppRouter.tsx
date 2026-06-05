import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from '@/pages/public/HomePage';
import { ProjectsPage } from '@/pages/public/ProjectsPage';
import { ProjectDetailPage } from '@/pages/public/ProjectDetailPage';
import { QuizPage } from '@/pages/public/QuizPage';
import { AdminPage } from '@/pages/admin/AdminPage';
import { EnterprisesPage } from '@/pages/public/EnterprisesPage';

export const AppRouter = () => {
  return (
    <Router>
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/" element={<HomePage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/:id" element={<ProjectDetailPage />} />
        <Route path="/enterprises" element={<EnterprisesPage />} />
        <Route path="/quiz" element={<QuizPage />} />
        
        {/* Маршрут админки */}
        <Route path="/admin" element={<AdminPage />} />

        <Route path="*" element={<HomePage />} />
      </Routes>
    </Router>
  );
};
