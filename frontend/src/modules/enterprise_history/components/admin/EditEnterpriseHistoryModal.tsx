import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { 
  useGetAdminEnterpriseHistoryQuery, 
  useUpdateEnterpriseHistoryMutation, 
  useAddHistorySlideMutation, 
  useDeleteHistorySlideMutation,
  useAddHistoryGalleryImagesMutation,
  useDeleteHistoryGalleryImageMutation
} from '../../api/enterpriseHistoryApi';
import { resolveBackendUrl } from '@/config/env';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  IconButton,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

interface Props {
  itemId: number;
  isOpen: boolean;
  onClose: () => void;
}

import { UpdateEnterpriseHistoryFormData } from '../../types';

export const EditEnterpriseHistoryModal = ({ itemId, isOpen, onClose }: Props) => {
  const { data: item, isLoading: isFetching } = useGetAdminEnterpriseHistoryQuery(itemId, { skip: !isOpen });
  const [updateItem, { isLoading: isUpdating }] = useUpdateEnterpriseHistoryMutation();
  const [addSlide] = useAddHistorySlideMutation();
  const [deleteSlide] = useDeleteHistorySlideMutation();
  const [addGallery] = useAddHistoryGalleryImagesMutation();
  const [deleteGallery] = useDeleteHistoryGalleryImageMutation();

  const { register, handleSubmit, reset } = useForm<UpdateEnterpriseHistoryFormData>();

  useEffect(() => {
    if (item) {
      reset({
        title: item.title || '',
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
      console.error(e);
      alert('Ошибка обновления');
    }
  };

  const handleAddSlide = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const formData = new FormData();
      formData.append('image', e.target.files[0]);
      formData.append('text', 'Новый слайд');
      try {
        await addSlide({ id: itemId, formData }).unwrap();
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
        await addGallery({ id: itemId, formData }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  if (isFetching) return null;

  return (
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="lg">
      <DialogTitle sx={{ m: 0, p: 2, fontWeight: 700 }}>
        Редактировать историю #{itemId}
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      
      <DialogContent dividers>
        <div className="adm-module-row">
          <div className="adm-module-main">
            <form onSubmit={handleSubmit(onSubmit)} id="edit-history-form" className="adm-form">
              <h4 className="adm-label" style={{ color: 'var(--primary-color)', margin: 0 }}>Основные данные</h4>
              
              <div className="adm-form-group">
                <label className="adm-label">Заголовок</label>
                <input {...register('title')} className="input-base" required />
              </div>

              <div className="adm-form-group">
                <label className="adm-label">Подзаголовок (общий)</label>
                <input {...register('general_subtitle')} className="input-base" />
              </div>

              <div className="adm-form-group">
                <label className="adm-label">Подзаголовок (детальный)</label>
                <input {...register('detail_subtitle')} className="input-base" />
              </div>

              <div className="adm-form-group">
                <label className="adm-label">Краткое описание</label>
                <textarea {...register('short_description')} className="input-base" rows={3} />
              </div>
              
              <FormControlLabel
                control={<Checkbox {...register('is_draft')} color="primary" defaultChecked />}
                label="Сохранить как черновик"
                sx={{ '& .MuiFormControlLabel-label': { fontSize: '0.9rem', fontWeight: 500 } }}
              />
            </form>
          </div>

          <div className="adm-module-sidebar" style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
            <div className="adm-form-group">
              <h4 className="adm-label" style={{ color: 'var(--primary-color)', marginBottom: '10px' }}>Слайды ("Как это было")</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '15px', maxHeight: '200px', overflowY: 'auto', padding: '4px' }}>
                {item?.how_it_was.map((slide) => (
                  <div key={slide.id} style={{ 
                    display: 'flex', 
                    gap: '12px', 
                    alignItems: 'center', 
                    border: '1px solid var(--accent-color-1)', 
                    padding: '8px',
                    borderRadius: '8px',
                    backgroundColor: '#fafafa'
                  }}>
                    {slide.image && (
                      <img src={resolveBackendUrl(slide.image)} style={{ width: '40px', height: '40px', objectFit: 'cover', borderRadius: '4px' }} alt="" />
                    )}
                    <span style={{ flex: 1, fontSize: '12px', fontWeight: 500 }}>{slide.text || 'Без текста'}</span>
                    <IconButton size="small" color="error" onClick={() => deleteSlide({ historyId: itemId, slideId: slide.id })}>
                      <CloseIcon fontSize="small" />
                    </IconButton>
                  </div>
                ))}
              </div>
              <label style={{ 
                display: 'block', 
                padding: '12px', 
                border: '1px dashed var(--primary-color)', 
                color: 'var(--primary-color)',
                textAlign: 'center',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '13px',
                backgroundColor: 'var(--accent-color-2)'
              }}>
                + Добавить слайд
                <input type="file" onChange={handleAddSlide} style={{ display: 'none' }} accept="image/*" />
              </label>
            </div>

            <div className="adm-form-group">
              <h4 className="adm-label" style={{ color: 'var(--primary-color)', marginBottom: '10px' }}>Галерея</h4>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fill, minmax(70px, 1fr))', 
                gap: '12px',
                marginBottom: '15px',
                maxHeight: '150px',
                overflowY: 'auto',
                padding: '4px'
              }}>
                {item?.gallery.map((img) => (
                  <div key={img.id} style={{ position: 'relative', aspectRatio: '1/1', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--accent-color-1)' }}>
                    <img src={resolveBackendUrl(img.image)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} alt="" />
                    <IconButton 
                      size="small"
                      onClick={() => deleteGallery({ historyId: itemId, imageId: img.id })}
                      sx={{ position: 'absolute', top: 2, right: 2, bgcolor: 'rgba(255,255,255,0.7)', p: '2px' }}
                    >
                      <CloseIcon sx={{ fontSize: '12px' }} />
                    </IconButton>
                  </div>
                ))}
              </div>
              <label style={{ 
                display: 'block', 
                padding: '12px', 
                border: '1px dashed var(--primary-color)', 
                color: 'var(--primary-color)',
                textAlign: 'center',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '13px',
                backgroundColor: 'var(--accent-color-2)'
              }}>
                + Фото в галерею
                <input type="file" multiple onChange={handleGalleryUpload} style={{ display: 'none' }} accept="image/*" />
              </label>
            </div>
          </div>
        </div>
      </DialogContent>

      <DialogActions sx={{ p: 2.5 }}>
        <button onClick={onClose} className="btn-outline">
          Отмена
        </button>
        <button 
          type="submit" 
          form="edit-history-form" 
          disabled={isUpdating} 
          className="btn-primary"
        >
          {isUpdating ? 'Сохранение...' : 'Сохранить изменения'}
        </button>
      </DialogActions>
    </Dialog>
  );
};
