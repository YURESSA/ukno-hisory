import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button, CircularProgress, Alert } from '@mui/material';
import { AdminPanelSettings as AdminIcon } from '@mui/icons-material';
import { useLoginMutation } from '../../api/authApi';
import styles from '@/styles/admin.module.css';

const loginSchema = z.object({
  email: z.string().min(1, 'Email обязателен').email('Некорректный формат email'),
  password: z.string().min(5, 'Пароль должен быть не менее 5 символов'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginForm = () => {
  const { 
    register, 
    handleSubmit, 
    formState: { errors } 
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  });
  
  const [login, { isLoading, error }] = useLoginMutation();

  const onSubmit = async (data: LoginFormData) => {
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
      <div className={styles['adm-card']} style={{ maxWidth: '400px', width: '100%', padding: '40px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <AdminIcon sx={{ fontSize: 48, color: 'var(--primary-color)', mb: 2 }} />
          <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 800, color: 'var(--secondary-color)' }}>
            Admin Login
          </h2>

          <p style={{ color: '#666', marginTop: '8px' }}>Вход в панель управления</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className={styles['adm-form']}>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Email</label>
            <input 
              {...register('email')} 
              type="email" 
              placeholder="admin@example.com" 
              className={`${styles['adm-input']} ${errors.email ? styles['adm-input-error'] : ''}`}
            />
            {errors.email && <span className={styles['adm-error-text']}>{errors.email.message}</span>}
          </div>

          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Пароль</label>
            <input 
              {...register('password')} 
              type="password" 
              placeholder="••••••••" 
              className={`${styles['adm-input']} ${errors.password ? styles['adm-input-error'] : ''}`}
            />
            {errors.password && <span className={styles['adm-error-text']}>{errors.password.message}</span>}
          </div>
          
          {error && (
            <Alert severity="error" sx={{ borderRadius: '8px', mb: 2 }}>
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