import { useState } from 'react';
import { LoginForm } from '@/modules/auth/components/LoginForm';
import { CreateProjectForm } from '@/modules/projects/components/CreateProjectForm';
import { AdminProjectList } from '@/modules/projects/components/AdminProjectList';
import { TimelineList } from '@/modules/timeline/components/TimelineList';
import { CreateTimelineForm } from '@/modules/timeline/components/CreateTimelineForm';
import { EnterpriseHistoryList } from '@/modules/enterprise_history/components/EnterpriseHistoryList';
import { CreateEnterpriseHistoryForm } from '@/modules/enterprise_history/components/CreateEnterpriseHistoryForm';
import { UserList } from '@/modules/users/components/UserList';
import { CreateAdminForm } from '@/modules/users/components/CreateAdminForm';

function App() {
  const [activeTab, setActiveTab] = useState<'projects' | 'timeline' | 'enterprise' | 'users'>('projects');
  const token = localStorage.getItem('token');

  if (!token) {
    return <LoginForm />;
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.reload();
  };

  const TabButton = ({ id, label }: { id: typeof activeTab, label: string }) => (
    <button 
      onClick={() => setActiveTab(id)}
      style={{ 
        padding: '10px 20px', 
        cursor: 'pointer', 
        background: activeTab === id ? '#1890ff' : '#f0f0f0',
        color: activeTab === id ? 'white' : 'black',
        border: '1px solid #d9d9d9',
        marginRight: '5px'
      }}
    >
      {label}
    </button>
  );

  return (
    <div style={{ padding: '40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Панель управления</h1>
        <button onClick={handleLogout} style={{ background: '#ff4d4f', color: 'white', border: 'none', padding: '8px 16px', cursor: 'pointer' }}>
          Выйти
        </button>
      </div>

      <div style={{ marginTop: '20px', marginBottom: '20px' }}>
        <TabButton id="projects" label="Проекты студентов" />
        <TabButton id="timeline" label="Таймлайн" />
        <TabButton id="enterprise" label="История предприятий" />
        <TabButton id="users" label="Пользователи" />
      </div>
      
      {activeTab === 'projects' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px' }}>
          <CreateProjectForm />
          <AdminProjectList />
        </div>
      )}

      {activeTab === 'timeline' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px' }}>
          <CreateTimelineForm />
          <TimelineList />
        </div>
      )}

      {activeTab === 'enterprise' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px' }}>
          <CreateEnterpriseHistoryForm />
          <EnterpriseHistoryList />
        </div>
      )}

      {activeTab === 'users' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px' }}>
          <CreateAdminForm />
          <UserList />
        </div>
      )}
    </div>
  );
}

export default App;