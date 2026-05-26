import { useForm, useWatch } from 'react-hook-form';
import { Button, CircularProgress, FormControlLabel, Checkbox } from '@mui/material';
import { CloudUpload as UploadIcon, Collections as GalleryIcon } from '@mui/icons-material';
import { useCreateEnterpriseHistoryMutation } from '../../api/enterpriseHistoryApi';

import { CreateEnterpriseHistoryFormData } from '../../types';
import styles from '@/styles/admin.module.css';

export const CreateEnterpriseHistoryForm = () => {
  const { register, handleSubmit, reset, control } = useForm<CreateEnterpriseHistoryFormData>();
  const [createHistory, { isLoading }] = useCreateEnterpriseHistoryMutation();

  const mainImage = useWatch({ control, name: 'general_main_image' });
  const detailImage = useWatch({ control, name: 'detail_main_image' });
  const gallery = useWatch({ control, name: 'gallery' });

  const onSubmit = async (data: CreateEnterpriseHistoryFormData) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('general_subtitle', data.general_subtitle);
    formData.append('detail_subtitle', data.detail_subtitle);
    formData.append('short_description', data.short_description);
    formData.append('is_draft', String(data.is_draft));

    if (data.general_main_image?.[0]) {
      formData.append('general_main_image', data.general_main_image[0]);
    }
    if (data.detail_main_image?.[0]) {
      formData.append('detail_main_image', data.detail_main_image[0]);
    }

    if (data.gallery) {
      Array.from(data.gallery).forEach((file) => {
        formData.append('gallery', file);
      });
    }

    try {
      await createHistory(formData).unwrap();
      alert('Запись создана!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <div className={styles['adm-card']}>
      <h3 className={styles['adm-title']}>Создать историю предприятия</h3>
      <form onSubmit={handleSubmit(onSubmit)} className={styles['adm-form']}>
        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Заголовок</label>
          <input {...register('title')} className={styles['adm-input']} placeholder="Название предприятия" required />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Подзаголовок (общий)</label>
          <input {...register('general_subtitle')} className={styles['adm-input']} placeholder="Краткий слоган" />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Подзаголовок (детальный)</label>
          <input {...register('detail_subtitle')} className={styles['adm-input']} placeholder="Более подробный подзаголовок" />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Краткое описание</label>
          <textarea {...register('short_description')} className={`${styles['adm-input']} ${styles['adm-textarea']}`} placeholder="Описание для ленты..." rows={3} />
        </div>
        
        <div className={styles['adm-form-group']}>
          <FormControlLabel
            control={<Checkbox {...register('is_draft')} color="primary" defaultChecked />}
            label="Сохранить как черновик"
            sx={{ '& .MuiFormControlLabel-label': { fontSize: '0.9rem', fontWeight: 500 } }}
          />
        </div>

        <div className={styles['adm-module-row']} style={{ gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' }}>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Главное фото (На странице с лентой)</label>
            <div 
              className={styles['adm-file-upload']} 
              style={{ padding: '20px', borderColor: mainImage?.[0] ? 'var(--primary-color)' : '' }} 
              onClick={() => document.getElementById('gen-img')?.click()}
            >
              <UploadIcon sx={{ fontSize: 24, color: mainImage?.[0] ? 'var(--primary-color)' : '#ccc' }} />
              <p style={{ margin: '5px 0 0 0', fontSize: '0.7rem' }}>{mainImage?.[0] ? 'Выбрано' : 'Список'}</p>
              <input id="gen-img" type="file" {...register('general_main_image')} accept="image/*" style={{ display: 'none' }} />
            </div>
          </div>

          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Главное фото (На странице предприятия)</label>
            <div 
              className={styles['adm-file-upload']} 
              style={{ padding: '20px', borderColor: detailImage?.[0] ? 'var(--primary-color)' : '' }} 
              onClick={() => document.getElementById('det-img')?.click()}
            >
              <UploadIcon sx={{ fontSize: 24, color: detailImage?.[0] ? 'var(--primary-color)' : '#ccc' }} />
              <p style={{ margin: '5px 0 0 0', fontSize: '0.7rem' }}>{detailImage?.[0] ? 'Выбрано' : 'Страница'}</p>
              <input id="det-img" type="file" {...register('detail_main_image')} accept="image/*" style={{ display: 'none' }} />
            </div>
          </div>

          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Галерея (Несколько фото)</label>
            <div 
              className={styles['adm-file-upload']} 
              style={{ padding: '20px', borderColor: gallery?.length ? 'var(--primary-color)' : '' }} 
              onClick={() => document.getElementById('gal-img')?.click()}
            >
              <GalleryIcon sx={{ fontSize: 24, color: gallery?.length ? 'var(--primary-color)' : '#ccc' }} />
              <p style={{ margin: '5px 0 0 0', fontSize: '0.7rem' }}>{gallery?.length ? `Выбрано: ${gallery.length}` : '0 фото'}</p>
              <input id="gal-img" type="file" {...register('gallery')} accept="image/*" multiple style={{ display: 'none' }} />
            </div>
          </div>
        </div>

        <Button 
          type="submit" 
          variant="contained" 
          disabled={isLoading}
          fullWidth
          sx={{ 
            bgcolor: 'var(--primary-color)', 
            '&:hover': { bgcolor: 'var(--primary-hover)' },
            py: 1.5,
            borderRadius: '8px',
            boxShadow: 'none',
            mt: 1
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Создать запись'}
        </Button>
      </form>
    </div>
  );
};
