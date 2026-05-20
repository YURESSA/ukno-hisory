import { useState } from 'react';
import { useGetAdminProjectsQuery, useDeleteProjectMutation, useUpdateProjectMutation } from '../api/projectsApi';
import { EditProjectModal } from './EditProjectModal';

export const AdminProjectList = () => {
  const { data: projects, isLoading, error } = useGetAdminProjectsQuery();
  const [deleteProject] = useDeleteProjectMutation();
  const [updateProject] = useUpdateProjectMutation();
  
  const [editingId, setEditingId] = useState<number | null>(null);

  if (isLoading) return <p>Загрузка списка...</p>;
  if (error) return <p>Ошибка загрузки данных</p>;

  const handleToggleDraft = async (id: number, currentStatus: boolean) => {
    try {
      await updateProject({ id, data: { is_draft: !currentStatus } }).unwrap();
    } catch (e) {
      console.error(e);
    }
  };

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
              <td>
                <button 
                  onClick={() => handleToggleDraft(project.id, project.is_draft)}
                  style={{ 
                    padding: '5px 10px', 
                    cursor: 'pointer',
                    background: project.is_draft ? '#fffbe6' : '#f6ffed',
                    border: `1px solid ${project.is_draft ? '#ffe58f' : '#b7eb8f'}`,
                    borderRadius: '4px'
                  }}
                >
                  {project.is_draft ? '📝 Черновик' : '✅ Опубликован'}
                </button>
              </td>
              <td style={{ display: 'flex', gap: '10px' }}>
                <button 
                  onClick={() => setEditingId(project.id)}
                  style={{ color: '#1890ff', cursor: 'pointer' }}
                >
                  Изменить
                </button>
                <button 
                  onClick={() => {
                    if (confirm('Удалить проект?')) deleteProject(project.id);
                  }} 
                  style={{ color: 'red', cursor: 'pointer' }}
                >
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

      {editingId && (
        <EditProjectModal 
          projectId={editingId} 
          isOpen={true} 
          onClose={() => setEditingId(null)} 
        />
      )}
    </div>
  );
};