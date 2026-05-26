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
import { 
  useGetAdminEnterpriseHistoriesQuery, 
  useDeleteEnterpriseHistoryMutation,
  useUpdateEnterpriseHistoryMutation
} from '../../api/enterpriseHistoryApi';
import { EditEnterpriseHistoryModal } from './EditEnterpriseHistoryModal';
import styles from '@/styles/admin.module.css';

export const EnterpriseHistoryList = () => {
  const { data: histories, isLoading, error } = useGetAdminEnterpriseHistoriesQuery();
  const [deleteHistory] = useDeleteEnterpriseHistoryMutation();
  const [updateHistory] = useUpdateEnterpriseHistoryMutation();

  const [editingId, setEditingId] = useState<number | null>(null);

  if (isLoading) return (
    <div className={styles['adm-card']} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );
  
  if (error) return (
    <div className={styles['adm-card']}>
      <p style={{ color: 'var(--error-color)' }}>Ошибка загрузки данных</p>
    </div>
  );

  const handleToggleDraft = async (id: number, currentStatus: boolean) => {
    try {
      await updateHistory({ id, data: { is_draft: !currentStatus } }).unwrap();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className={styles['adm-card']}>
      <div className={styles['adm-list-header']}>
        <h3 className={styles['adm-title']}>История предприятий</h3>
      </div>

      <TableContainer component={Paper} className={styles['adm-table-container']}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead className={styles['adm-mui-table-head']}>
            <TableRow>
              <TableCell width={60}>ID</TableCell>
              <TableCell>Заголовок</TableCell>
              <TableCell>Подзаголовок</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {histories?.map((history) => (
              <TableRow key={history.id} hover>
                <TableCell>{history.id}</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>{history.title}</TableCell>
                <TableCell>{history.general_subtitle}</TableCell>
                <TableCell>
                  <Tooltip title={history.is_draft ? "Опубликовать" : "Снять с публикации"}>
                    <span 
                      onClick={() => handleToggleDraft(history.id, history.is_draft)}
                      className={`${styles['adm-badge']} ${history.is_draft ? styles['adm-badge-draft'] : styles['adm-badge-published']}`}
                      style={{ cursor: 'pointer' }}
                    >
                      {history.is_draft ? 'Черновик' : 'Опубликован'}
                    </span>
                  </Tooltip>
                </TableCell>
                <TableCell align="right">
                  <div className={styles['adm-actions-cell']}>
                    <IconButton 
                      size="small" 
                      onClick={() => setEditingId(history.id)}
                      sx={{ color: 'var(--primary-color)' }}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      onClick={() => {
                        if (confirm('Удалить запись?')) deleteHistory(history.id);
                      }}
                      sx={{ color: 'var(--error-color)' }}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {histories?.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 3, color: '#999' }}>
                  Записей пока нет
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {editingId && (
        <EditEnterpriseHistoryModal 
          itemId={editingId} 
          isOpen={true} 
          onClose={() => setEditingId(null)} 
        />
      )}
    </div>
  );
};
