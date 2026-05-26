import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Tabs, 
  Tab,
  Button,
  Tooltip
} from '@mui/material';
import { 
  Logout as LogoutIcon, 
  Business as BusinessIcon,
  Timeline as TimelineIcon,
  People as UsersIcon,
  Quiz as QuizIcon,
  FolderSpecial as ProjectsIcon
} from '@mui/icons-material';
import styles from '@/styles/admin.module.css';

type AdminTab = 'projects' | 'timeline' | 'enterprise' | 'users' | 'quiz';

interface AdminLayoutProps {
  children: React.ReactNode;
  activeTab: AdminTab;
  onTabChange: (tab: AdminTab) => void;
}

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children, activeTab, onTabChange }) => {
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.reload();
  };

  const handleChange = (_event: React.SyntheticEvent, newValue: AdminTab) => {
    onTabChange(newValue);
  };

  return (
    <div className={styles['adm-layout']}>
      <header className={styles['adm-header']}>
        <div className={styles['adm-logo']}>
          <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
            <span>Admin Panel</span>
          </Link>
        </div>
        <Tooltip title="Выйти из системы">
          <Button 
            onClick={handleLogout} 
            variant="contained" 
            color="error"
            startIcon={<LogoutIcon />}
            size="small"
            sx={{ borderRadius: '8px', textTransform: 'none', fontWeight: 600 }}
          >
            Выйти
          </Button>
        </Tooltip>
      </header>

      <nav className={styles['adm-nav-bar']}>
        <div className={styles['adm-container']}>
          <Tabs 
            value={activeTab} 
            onChange={handleChange} 
            variant="scrollable"
            scrollButtons="auto"
            textColor="primary"
            indicatorColor="primary"
            sx={{
              '& .MuiTab-root': {
                fontWeight: 700,
                minHeight: 64,
                fontSize: '0.9rem',
                textTransform: 'none',
                gap: 1,
                color: '#666'
              },
              '& .Mui-selected': {
                color: 'var(--primary-color) !important'
              },
              '& .MuiTabs-indicator': {
                backgroundColor: 'var(--primary-color)',
                height: 3
              }
            }}
          >
            <Tab icon={<ProjectsIcon fontSize="small" />} iconPosition="start" label="Проекты" value="projects" />
            <Tab icon={<TimelineIcon fontSize="small" />} iconPosition="start" label="Таймлайн" value="timeline" />
            <Tab icon={<BusinessIcon fontSize="small" />} iconPosition="start" label="История предприятий" value="enterprise" />
            <Tab icon={<UsersIcon fontSize="small" />} iconPosition="start" label="Пользователи" value="users" />
            <Tab icon={<QuizIcon fontSize="small" />} iconPosition="start" label="Квиз" value="quiz" />
          </Tabs>
        </div>
      </nav>

      <main className={styles['adm-content']}>
        <div className={styles['adm-container']}>
          {children}
        </div>
      </main>
    </div>
  );
};
