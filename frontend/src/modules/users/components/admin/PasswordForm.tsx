import { useState } from 'react';
import { Alert, Button, Stack, TextField } from '@mui/material';
import { useChangePasswordMutation } from '../../api/usersApi';
import styles from '@/styles/admin.module.css';

export const apiError = (error: unknown): string => {
  const detail = (error as { data?: { detail?: unknown } })?.data?.detail;
  return typeof detail === 'string' ? detail : 'Не удалось сохранить изменения. Попробуйте снова.';
};

export const PasswordForm = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [changePassword, { isLoading }] = useChangePasswordMutation();

  return <div className={styles['adm-card']}>
    <h3 className={styles['adm-title']}>Мой пароль</h3>
    <form onSubmit={async event => {
      event.preventDefault(); setMessage(''); setError('');
      if (newPassword !== confirmation) { setError('Новые пароли не совпадают'); return; }
      try {
        await changePassword({ old_password: oldPassword, new_password: newPassword }).unwrap();
        setOldPassword(''); setNewPassword(''); setConfirmation('');
        setMessage('Пароль изменён. Для следующего входа используйте новый пароль.');
      } catch (err) { setError(apiError(err)); }
    }}>
      <Stack spacing={2}>
        {message && <Alert severity="success">{message}</Alert>}
        {error && <Alert severity="error">{error}</Alert>}
        <TextField label="Текущий пароль" type="password" autoComplete="current-password" required value={oldPassword} onChange={e => setOldPassword(e.target.value)} />
        <TextField label="Новый пароль" type="password" autoComplete="new-password" required slotProps={{ htmlInput: { minLength: 8, maxLength: 128 } }} helperText="От 8 до 128 символов" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
        <TextField label="Повторите новый пароль" type="password" autoComplete="new-password" required value={confirmation} onChange={e => setConfirmation(e.target.value)} />
        <Button type="submit" variant="contained" disabled={isLoading}>{isLoading ? 'Сохранение…' : 'Сменить мой пароль'}</Button>
      </Stack>
    </form>
  </div>;
};
