import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { 
  useGetAdminProjectQuery, 
  useUpdateProjectMutation, 
  useAddGalleryImagesMutation, 
  useDeleteGalleryImageMutation 
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
  Checkbox
} from '@mui/material';
import { 
  Close as CloseIcon, 
  AddPhotoAlternate as AddIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';

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
      <DialogTitle sx={{ m: 0, p: 3, fontWeight: 800, fontSize: '1.4rem', color: 'var(--secondary-color)' }}>
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
        <form onSubmit={handleSubmit(onSubmit)} id="edit-project-form" className="adm-form">
          <div className="adm-module-row" style={{ gridTemplateColumns: '1fr 350px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              <div className="adm-form-group">
                <label className="adm-label">Название проекта</label>
                <input {...register('title')} className="adm-input" required />
              </div>

              <div className="adm-form-group">
                <label className="adm-label">Автор</label>
                <input {...register('author')} className="adm-input" />
              </div>

              <div className="adm-module-row" style={{ gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' }}>
                <div className="adm-form-group">
                  <label className="adm-label">Год</label>
                  <input type="number" {...register('year')} className="adm-input" />
                </div>
                <div className="adm-form-group">
                  <label className="adm-label">Тег 1</label>
                  <input {...register('tag_one')} className="adm-input" />
                </div>
                <div className="adm-form-group">
                  <label className="adm-label">Тег 2</label>
                  <input {...register('tag_two')} className="adm-input" />
                </div>
              </div>

              <div className="adm-form-group">
                <label className="adm-label">Краткое описание</label>
                <textarea {...register('short_description')} className="adm-input adm-textarea" rows={2} />
              </div>

              <div className="adm-form-group">
                <label className="adm-label">Полное описание</label>
                <textarea {...register('description')} className="adm-input adm-textarea" rows={6} />
              </div>

              <FormControlLabel
                control={<Checkbox {...register('is_draft')} color="primary" />}
                label="Черновик (не показывать на сайте)"
                sx={{ '& .MuiFormControlLabel-label': { fontSize: '0.9rem', fontWeight: 600 } }}
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <h4 className="adm-label" style={{ borderBottom: '2px solid var(--accent-color-1)', paddingBottom: '8px', marginBottom: '8px' }}>
                Галерея проекта
              </h4>
              
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(2, 1fr)', 
                gap: '12px',
                maxHeight: '450px',
                overflowY: 'auto',
                padding: '4px'
              }}>
                {project?.gallery.map((img) => (
                  <div key={img.id} style={{ 
                    position: 'relative', 
                    borderRadius: '12px', 
                    overflow: 'hidden',
                    aspectRatio: '1/1',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                  }}>
                    <img 
                      src={resolveBackendUrl(img.image)} 
                      alt="" 
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
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
                sx={{ 
                  py: 4, 
                  borderStyle: 'dashed', 
                  borderRadius: '12px',
                  color: 'var(--primary-color)',
                  borderColor: 'var(--primary-color)',
                  '&:hover': { borderStyle: 'dashed', bgcolor: 'var(--accent-color-2)' }
                }}
              >
                Добавить фото
                <input type="file" multiple onChange={handleGalleryUpload} hidden accept="image/*" />
              </Button>
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
