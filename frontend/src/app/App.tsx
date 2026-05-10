import { LoginForm } from '@/modules/auth/components/LoginForm';
import { CreateProjectForm } from '@/modules/projects/components/CreateProjectForm';
import { AdminProjectList } from '@/modules/projects/components/AdminProjectList';

function App() {
  const token = localStorage.getItem('token');

  if (!token) {
    return <LoginForm />;
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.reload();
  };

  return (
    <div style={{ padding: '40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Панель управления</h1>
        <button onClick={handleLogout} style={{ background: '#ff4d4f', color: 'white', border: 'none', padding: '8px 16px', cursor: 'pointer' }}>
          Выйти
        </button>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px', marginTop: '20px' }}>
        <CreateProjectForm />
        <AdminProjectList />
      </div>
    </div>
  );
}

export default App;