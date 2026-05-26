import React from 'react';
import { Link } from 'react-router-dom';
import styles from '@/styles/publicLayout.module.css';

interface PublicLayoutProps {
  children: React.ReactNode;
}

export const PublicLayout: React.FC<PublicLayoutProps> = ({ children }) => {
  return (
    <div className="main-layout">
      <header className={styles['nav-header']}>
        <div className={`container ${styles['nav-toolbar']}`}>
          <Link to="/" className={styles['nav-logo']}>
            UKNO
          </Link>
          
          <nav>
            <ul className={styles['nav-list']}>
              <li><Link to="/" className={styles['nav-link']}>Главная</Link></li>
              <li><Link to="/projects" className={styles['nav-link']}>Проекты</Link></li>
              <li><Link to="/enterprise" className={styles['nav-link']}>Предприятия</Link></li>
              <li><Link to="/quiz" className={styles['nav-link']}>Квиз</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="section-padding">
        {children}
      </main>

      <footer className={styles.footer}>
        <div className="container">
          <p className={styles['footer-text']}>
          </p>
        </div>
      </footer>
    </div>
  );
};
