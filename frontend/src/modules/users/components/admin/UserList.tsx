import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper, 
  IconButton,
  CircularProgress
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import { useGetUsersQuery, useDeleteUserMutation } from '../../api/usersApi';

export const UserList = () => {
  const { data: users, isLoading, error } = useGetUsersQuery();
  const [deleteUser] = useDeleteUserMutation();

  if (isLoading) return (
    <div className="adm-card" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );

  if (error) return (
    <div className="adm-card">
      <p style={{ color: 'var(--error-color)' }}>Ошибка загрузки данных</p>
    </div>
  );

  return (
    <div className="adm-card">
      <h3 className="adm-title">Пользователи (Админы)</h3>
      
      <TableContainer component={Paper} className="adm-table-container">
        <Table>
          <TableHead className="adm-mui-table-head">
            <TableRow>
              <TableCell width={60}>ID</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Роль</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users?.map((user) => (
              <TableRow key={user.id} hover>
                <TableCell>{user.id}</TableCell>
                <TableCell sx={{ fontWeight: 500 }}>{user.email}</TableCell>
                <TableCell>
                  <span className={`adm-badge ${user.role === 'superadmin' ? 'adm-badge-published' : 'adm-badge-draft'}`} style={{ cursor: 'default' }}>
                    {user.role}
                  </span>
                </TableCell>
                <TableCell align="right">
                  <div className="adm-actions-cell">
                    <IconButton 
                      size="small" 
                      onClick={() => {
                        if (window.confirm('Удалить пользователя?')) deleteUser(user.id);
                      }}
                      sx={{ color: 'var(--error-color)' }}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {users?.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center" sx={{ py: 3, color: '#999' }}>
                  Пользователей пока нет
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};
