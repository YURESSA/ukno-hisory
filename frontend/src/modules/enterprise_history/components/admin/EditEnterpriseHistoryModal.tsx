import { useForm } from 'react-hook-form';
import { useEffect, useState } from 'react';
import { 
  useGetAdminEnterpriseHistoryQuery, 
  useUpdateEnterpriseHistoryMutation, 
  useAddHistorySlideMutation, 
  useDeleteHistorySlideMutation,
  useAddHistoryGalleryImagesMutation,
  useDeleteHistoryGalleryImageMutation,
  useUpdateHistoryGeneralMainImageMutation,
  useUpdateHistoryDetailMainImageMutation,
  useReorderHistorySlidesMutation
} from '../../api/enterpriseHistoryApi';
import { useGetSubdistrictsQuery } from '@/modules/subdistricts/api/subdistrictsApi';
import { resolveBackendUrl } from '@/config/env';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  IconButton,
  FormControlLabel,
  Checkbox,
  Button,
  CircularProgress,
  TextField,
  Box,
  Typography
} from '@mui/material';
import { 
  Close as CloseIcon, 
  PhotoCamera as PhotoIcon,
  AddPhotoAlternate as AddIcon,
  ArrowUpward as UpIcon,
  ArrowDownward as DownIcon
} from '@mui/icons-material';
import styles from '@/styles/admin.module.css';

interface Props {
  itemId: number;
  isOpen: boolean;
  onClose: () => void;
}

import { UpdateEnterpriseHistoryFormData } from '../../types';

export const EditEnterpriseHistoryModal = ({ itemId, isOpen, onClose }: Props) => {
  const { data: item, isLoading: isFetching } = useGetAdminEnterpriseHistoryQuery(itemId, { skip: !isOpen });
  const [updateItem, { isLoading: isUpdating }] = useUpdateEnterpriseHistoryMutation();
  const [addSlide, { isLoading: isAddingSlide }] = useAddHistorySlideMutation();
  const [deleteSlide] = useDeleteHistorySlideMutation();
  const [addGallery] = useAddHistoryGalleryImagesMutation();
  const [deleteGallery] = useDeleteHistoryGalleryImageMutation();
  const [updateGeneralImage] = useUpdateHistoryGeneralMainImageMutation();
  const [updateDetailImage] = useUpdateHistoryDetailMainImageMutation();
  const [reorderSlides] = useReorderHistorySlidesMutation();
  const { data: subdistricts, isLoading: isSubdistrictsLoading } = useGetSubdistrictsQuery();

  const { register, handleSubmit, reset } = useForm<UpdateEnterpriseHistoryFormData>();

  const [newSlideText, setNewSlideText] = useState('');
  const [newSlideImage, setNewSlideImage] = useState<File | null>(null);

  useEffect(() => {
    if (item) {
      reset({
        title: item.title || '',
        subdistrict: item.subdistrict || '',
        general_subtitle: item.general_subtitle || '',
        detail_subtitle: item.detail_subtitle || '',
        short_description: item.short_description || '',
        is_draft: item.is_draft,
      });
    }
  }, [item, reset]);

  const onSubmit = async (data: UpdateEnterpriseHistoryFormData) => {
    try {
      await updateItem({ id: itemId, data }).unwrap();
      alert('Обновлено!');
      onClose();
    } catch (e) {
      console.error('Ошибка!', e);
    }
  };

  const handleGeneralImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      try {
        await updateGeneralImage({ id: itemId, image: e.target.files[0] }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleDetailImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      try {
        await updateDetailImage({ id: itemId, image: e.target.files[0] }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleCreateSlide = async () => {
    if (!newSlideText && !newSlideImage) {
      alert('Введите текст или выберите фото для слайда');
      return;
    }

    const formData = new FormData();
    if (newSlideText) formData.append('text', newSlideText);
    if (newSlideImage) formData.append('image', newSlideImage);

    try {
      await addSlide({ id: itemId, formData }).unwrap();
      setNewSlideText('');
      setNewSlideImage(null);
    } catch (e) {
      console.error(e);
    }
  };

  const handleReorder = async (currentIndex: number, direction: 'up' | 'down') => {
    if (!item) return;
    const newSlides = [...item.how_it_was];
    const targetIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
    
    if (targetIndex < 0 || targetIndex >= newSlides.length) return;

    [newSlides[currentIndex], newSlides[targetIndex]] = [newSlides[targetIndex], newSlides[currentIndex]];
    
    try {
      await reorderSlides({ id: itemId, slideIds: newSlides.map(s => s.id) }).unwrap();
    } catch (e) {
      console.error(e);
    }
  };

  const handleGalleryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const formData = new FormData();
      Array.from(e.target.files).forEach(file => {
        formData.append('images', file);
      });
      try {
        await addGallery({ id: itemId, formData }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  if (isFetching) return null;

  return (
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="lg">
      <DialogTitle sx={{ m: 0, p: 3, fontWeight: 800, fontSize: '22px', color: 'var(--secondary-color)' }}>
        Редактировать историю #{itemId}
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
        <div className={styles['adm-module-row']}>
          <div className={styles['adm-module-main']}>
            <form onSubmit={handleSubmit(onSubmit)} id="edit-history-form" className={styles['adm-form']}>
              <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`}>Основные данные</h4>
              
              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Заголовок</label>
                <input {...register('title')} className={styles['adm-input']} required />
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
                <input {...register('general_subtitle')} className={styles['adm-input']} />
              </div>

              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Подзаголовок (детальный)</label>
                <input {...register('detail_subtitle')} className={styles['adm-input']} />
              </div>

              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Описание</label>
                <textarea {...register('short_description')} className={`${styles['adm-input']} ${styles['adm-textarea']}`} rows={3} />
              </div>
              
              <FormControlLabel
                control={<Checkbox {...register('is_draft')} color="primary" />}
                label="Сохранить как черновик"
                sx={{ '& .MuiFormControlLabel-label': { fontSize: '14px', fontWeight: 600 } }}
              />

              <div className={`${styles['adm-grid-2']} ${styles['adm-mt-20']}`}>
                <div className={styles['adm-form-group']}>
                  <label className={styles['adm-label']}>Главное фото (На странице с лентой)</label>
                  {item?.general_main_image ? (
                    <div className={styles['adm-img-preview-container']}>
                      <img src={resolveBackendUrl(item.general_main_image)} className={styles['adm-img-full']} alt="" />
                    </div>
                  ) : (
                    <div className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${styles['adm-mb-20']}`}>
                      <PhotoIcon sx={{ fontSize: 24, color: '#ccc' }} />
                    </div>
                  )}
                  <Button component="label" variant="outlined" size="small" startIcon={<PhotoIcon />} fullWidth sx={{ borderRadius: '8px', textTransform: 'none' }}>
                    Изменить
                    <input type="file" onChange={handleGeneralImageUpload} hidden accept="image/*" />
                  </Button>
                </div>

                <div className={styles['adm-form-group']}>
                  <label className={styles['adm-label']}>Главное фото (На странице предприятия)</label>
                  {item?.detail_main_image ? (
                    <div className={styles['adm-img-preview-container']}>
                      <img src={resolveBackendUrl(item.detail_main_image)} className={styles['adm-img-full']} alt="" />
                    </div>
                  ) : (
                    <div className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${styles['adm-mb-20']}`}>
                      <PhotoIcon sx={{ fontSize: 24, color: '#ccc' }} />
                    </div>
                  )}
                  <Button component="label" variant="outlined" size="small" startIcon={<PhotoIcon />} fullWidth sx={{ borderRadius: '8px', textTransform: 'none' }}>
                    Изменить
                    <input type="file" onChange={handleDetailImageUpload} hidden accept="image/*" />
                  </Button>
                </div>
              </div>
            </form>
          </div>

          <div className={styles['adm-sidebar-section']}>
            <div className={styles['adm-form-group']}>
              <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`}>Слайды ("Как это было")</h4>
              
              <div className={styles['adm-temp-slide']}>
                <TextField
                  multiline
                  rows={5}
                  fullWidth
                  placeholder="Текст слайда..."
                  value={newSlideText}
                  onChange={(e) => setNewSlideText(e.target.value)}
                  sx={{ mb: 2, bgcolor: '#fff' }}
                  size="small"
                />
                <Box sx={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                  <Button 
                    component="label" 
                    variant="outlined" 
                    size="small" 
                    startIcon={<PhotoIcon />}
                    sx={{ flex: 1, textTransform: 'none', borderRadius: '8px', bgcolor: newSlideImage ? 'var(--accent-color-2)' : '#fff' }}
                  >
                    {newSlideImage ? 'Фото выбрано' : 'Добавить фото'}
                    <input type="file" hidden accept="image/*" onChange={(e) => setNewSlideImage(e.target.files?.[0] || null)} />
                  </Button>
                  <Button 
                    variant="contained" 
                    size="small" 
                    disabled={isAddingSlide || (!newSlideText && !newSlideImage)}
                    onClick={handleCreateSlide}
                    sx={{ borderRadius: '8px', textTransform: 'none', px: 3 }}
                  >
                    {isAddingSlide ? <CircularProgress size={20} color="inherit" /> : 'Добавить'}
                  </Button>
                </Box>
              </div>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: '10px', my: 2, maxHeight: '400px', overflowY: 'auto', p: 0.5 }}>
                {item?.how_it_was.map((slide, index) => (
                  <div key={slide.id} className={styles['adm-slide-item']}>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <IconButton size="small" disabled={index === 0} onClick={() => handleReorder(index, 'up')}>
                        <UpIcon sx={{ fontSize: 16 }} />
                      </IconButton>
                      <IconButton size="small" disabled={index === (item?.how_it_was.length || 0) - 1} onClick={() => handleReorder(index, 'down')}>
                        <DownIcon sx={{ fontSize: 16 }} />
                      </IconButton>
                    </Box>
                    {slide.image && (
                      <img src={resolveBackendUrl(slide.image)} className={styles['adm-slide-thumb']} alt="" />
                    )}
                    <Typography className={styles['adm-slide-text']}>
                      {slide.text || <em style={{ color: '#999' }}>Только фото</em>}
                    </Typography>
                    <IconButton size="small" color="error" onClick={() => { if(confirm('Удалить слайд?')) deleteSlide({ historyId: itemId, slideId: slide.id }); }}>
                      <CloseIcon fontSize="small" />
                    </IconButton>
                  </div>
                ))}
              </Box>
            </div>

            <div className={styles['adm-form-group']}>
              <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`}>Галерея</h4>
              <div className={styles['adm-gallery-flex']}>
                {item?.gallery.map((img) => (
                  <div key={img.id} className={styles['adm-gallery-item']}>
                    <img src={resolveBackendUrl(img.image)} className={styles['adm-gallery-img']} alt="" />
                    <IconButton 
                      size="small"
                      onClick={() => deleteGallery({ historyId: itemId, imageId: img.id })}
                      sx={{ position: 'absolute', top: 2, right: 2, bgcolor: 'rgba(255,255,255,0.8)', p: '2px', color: 'var(--error-color)' }}
                    >
                      <CloseIcon sx={{ fontSize: '14px' }} />
                    </IconButton>
                  </div>
                ))}
              </div>
              <Button component="label" variant="outlined" size="small" startIcon={<AddIcon />} fullWidth sx={{ borderRadius: '8px', textTransform: 'none', borderStyle: 'dashed' }}>
                Фото в галерею
                <input type="file" multiple onChange={handleGalleryUpload} hidden accept="image/*" />
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 2 }}>
        <Button onClick={onClose} sx={{ color: '#666', fontWeight: 600 }}>
          Отмена
        </Button>
        <Button 
          type="submit" 
          form="edit-history-form" 
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
