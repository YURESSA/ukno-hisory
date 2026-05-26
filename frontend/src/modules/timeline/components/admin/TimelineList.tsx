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
  CircularProgress
} from '@mui/material';
import { 
  Edit as EditIcon, 
  Delete as DeleteIcon 
} from '@mui/icons-material';
import { useGetTimelineQuery, useDeleteTimelineMutation } from '../../api/timelineApi';
import { EditTimelineModal } from './EditTimelineModal';
import { TimelineEvent } from '../../types';
import { resolveBackendUrl } from '@/config/env';
import styles from '@/styles/admin.module.css';

export const TimelineList = () => {
  const { data: timeline, isLoading, error } = useGetTimelineQuery();
  const [deleteTimeline] = useDeleteTimelineMutation();
  
  const [editingEvent, setEditingEvent] = useState<TimelineEvent | null>(null);

  if (isLoading) return (
    <div className={styles['adm-card']} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );
  
  if (error) return (
    <div className={styles['adm-card']}>
      <p style={{ color: 'var(--error-color)' }}>Ошибка загрузки таймлайна</p>
    </div>
  );

  return (
    <div className={styles['adm-card']}>
      <h3 className={styles['adm-title']}>Таймлайн событий</h3>
      
      <TableContainer component={Paper} className={styles['adm-table-container']}>
        <Table>
          <TableHead className={styles['adm-mui-table-head']}>
            <TableRow>
              <TableCell width={100}>Год</TableCell>
              <TableCell>Текст</TableCell>
              <TableCell>Изображение</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {timeline?.map((item) => (
              <TableRow key={item.id} hover>
                <TableCell>
                  <span className={styles['adm-year-badge']}>{item.year}</span>
                </TableCell>
                <TableCell>{item.text}</TableCell>
                <TableCell>
                  {item.image && (
                    <img 
                      src={resolveBackendUrl(item.image)} 
                      alt={item.text} 
                      className={styles['adm-image-preview']}
                    />
                  )}
                </TableCell>
                <TableCell align="right">
                  <div className={styles['adm-actions-cell']}>
                    <IconButton 
                      size="small" 
                      onClick={() => setEditingEvent(item)}
                      sx={{ color: 'var(--primary-color)' }}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      onClick={() => {
                        if (confirm('Удалить событие?')) deleteTimeline(item.id);
                      }}
                      sx={{ color: 'var(--error-color)' }}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {timeline?.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center" sx={{ py: 3, color: '#999' }}>
                  Событий пока нет
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {editingEvent && (
        <EditTimelineModal 
          event={editingEvent}
          isOpen={true}
          onClose={() => setEditingEvent(null)}
        />
      )}
    </div>
  );
};
