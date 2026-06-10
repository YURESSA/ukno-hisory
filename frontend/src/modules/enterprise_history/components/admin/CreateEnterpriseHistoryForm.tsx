import { useState } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { Button, CircularProgress, FormControlLabel, Checkbox, IconButton, TextField, Box } from '@mui/material';
import { 
  CloudUpload as UploadIcon, 
  Collections as GalleryIcon,
  AddPhotoAlternate as AddIcon,
  Delete as DeleteIcon,
  PhotoCamera as PhotoIcon
} from '@mui/icons-material';
import { 
  useCreateEnterpriseHistoryMutation,
  useAddHistorySlideMutation
} from '../../api/enterpriseHistoryApi';
import { useGetSubdistrictsQuery } from '@/modules/subdistricts/api/subdistrictsApi';

import { CreateEnterpriseHistoryFormData } from '../../types';
import styles from '@/styles/admin.module.css';

export const CreateEnterpriseHistoryForm = () => {
  const { register, handleSubmit, reset, control } = useForm<CreateEnterpriseHistoryFormData>();
  const [createHistory, { isLoading }] = useCreateEnterpriseHistoryMutation();
  const [addSlide] = useAddHistorySlideMutation();
  const { data: subdistricts, isLoading: isSubdistrictsLoading } = useGetSubdistrictsQuery();

  const [tempSlides, setTempSlides] = useState<{ text: string, image: File | null }[]>([]);

  const mainImage = useWatch({ control, name: 'general_main_image' });
  const detailImage = useWatch({ control, name: 'detail_main_image' });
  const gallery = useWatch({ control, name: 'gallery' });

  const handleAddTempSlide = () => {
    setTempSlides([...tempSlides, { text: '', image: null }]);
  };

  const handleRemoveTempSlide = (index: number) => {
    setTempSlides(tempSlides.filter((_, i) => i !== index));
  };

  const handleSlideTextChange = (index: number, text: string) => {
    const newSlides = [...tempSlides];
    newSlides[index].text = text;
    setTempSlides(newSlides);
  };

  const handleSlideImageChange = (index: number, file: File | null) => {
    const newSlides = [...tempSlides];
    newSlides[index].image = file;
    setTempSlides(newSlides);
  };

  const onSubmit = async (data: CreateEnterpriseHistoryFormData) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('subdistrict', data.subdistrict);
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
      const result = await createHistory(formData).unwrap();
      
      for (const slide of tempSlides) {
        const slideFormData = new FormData();
        if (slide.text) slideFormData.append('text', slide.text);
        if (slide.image) slideFormData.append('image', slide.image);
        
        if (slide.text || slide.image) {
          await addSlide({ id: result.id, formData: slideFormData }).unwrap();
        }
      }

      alert('Запись создана!');
      reset();
      setTempSlides([]);
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
          <label className={styles['adm-label']}>Подрайон</label>
          <select {...register('subdistrict')} className={styles['adm-input']} required disabled={isSubdistrictsLoading}>
            <option value="">{isSubdistrictsLoading ? 'Загрузка...' : 'Выберите подрайон'}</option>
            {subdistricts?.map(sub => (
              <option key={sub.name} value={sub.name}>{sub.name}</option>
            ))}
          </select>
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
          <label className={styles['adm-label']}>Описание</label>
          <textarea {...register('short_description')} className={`${styles['adm-input']} ${styles['adm-textarea']}`} placeholder="Описание для ленты..." rows={3} />
        </div>
        
        <div className={styles['adm-form-group']}>
          <FormControlLabel
            control={<Checkbox {...register('is_draft')} color="primary" defaultChecked />}
            label="Сохранить как черновик"
            sx={{ '& .MuiFormControlLabel-label': { fontSize: '14px', fontWeight: 500 } }}
          />
        </div>

        <div className={styles['adm-flex-3col']}>
          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Главное фото (На странице с лентой)</label>
            <div 
              className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${mainImage?.[0] ? styles['adm-file-upload-active'] : ''}`}
              onClick={() => document.getElementById('gen-img')?.click()}
            >
              <UploadIcon sx={{ fontSize: 24, color: mainImage?.[0] ? 'var(--primary-color)' : '#ccc' }} />
              <p className={styles['adm-file-upload-text']}>{mainImage?.[0] ? 'Выбрано' : 'Список'}</p>
              <input id="gen-img" type="file" {...register('general_main_image')} accept="image/*" style={{ display: 'none' }} />
            </div>
          </div>

          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Главное фото (На странице предприятия)</label>
            <div 
              className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${detailImage?.[0] ? styles['adm-file-upload-active'] : ''}`}
              onClick={() => document.getElementById('det-img')?.click()}
            >
              <UploadIcon sx={{ fontSize: 24, color: detailImage?.[0] ? 'var(--primary-color)' : '#ccc' }} />
              <p className={styles['adm-file-upload-text']}>{detailImage?.[0] ? 'Выбрано' : 'Страница'}</p>
              <input id="det-img" type="file" {...register('detail_main_image')} accept="image/*" style={{ display: 'none' }} />
            </div>
          </div>

          <div className={styles['adm-form-group']}>
            <label className={styles['adm-label']}>Галерея (Несколько фото)</label>
            <div 
              className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${gallery?.length ? styles['adm-file-upload-active'] : ''}`}
              onClick={() => document.getElementById('gal-img')?.click()}
            >
              <GalleryIcon sx={{ fontSize: 24, color: gallery?.length ? 'var(--primary-color)' : '#ccc' }} />
              <p className={styles['adm-file-upload-text']}>{gallery?.length ? `Выбрано: ${gallery.length}` : '0 фото'}</p>
              <input id="gal-img" type="file" {...register('gallery')} accept="image/*" multiple style={{ display: 'none' }} />
            </div>
          </div>
        </div>

        <div className={`${styles['adm-form-group']} ${styles['adm-mt-20']}`}>
          <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`}>Слайды ("Как это было")</h4>
          
          <div className={styles['adm-temp-slide-container']}>
            {tempSlides.map((slide, index) => (
              <div key={index} className={styles['adm-temp-slide']}>
                <IconButton 
                  onClick={() => handleRemoveTempSlide(index)}
                  sx={{ position: 'absolute', top: 5, right: 5, color: 'var(--error-color)' }}
                  size="small"
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
                
                <TextField
                  multiline
                  rows={2}
                  fullWidth
                  placeholder="Текст слайда..."
                  value={slide.text}
                  onChange={(e) => handleSlideTextChange(index, e.target.value)}
                  sx={{ mb: 1, bgcolor: '#fff' }}
                  size="small"
                />
                <Box sx={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                  <Button 
                    component="label" 
                    variant="outlined" 
                    size="small" 
                    startIcon={<PhotoIcon />}
                    sx={{ flex: 1, textTransform: 'none', borderRadius: '8px', bgcolor: slide.image ? 'var(--accent-color-2)' : '#fff' }}
                  >
                    {slide.image ? 'Фото выбрано' : 'Добавить фото'}
                    <input type="file" hidden accept="image/*" onChange={(e) => handleSlideImageChange(index, e.target.files?.[0] || null)} />
                  </Button>
                </Box>
              </div>
            ))}
            
            <Button 
              variant="outlined" 
              startIcon={<AddIcon />} 
              onClick={handleAddTempSlide}
              sx={{ borderRadius: '8px', textTransform: 'none', borderStyle: 'dashed' }}
            >
              Добавить слайд
            </Button>
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
            mt: 3
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Создать запись'}
        </Button>
      </form>
    </div>
  );
};
