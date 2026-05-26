import React from 'react';
import { Link } from 'react-router-dom';

interface PublicLayoutProps {
  children: React.ReactNode;
}

export const PublicLayout: React.FC<PublicLayoutProps> = ({ children }) => {
  return (
    <div className="main-layout">
      <header className="nav-header">
        <div className="container nav-toolbar">
          <Link to="/" className="nav-logo">
            UKNO
          </Link>
          
          <nav>
            <ul className="nav-list">
              <li><Link to="/" className="nav-link">Главная</Link></li>
              <li><Link to="/projects" className="nav-link">Проекты</Link></li>
              <li><Link to="/enterprise" className="nav-link">Предприятия</Link></li>
              <li><Link to="/quiz" className="nav-link">Квиз</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="section-padding">
        {children}
      </main>

      <footer className="footer">
        <div className="container">
          <p className="footer-text">
          </p>
        </div>
      </footer>
    </div>
  );
};
