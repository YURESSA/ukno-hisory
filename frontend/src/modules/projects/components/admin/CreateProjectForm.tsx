import { useForm, useWatch } from 'react-hook-form';
import { Button, CircularProgress, FormControlLabel, Checkbox } from '@mui/material';
import { CloudUpload as UploadIcon, Collections as GalleryIcon } from '@mui/icons-material';
import { useCreateProjectMutation } from '../../api/projectsApi';
import styles from '@/styles/admin.module.css';

import { CreateProjectFormData } from '../../types';

export const CreateProjectForm = () => {
  const { register, handleSubmit, reset, control } = useForm<CreateProjectFormData>();
  const [createProject, { isLoading }] = useCreateProjectMutation();

  const galleryFiles = useWatch({ control, name: 'gallery' });
  const mainImageFile = useWatch({ control, name: 'main_image' });

  const onSubmit = async (data: CreateProjectFormData) => {
    const formData = new FormData();
    
    formData.append('title', data.title);
    formData.append('author', data.author);
    formData.append('short_description', data.short_description);
    formData.append('description', data.description);
    formData.append('year', data.year);
    formData.append('tag_one', data.tag_one);
    formData.append('tag_two', data.tag_two);
    formData.append('is_draft', String(data.is_draft));

    if (data.main_image?.[0]) {
      formData.append('main_image', data.main_image[0]);
    }

    if (data.gallery) {
      Array.from(data.gallery).forEach((file) => {
        formData.append('gallery', file);
      });
    }

    try {
      await createProject(formData).unwrap();
      alert('Проект создан!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <div className={styles['adm-card']}>
      <h3 className={styles['adm-title']}>Создать проект</h3>
      <form onSubmit={handleSubmit(onSubmit)} className={styles['adm-form']}>
        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Название проекта</label>
          <input {...register('title')} placeholder="Название" className={styles['adm-input']} required />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Автор</label>
          <input {...register('author')} placeholder="Имя студента" className={styles['adm-input']} />
        </div>

        <div className={styles['adm-module-row']} style={{ gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' }}>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Год</label>
            <input type="number" {...register('year')} placeholder="2024" className={styles['adm-input']} />
          </div>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Тег 1</label>
            <input {...register('tag_one')} placeholder="Web" className={styles['adm-input']} />
          </div>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Тег 2</label>
            <input {...register('tag_two')} placeholder="React" className={styles['adm-input']} />
          </div>
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Краткое описание</label>
          <textarea {...register('short_description')} placeholder="Для карточки проекта..." className={`${styles['adm-input']} ${styles['adm-textarea']}`} />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Полное описание</label>
          <textarea {...register('description')} placeholder="Детальное описание проекта..." rows={4} className={`${styles['adm-input']} ${styles['adm-textarea']}`} />
        </div>
        
        <div className={styles['adm-form-group']}>
          <FormControlLabel
            control={<Checkbox {...register('is_draft')} color="primary" />}
            label="Сохранить как черновик"
            sx={{ '& .MuiFormControlLabel-label': { fontSize: '0.9rem', fontWeight: 500 } }}
          />
        </div>

        <div className={styles['adm-module-row']} style={{ gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Главное фото</label>
            <div 
              className={styles['adm-file-upload']} 
              onClick={() => document.getElementById('main-image-input')?.click()}
              style={{ padding: '20px', borderColor: mainImageFile?.[0] ? 'var(--primary-color)' : '' }}
            >
              <UploadIcon sx={{ fontSize: 24, color: mainImageFile?.[0] ? 'var(--primary-color)' : '#ccc' }} />
              <p style={{ margin: '5px 0 0 0', fontSize: '0.75rem' }}>
                {mainImageFile?.[0] ? 'Фото выбрано' : 'Выбрать'}
              </p>
              <input 
                id="main-image-input"
                type="file" 
                {...register('main_image')} 
                accept="image/*" 
                style={{ display: 'none' }} 
              />
            </div>
          </div>

          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Галерея</label>
            <div 
              className={styles['adm-file-upload']} 
              onClick={() => document.getElementById('gallery-input')?.click()}
              style={{ padding: '20px', borderColor: galleryFiles?.length ? 'var(--primary-color)' : '' }}
            >
              <GalleryIcon sx={{ fontSize: 24, color: galleryFiles?.length ? 'var(--primary-color)' : '#ccc' }} />
              <p style={{ margin: '5px 0 0 0', fontSize: '0.75rem' }}>
                {galleryFiles?.length ? `Выбрано: ${galleryFiles.length}` : 'Выбрать (можно сразу несколько)'}
              </p>
              <input 
                id="gallery-input"
                type="file" 
                {...register('gallery')} 
                accept="image/*" 
                multiple
                style={{ display: 'none' }} 
              />
            </div>
          </div>
        </div>

        <Button 
          type="submit" 
          variant="contained" 
          disabled={isLoading}
          fullWidth
          size="large"
          sx={{ 
            bgcolor: 'var(--primary-color)', 
            '&:hover': { bgcolor: 'var(--primary-hover)' },
            py: 1.5,
            borderRadius: '8px',
            boxShadow: 'none',
            mt: 1
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Создать проект'}
        </Button>
      </form>
    </div>
  );
};
