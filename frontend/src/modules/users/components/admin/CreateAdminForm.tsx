import { useForm } from 'react-hook-form';
import { Button, CircularProgress } from '@mui/material';
import { PersonAdd as AddIcon } from '@mui/icons-material';
import { useCreateAdminMutation } from '../../api/usersApi';

import { CreateAdminRequest } from '../../types';
import styles from '@/styles/admin.module.css';

export const CreateAdminForm = () => {
  const { register, handleSubmit, reset } = useForm<CreateAdminRequest>();
  const [createAdmin, { isLoading }] = useCreateAdminMutation();

  const onSubmit = async (data: CreateAdminRequest) => {
    try {
      await createAdmin({ email: data.email }).unwrap();
      alert('Приглашение отправлено! Администратор создан (пароль нужно сбросить через почту или задать вручную).');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
      alert('Ошибка при создании администратора (возможно, у вас недостаточно прав)');
    }
  };

  return (
    <div className={styles['adm-card']}>
      <h3 className={styles['adm-title']}>Создать администратора</h3>
      <p className={styles['adm-helper-text']} style={{ marginBottom: '20px' }}>
        Только для супер-администраторов. Укажите email для отправки приглашения.
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className={styles['adm-form']}>
        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Email нового админа</label>
          <input 
            type="email" 
            {...register('email')} 
            placeholder="admin@example.com" 
            className={styles['adm-input']}
            required 
          />
        </div>
        
        <Button 
          type="submit" 
          variant="contained" 
          disabled={isLoading}
          startIcon={!isLoading && <AddIcon />}
          fullWidth
          sx={{ 
            bgcolor: 'var(--primary-color)', 
            '&:hover': { bgcolor: 'var(--primary-hover)' },
            py: 1.5,
            borderRadius: '8px',
            boxShadow: 'none',
            mt: 1
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Добавить админа'}
        </Button>
      </form>
    </div>
  );
};
