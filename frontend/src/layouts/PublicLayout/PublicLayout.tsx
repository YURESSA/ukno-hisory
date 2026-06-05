import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from '@/styles/publicLayout.module.css';

interface PublicLayoutProps {
  children: React.ReactNode;
}

export const PublicLayout: React.FC<PublicLayoutProps> = ({ children }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { hash, pathname } = useLocation();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  // Скролл к якорю при смене страницы или хеша
  useEffect(() => {
    if (hash) {
      const id = hash.replace('#', '');
      const element = document.getElementById(id);
      if (element) {
        const timer = setTimeout(() => {
          element.scrollIntoView({ behavior: 'smooth' });
        }, 100);
        return () => clearTimeout(timer);
      }
    }
  }, [hash, pathname]);

  return (
    <div className="main-layout">
      <header className={styles['nav-header']}>
        <div className={`container ${styles['nav-toolbar']}`}>
          <Link to="/" className={styles['logo']} onClick={closeMenu}>
            <img src="/logo-desktop.png" alt="логотип" />
          </Link>
          
          <div className={styles['menu-wrapper']}>
            <button 
              className={`${styles['nav-dropdown']} ${isMenuOpen ? styles['active'] : ''}`}
              onClick={toggleMenu}
            >
              <h6>меню</h6>
            </button>

            {isMenuOpen && (
              <>
                <div className={styles['menu-overlay']} onClick={closeMenu} />
                <div className={styles['menu-content']}>
                  <nav className={styles['menu-nav']}>
                    <Link to="/#map" className={styles['menu-link']} onClick={closeMenu}>
                      <h6>Интерактивная карта</h6>
                    </Link>
                    <Link to="/#history" className={styles['menu-link']} onClick={closeMenu}>
                      <h6>история района</h6>
                    </Link>
                    <Link to="/projects" className={styles['menu-link']} onClick={closeMenu}>
                      <h6>Проекты школьников</h6>
                    </Link>
                    <Link to="/enterprises" className={styles['menu-link']} onClick={closeMenu}>
                      <h6>история предприятий</h6>
                    </Link>
                    <Link to="/quiz" className={styles['menu-link']} onClick={closeMenu}>
                      <h6>квиз</h6>
                    </Link>
                    <a 
                      href="https://5buro.ru/" 
                      className={styles['menu-link']} 
                      target="_blank" 
                      onClick={closeMenu}
                    >
                      <h6>молодёжное пространство 5 этаж</h6>
                    </a>
                  </nav>

                  <div className={styles['menu-footer']}>
                    <a href="mailto:mb@mail.ru" className={styles['footer-link']}>mb@mail.ru</a>
                    <a href="tel:+7907889373" className={styles['footer-link']}>+7 907 889 373</a>
                    <div className={styles['social-links']}>
                      <a href="https://vk.com/bureau5" target="_blank" className={styles['footer-link']}>
                        <img src="/social_vk.png" alt="VK-link"/>
                      </a>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
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
