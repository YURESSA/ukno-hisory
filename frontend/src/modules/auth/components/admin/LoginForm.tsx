import { useForm } from 'react-hook-form';
import { Button, CircularProgress, Alert } from '@mui/material';
import { AdminPanelSettings as AdminIcon } from '@mui/icons-material';
import { useLoginMutation } from '../../api/authApi';

import { LoginRequest } from '../../types';

export const LoginForm = () => {
  const { register, handleSubmit } = useForm<LoginRequest>();
  const [login, { isLoading, error }] = useLoginMutation();

  const onSubmit = async (data: LoginRequest) => {
    try {
      const result = await login({
        email: data.email,
        password: data.password
      }).unwrap();
      
      localStorage.setItem('token', result.access_token);
      window.location.reload();
    } catch (err) {
      console.error('Ошибка входа:', err);
    }
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh', 
      backgroundColor: '#f4f6f8' 
    }}>
      <div className="adm-card" style={{ maxWidth: '400px', width: '100%', padding: '40px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <AdminIcon sx={{ fontSize: 48, color: 'var(--primary-color)', mb: 2 }} />
          <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 800, color: 'var(--secondary-color)' }}>
            UKNO Admin
          </h2>
          <p style={{ color: '#666', marginTop: '8px' }}>Вход в панель управления</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="adm-form">
          <div className="adm-form-group">
            <label className="adm-label">Email</label>
            <input 
              {...register('email')} 
              type="email" 
              placeholder="admin@example.com" 
              className="adm-input" 
              required 
            />
          </div>

          <div className="adm-form-group">
            <label className="adm-label">Пароль</label>
            <input 
              {...register('password')} 
              type="password" 
              placeholder="••••••••" 
              className="adm-input" 
              required 
            />
          </div>
          
          {error && (
            <Alert severity="error" sx={{ borderRadius: '8px' }}>
              Неверный логин или пароль
            </Alert>
          )}
          
          <Button 
            type="submit" 
            variant="contained" 
            disabled={isLoading}
            fullWidth
            size="large"
            sx={{ 
              bgcolor: 'var(--primary-color)', 
              '&:hover': { bgcolor: 'var(--primary-hover)' },
              py: 1.5,
              borderRadius: '8px',
              boxShadow: 'none',
              mt: 1
            }}
          >
            {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Войти в систему'}
          </Button>
        </form>
      </div>
    </div>
  );
};