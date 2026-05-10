import { useGetAdminProjectsQuery, useDeleteProjectMutation } from '../api/projectsApi';

export const AdminProjectList = () => {
  const { data: projects, isLoading, error } = useGetAdminProjectsQuery();
  const [deleteProject] = useDeleteProjectMutation();

  if (isLoading) return <p>Загрузка списка...</p>;
  if (error) return <p>Ошибка загрузки данных</p>;

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Список проектов (Админ-панель)</h3>
      <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Автор</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {projects?.map((project) => (
            <tr key={project.id}>
              <td>{project.id}</td>
              <td>{project.title}</td>
              <td>{project.author}</td>
              <td>{project.is_draft ? '📝 Черновик' : '✅ Опубликован'}</td>
              <td>
                <button onClick={() => deleteProject(project.id)} style={{ color: 'red' }}>
                  Удалить
                </button>
              </td>
            </tr>
          ))}
          {projects?.length === 0 && (
            <tr>
              <td colSpan={5} style={{ textAlign: 'center' }}>База данных пуста</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};