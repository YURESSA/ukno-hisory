import { useGetUsersQuery, useDeleteUserMutation } from '../api/usersApi';

export const UserList = () => {
  const { data: users, isLoading, error } = useGetUsersQuery();
  const [deleteUser] = useDeleteUserMutation();

  if (isLoading) return <p>Загрузка пользователей...</p>;
  if (error) return <p>Ошибка загрузки данных</p>;

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Пользователи (Админы)</h3>
      <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Роль</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {users?.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>
                <button onClick={() => deleteUser(user.id)} style={{ color: 'red' }}>
                  Удалить
                </button>
              </td>
            </tr>
          ))}
          {users?.length === 0 && (
            <tr>
              <td colSpan={4} style={{ textAlign: 'center' }}>Пользователей нет</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};
