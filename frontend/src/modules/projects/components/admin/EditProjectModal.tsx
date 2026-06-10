import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { 
  useGetAdminProjectQuery, 
  useUpdateProjectMutation, 
  useAddGalleryImagesMutation, 
  useDeleteGalleryImageMutation,
  useUpdateProjectMainImageMutation,
  useDeleteProjectMainImageMutation
} from '../../api/projectsApi';
import { resolveBackendUrl } from '@/config/env';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  IconButton,
  Button,
  CircularProgress,
  FormControlLabel,
  Checkbox,
  Tooltip,
  Box
} from '@mui/material';
import { 
  Close as CloseIcon, 
  AddPhotoAlternate as AddIcon,
  Delete as DeleteIcon,
  PhotoCamera as PhotoIcon
} from '@mui/icons-material';
import styles from '@/styles/admin.module.css';

interface Props {
  projectId: number;
  isOpen: boolean;
  onClose: () => void;
}

import { UpdateProjectFormData } from '../../types';

export const EditProjectModal = ({ projectId, isOpen, onClose }: Props) => {
  const { data: project, isLoading: isFetching } = useGetAdminProjectQuery(projectId, { skip: !isOpen });
  const [updateProject, { isLoading: isUpdating }] = useUpdateProjectMutation();
  const [addGalleryImages] = useAddGalleryImagesMutation();
  const [deleteGalleryImage] = useDeleteGalleryImageMutation();
  const [updateMainImage] = useUpdateProjectMainImageMutation();
  const [deleteMainImage] = useDeleteProjectMainImageMutation();

  const { register, handleSubmit, reset } = useForm<UpdateProjectFormData>();

  useEffect(() => {
    if (project) {
      reset({
        title: project.title || '',
        author: project.author || '',
        short_description: project.short_description || '',
        description: project.description || '',
        year: project.year || 0,
        tag_one: project.tag_one || '',
        tag_two: project.tag_two || '',
        is_draft: project.is_draft,
      });
    }
  }, [project, reset]);

  const onSubmit = async (data: UpdateProjectFormData) => {
    try {
      await updateProject({ id: projectId, data }).unwrap();
      alert('Проект обновлен!');
      onClose();
    } catch (e) {
      console.error(e);
      alert('Ошибка при обновлении');
    }
  };

  const handleMainImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      try {
        await updateMainImage({ id: projectId, image: e.target.files[0] }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleGalleryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const formData = new FormData();
      Array.from(e.target.files).forEach(file => {
        formData.append('images', file);
      });
      try {
        await addGalleryImages({ id: projectId, formData }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  if (isFetching) return null;

  return (
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="lg">
      <DialogTitle sx={{ m: 0, p: 3, fontWeight: 800, fontSize: '22px', color: 'var(--secondary-color)' }}>
        Редактирование проекта #{projectId}
        <IconButton
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 16,
            top: 16,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      
      <DialogContent dividers sx={{ p: 4 }}>
        <form onSubmit={handleSubmit(onSubmit)} id="edit-project-form" className={styles['adm-form']}>
          <div className={styles['adm-module-row-2-1']}>
            <div className={styles['adm-flex-main']}>
              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Название проекта</label>
                <input {...register('title')} className={styles['adm-input']} required />
              </div>

              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Автор</label>
                <input {...register('author')} className={styles['adm-input']} />
              </div>

              <div className={styles['adm-grid-3']}>
                <div className={styles['adm-form-group']}>
                  <label className={styles['adm-label']}>Год</label>
                  <input type="number" {...register('year')} className={styles['adm-input']} />
                </div>
                <div className={styles['adm-form-group']}>
                  <label className={styles['adm-label']}>Тег 1</label>
                  <input {...register('tag_one')} className={styles['adm-input']} />
                </div>
                <div className={styles['adm-form-group']}>
                  <label className={styles['adm-label']}>Тег 2</label>
                  <input {...register('tag_two')} className={styles['adm-input']} />
                </div>
              </div>

              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Краткое описание</label>
                <textarea {...register('short_description')} className={`${styles['adm-input']} ${styles['adm-textarea']}`} rows={2} />
              </div>

              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Полное описание</label>
                <textarea {...register('description')} className={`${styles['adm-input']} ${styles['adm-textarea']}`} rows={6} />
              </div>

              <FormControlLabel
                control={<Checkbox {...register('is_draft')} color="primary" />}
                label="Черновик (не показывать на сайте)"
                sx={{ '& .MuiFormControlLabel-label': { fontSize: '14px', fontWeight: 600 } }}
              />
            </div>

            <div className={styles['adm-flex-sidebar']}>
              <div className={styles['adm-form-group']}>
                <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`}>
                  Главное фото
                </h4>
                
                {project?.main_image ? (
                  <div className={styles['adm-img-preview-container']}>
                    <img src={resolveBackendUrl(project.main_image)} className={styles['adm-img-full']} alt="" />
                    <div className={styles['adm-abs-top-right']}>
                      <Tooltip title="Удалить главное фото">
                        <IconButton 
                          size="small" 
                          onClick={() => { if(confirm('Удалить главное фото?')) deleteMainImage(projectId); }}
                          sx={{ bgcolor: 'rgba(255,255,255,0.9)', color: 'var(--error-color)', '&:hover': { bgcolor: 'var(--error-color)', color: '#fff' } }}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </div>
                  </div>
                ) : (
                  <div className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${styles['adm-mb-15']}`}>
                    <PhotoIcon sx={{ fontSize: 32, color: '#ccc' }} />
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>Главное фото не задано</p>
                  </div>
                )}
                
                <Button
                  component="label"
                  variant="outlined"
                  size="small"
                  startIcon={<PhotoIcon />}
                  fullWidth
                  sx={{ borderRadius: '8px', textTransform: 'none' }}
                >
                  {project?.main_image ? 'Заменить главное фото' : 'Установить главное фото'}
                  <input type="file" onChange={handleMainImageUpload} hidden accept="image/*" />
                </Button>
              </div>

              <div className={styles['adm-form-group']}>
                <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`} style={{ marginTop: '10px' }}>
                  Галерея проекта
                </h4>
                
                <div className={styles['adm-gallery-2col']}>
                  {project?.gallery.map((img) => (
                    <div key={img.id} className={styles['adm-gallery-item-50']}>
                      <img 
                        src={resolveBackendUrl(img.image)} 
                        alt="" 
                        className={styles['adm-img-full']}
                      />
                      <IconButton 
                        size="small"
                        onClick={() => deleteGalleryImage({ projectId, imageId: img.id })}
                        sx={{ 
                          position: 'absolute', 
                          top: 4, 
                          right: 4, 
                          bgcolor: 'rgba(255,255,255,0.9)',
                          color: 'var(--error-color)',
                          '&:hover': { bgcolor: 'var(--error-color)', color: '#fff' }
                        }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </div>
                  ))}
                </div>

                <Button
                  component="label"
                  variant="outlined"
                  startIcon={<AddIcon />}
                  className={styles['adm-btn-dashed']}
                  sx={{ 
                    mt: 1,
                    py: 2, 
                    color: 'var(--primary-color)',
                    borderColor: 'var(--primary-color)',
                  }}
                >
                  Добавить в галерею
                  <input type="file" multiple onChange={handleGalleryUpload} hidden accept="image/*" />
                </Button>
              </div>
            </div>
          </div>
        </form>
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 2 }}>
        <Button onClick={onClose} sx={{ color: '#666', fontWeight: 600 }}>
          Отмена
        </Button>
        <Button 
          type="submit" 
          form="edit-project-form" 
          variant="contained"
          disabled={isUpdating}
          sx={{ 
            bgcolor: 'var(--primary-color)', 
            px: 4,
            py: 1.2,
            borderRadius: '8px',
            boxShadow: 'none',
            '&:hover': { bgcolor: 'var(--primary-hover)', boxShadow: 'none' }
          }}
        >
          {isUpdating ? <CircularProgress size={24} color="inherit" /> : 'Сохранить изменения'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
