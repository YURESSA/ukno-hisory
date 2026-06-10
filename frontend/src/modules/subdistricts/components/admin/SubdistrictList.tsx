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
  CircularProgress,
  Tooltip,
  Typography
} from '@mui/material';
import { Edit as EditIcon, Image as ImageIcon, ImageNotSupported as NoImageIcon } from '@mui/icons-material';
import { useGetSubdistrictsQuery } from '../../api/subdistrictsApi';
import { EditSubdistrictModal } from './EditSubdistrictModal';
import styles from '@/styles/admin.module.css';

export const SubdistrictList = () => {
  const { data: subdistricts, isLoading, error } = useGetSubdistrictsQuery();
  const [editingName, setEditingName] = useState<string | null>(null);

  if (isLoading) return (
    <div className={`${styles['adm-card']} ${styles['adm-flex-center']}`} style={{ minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );
  
  if (error) return (
    <div className={styles['adm-card']}>
      <Typography sx={{ color: 'var(--error-color)' }}>Ошибка загрузки подрайонов</Typography>
    </div>
  );

  return (
    <div className={styles['adm-card']}>
      <h3 className={styles['adm-title']}>Управление подрайонами</h3>
      <p className={styles['adm-description']}>
        Здесь вы можете отредактировать описания и изображения подрайонов для интерактивной карты.
      </p>

      <TableContainer component={Paper} className={styles['adm-table-container']}>
        <Table>
          <TableHead className={styles['adm-mui-table-head']}>
            <TableRow>
              <TableCell>Название подрайона</TableCell>
              <TableCell>Описание</TableCell>
              <TableCell width={100}>Фото</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {subdistricts?.map((sub) => (
              <TableRow key={sub.name} hover>
                <TableCell sx={{ fontWeight: 600 }}>{sub.name}</TableCell>
                <TableCell>
                  {sub.description ? (
                    <span className={styles['adm-text-ellipsis-2']}>
                      {sub.description}
                    </span>
                  ) : (
                    <em style={{ color: '#ccc' }}>Нет описания</em>
                  )}
                </TableCell>
                <TableCell>
                  {sub.image ? (
                    <Tooltip title="Изображение установлено">
                      <ImageIcon color="primary" />
                    </Tooltip>
                  ) : (
                    <Tooltip title="Нет изображения">
                      <NoImageIcon style={{ color: '#ccc' }} />
                    </Tooltip>
                  )}
                </TableCell>
                <TableCell align="right">
                  <IconButton 
                    size="small" 
                    onClick={() => setEditingName(sub.name)}
                    sx={{ color: 'var(--primary-color)' }}
                  >
                    <EditIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {editingName && (
        <EditSubdistrictModal 
          subdistrictName={editingName} 
          isOpen={true} 
          onClose={() => setEditingName(null)} 
        />
      )}
    </div>
  );
};
