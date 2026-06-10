import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  IconButton, 
  CircularProgress,
  Box,
  Typography
} from '@mui/material';
import { Close as CloseIcon, PhotoCamera as PhotoIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { 
  useGetSubdistrictDetailQuery, 
  useUpdateSubdistrictMutation, 
  useUpdateSubdistrictImageMutation,
  useDeleteSubdistrictImageMutation
} from '../../api/subdistrictsApi';
import { resolveBackendUrl } from '@/config/env';
import styles from '@/styles/admin.module.css';

interface Props {
  subdistrictName: string;
  isOpen: boolean;
  onClose: () => void;
}

export const EditSubdistrictModal = ({ subdistrictName, isOpen, onClose }: Props) => {
  const { data: subdistrict, isLoading: isFetching } = useGetSubdistrictDetailQuery(subdistrictName, { skip: !isOpen });
  const [updateSubdistrict, { isLoading: isUpdating }] = useUpdateSubdistrictMutation();
  const [updateImage, { isLoading: isUpdatingImage }] = useUpdateSubdistrictImageMutation();
  const [deleteImage] = useDeleteSubdistrictImageMutation();

  const { register, handleSubmit, reset } = useForm<{ description: string }>();

  useEffect(() => {
    if (subdistrict) {
      reset({
        description: subdistrict.description || '',
      });
    }
  }, [subdistrict, reset]);

  const onSubmit = async (data: { description: string }) => {
    try {
      await updateSubdistrict({ name: subdistrictName, data }).unwrap();
      alert('Данные обновлены');
      onClose();
    } catch (e) {
      console.error(e);
      alert('Ошибка при обновлении');
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      try {
        await updateImage({ name: subdistrictName, image: e.target.files[0] }).unwrap();
      } catch (e) {
        console.error(e);
        alert('Ошибка при загрузке изображения');
      }
    }
  };

  if (isFetching) return null;

  return (
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle sx={{ m: 0, p: 3, fontWeight: 800 }}>
        Редактировать подрайон: {subdistrictName}
        <IconButton
          onClick={onClose}
          sx={{ position: 'absolute', right: 16, top: 16, color: (theme) => theme.palette.grey[500] }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      
      <DialogContent dividers sx={{ p: 4 }}>
        <form onSubmit={handleSubmit(onSubmit)} id="edit-subdistrict-form" className={styles['adm-form']}>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Описание подрайона</label>
            <textarea 
              {...register('description')} 
              className={`${styles['adm-input']} ${styles['adm-textarea']}`} 
              rows={8}
              placeholder="Введите описание для отображения на карте..."
            />
          </div>

          <div className={`${styles['adm-form-group']} ${styles['adm-mt-20']}`}>
            <label className={styles['adm-label']}>Изображение подрайона</label>
            {subdistrict?.image ? (
              <Box className={styles['adm-img-preview-container']} sx={{ maxWidth: '400px' }}>
                <img 
                  src={resolveBackendUrl(subdistrict.image)} 
                  alt={subdistrict.name} 
                  className={styles['adm-img-full']}
                />
                <IconButton 
                  onClick={() => { if(confirm('Удалить изображение?')) deleteImage(subdistrictName); }}
                  sx={{ position: 'absolute', top: 8, right: 8, bgcolor: 'rgba(255,255,255,0.8)', color: 'error.main' }}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            ) : (
              <Box className={styles['adm-placeholder-box']}>
                <PhotoIcon sx={{ fontSize: 48, color: '#ccc' }} />
                <Typography sx={{ color: '#999' }}>Изображение не установлено</Typography>
              </Box>
            )}
            <Button 
              component="label" 
              variant="outlined" 
              startIcon={<PhotoIcon />}
              disabled={isUpdatingImage}
              sx={{ width: 'fit-content' }}
            >
              {isUpdatingImage ? 'Загрузка...' : (subdistrict?.image ? 'Изменить фото' : 'Загрузить фото')}
              <input type="file" hidden accept="image/*" onChange={handleImageUpload} />
            </Button>
          </div>
        </form>

        {subdistrict?.enterprises && subdistrict.enterprises.length > 0 && (
          <div className={styles['adm-mt-20']}>
            <h4 className={styles['adm-label']}>Предприятия в этом подрайоне:</h4>
            <ul className={styles['adm-subdistrict-list']}>
              {subdistrict.enterprises.map(ent => (
                <li key={ent.id}>{ent.title}</li>
              ))}
            </ul>
          </div>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button onClick={onClose} color="inherit">Отмена</Button>
        <Button 
          type="submit" 
          form="edit-subdistrict-form" 
          variant="contained" 
          disabled={isUpdating}
          sx={{ bgcolor: 'var(--primary-color)', '&:hover': { bgcolor: 'var(--primary-hover)' } }}
        >
          {isUpdating ? <CircularProgress size={24} color="inherit" /> : 'Сохранить'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
