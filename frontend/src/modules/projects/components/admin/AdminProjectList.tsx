import { useState } from 'react';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper, 
  IconButton, 
  Tooltip,
  CircularProgress
} from '@mui/material';
import { 
  Edit as EditIcon, 
  Delete as DeleteIcon
} from '@mui/icons-material';
import { useGetAdminProjectsQuery, useDeleteProjectMutation, useUpdateProjectMutation } from '../../api/projectsApi';
import { EditProjectModal } from './EditProjectModal';

export const AdminProjectList = () => {
  const { data: projects, isLoading, error } = useGetAdminProjectsQuery();
  const [deleteProject] = useDeleteProjectMutation();
  const [updateProject] = useUpdateProjectMutation();
  
  const [editingId, setEditingId] = useState<number | null>(null);

  if (isLoading) return (
    <div className="adm-card" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );
  
  if (error) return (
    <div className="adm-card">
      <p style={{ color: 'var(--error-color)' }}>Ошибка загрузки данных</p>
    </div>
  );

  const handleToggleDraft = async (id: number, currentStatus: boolean) => {
    try {
      await updateProject({ id, data: { is_draft: !currentStatus } }).unwrap();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="adm-card">
      <div className="adm-list-header">
        <h3 className="adm-title">Список проектов</h3>
      </div>

      <TableContainer component={Paper} className="adm-table-container">
        <Table sx={{ minWidth: 650 }}>
          <TableHead className="adm-mui-table-head">
            <TableRow>
              <TableCell width={60}>ID</TableCell>
              <TableCell>Название</TableCell>
              <TableCell>Автор</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {projects?.map((project) => (
              <TableRow key={project.id} hover>
                <TableCell>{project.id}</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>{project.title}</TableCell>
                <TableCell>{project.author}</TableCell>
                <TableCell>
                  <Tooltip title={project.is_draft ? "Опубликовать" : "Снять с публикации"}>
                    <span 
                      onClick={() => handleToggleDraft(project.id, project.is_draft)}
                      className={`adm-badge ${project.is_draft ? 'adm-badge-draft' : 'adm-badge-published'}`}
                      style={{ cursor: 'pointer' }}
                    >
                      {project.is_draft ? 'Черновик' : 'Опубликован'}
                    </span>
                  </Tooltip>
                </TableCell>
                <TableCell align="right">
                  <div className="adm-actions-cell">
                    <IconButton 
                      size="small" 
                      onClick={() => setEditingId(project.id)}
                      sx={{ color: 'var(--primary-color)' }}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      onClick={() => {
                        if (confirm('Удалить проект?')) deleteProject(project.id);
                      }}
                      sx={{ color: 'var(--error-color)' }}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {projects?.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 3, color: '#999' }}>
                  Проектов пока нет
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

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
