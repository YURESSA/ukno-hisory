import { useState } from 'react';
import {
  Alert, Button, CircularProgress, Dialog, DialogActions, DialogContent,
  DialogTitle, MenuItem, Stack, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, TextField, Typography,
} from '@mui/material';
import {
  useAdminChangePasswordMutation, useDeleteUserMutation, useGetMeQuery,
  useGetUsersQuery, useUpdateUserMutation,
} from '../../api/usersApi';
import { User, UserRole } from '../../types';
import { apiError } from './PasswordForm';
import styles from '@/styles/admin.module.css';

export const UserList = () => {
  const { data: users, isLoading, error, refetch } = useGetUsersQuery();
  const { data: me } = useGetMeQuery();
  const [updateUser, { isLoading: saving }] = useUpdateUserMutation();
  const [changePassword, { isLoading: changingPassword }] = useAdminChangePasswordMutation();
  const [deleteUser, { isLoading: deleting }] = useDeleteUserMutation();
  const [editing, setEditing] = useState<User | null>(null);
  const [passwordUser, setPasswordUser] = useState<User | null>(null);
  const [deletingUser, setDeletingUser] = useState<User | null>(null);
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<UserRole>(UserRole.ADMIN);
  const [password, setPassword] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [failure, setFailure] = useState('');
  const [success, setSuccess] = useState('');
  const isSuperadmin = me?.role === UserRole.SUPER_ADMIN;
  const busy = saving || changingPassword || deleting;
  const clearMessages = () => { setFailure(''); setSuccess(''); };
  const close = () => {
    if (busy) return;
    setEditing(null); setPasswordUser(null); setDeletingUser(null);
    setPassword(''); setConfirmation(''); setFailure('');
  };

  if (isLoading) return <CircularProgress aria-label="Загрузка пользователей" />;
  if (error) return <Alert severity="error" action={<Button onClick={() => refetch()}>Повторить</Button>}>Не удалось загрузить пользователей</Alert>;

  return <div className={styles['adm-card']}>
    <h3 className={styles['adm-title']}>Пользователи</h3>
    <Typography sx={{ mb: 2 }}>Изменять email, роли и чужие пароли может супер-администратор.</Typography>
    {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
    <TableContainer>
      <Table>
        <TableHead><TableRow><TableCell>Email</TableCell><TableCell>Роль</TableCell><TableCell>Действия</TableCell></TableRow></TableHead>
        <TableBody>{users?.map(user => <TableRow key={user.id}>
          <TableCell>{user.email}{me?.id === user.id && ' (вы)'}</TableCell>
          <TableCell>{user.role === UserRole.SUPER_ADMIN ? 'Супер-администратор' : 'Администратор'}</TableCell>
          <TableCell><Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: 'wrap' }}>
            {isSuperadmin && <Button size="small" onClick={() => {
              clearMessages(); setEditing(user); setEmail(user.email); setRole(user.role);
            }}>Редактировать</Button>}
            {isSuperadmin && me?.id !== user.id && <>
              <Button size="small" onClick={() => { clearMessages(); setPassword(''); setConfirmation(''); setPasswordUser(user); }}>Задать пароль</Button>
              <Button size="small" color="error" onClick={() => { clearMessages(); setDeletingUser(user); }}>Удалить</Button>
            </>}
            {me?.id === user.id && <Typography variant="caption">Свой пароль можно изменить в форме «Мой пароль».</Typography>}
          </Stack></TableCell>
        </TableRow>)}</TableBody>
      </Table>
    </TableContainer>

    <Dialog open={!!editing} onClose={close} fullWidth maxWidth="sm">
      <form onSubmit={async e => {
        e.preventDefault(); if (!editing) return; setFailure('');
        try {
          await updateUser({ userId: editing.id, data: { email, role } }).unwrap();
          setEditing(null); setSuccess('Пользователь обновлён');
        } catch (err) { setFailure(apiError(err)); }
      }}>
        <DialogTitle>Редактировать пользователя</DialogTitle>
        <DialogContent><Stack spacing={2} sx={{ pt: 1 }}>
          {failure && <Alert severity="error">{failure}</Alert>}
          <TextField label="Email" type="email" required value={email} onChange={e => setEmail(e.target.value)} />
          <TextField select label="Роль" value={role} disabled={editing?.id === me?.id} onChange={e => setRole(e.target.value as UserRole)} helperText={editing?.id === me?.id ? 'Собственную роль изменить нельзя' : 'Супер-администратор получает управление всеми пользователями'}>
            <MenuItem value={UserRole.ADMIN}>Администратор</MenuItem>
            <MenuItem value={UserRole.SUPER_ADMIN}>Супер-администратор</MenuItem>
          </TextField>
        </Stack></DialogContent>
        <DialogActions><Button onClick={close} disabled={busy}>Отмена</Button><Button type="submit" variant="contained" disabled={busy}>Сохранить</Button></DialogActions>
      </form>
    </Dialog>

    <Dialog open={!!passwordUser} onClose={close} fullWidth maxWidth="sm">
      <form onSubmit={async e => {
        e.preventDefault(); if (!passwordUser) return; setFailure('');
        if (password !== confirmation) { setFailure('Пароли не совпадают'); return; }
        try {
          await changePassword({ userId: passwordUser.id, data: { new_password: password } }).unwrap();
          setPasswordUser(null); setPassword(''); setConfirmation(''); setSuccess('Пароль пользователя изменён');
        } catch (err) { setFailure(apiError(err)); }
      }}>
        <DialogTitle>Задать пароль</DialogTitle>
        <DialogContent><Stack spacing={2} sx={{ pt: 1 }}>
          <Typography>{passwordUser?.email}</Typography>
          {failure && <Alert severity="error">{failure}</Alert>}
          <TextField label="Новый пароль пользователя" type="password" autoComplete="new-password" required slotProps={{ htmlInput: { minLength: 8, maxLength: 128 } }} helperText="От 8 до 128 символов" value={password} onChange={e => setPassword(e.target.value)} />
          <TextField label="Повторите пароль пользователя" type="password" autoComplete="new-password" required value={confirmation} onChange={e => setConfirmation(e.target.value)} />
        </Stack></DialogContent>
        <DialogActions><Button onClick={close} disabled={busy}>Отмена</Button><Button type="submit" variant="contained" disabled={busy}>Изменить пароль</Button></DialogActions>
      </form>
    </Dialog>

    <Dialog open={!!deletingUser} onClose={close} fullWidth maxWidth="sm">
      <DialogTitle>Удалить пользователя?</DialogTitle>
      <DialogContent>
        <Typography>{deletingUser?.email} потеряет доступ к админке.</Typography>
        {failure && <Alert severity="error">{failure}</Alert>}
      </DialogContent>
      <DialogActions><Button onClick={close} disabled={busy}>Отмена</Button><Button color="error" disabled={busy} onClick={async () => {
        if (!deletingUser) return;
        try { await deleteUser(deletingUser.id).unwrap(); setDeletingUser(null); setSuccess('Пользователь удалён'); }
        catch (err) { setFailure(apiError(err)); }
      }}>Удалить</Button></DialogActions>
    </Dialog>
  </div>;
};
