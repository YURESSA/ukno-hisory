import { useForm } from 'react-hook-form';
import { Button, CircularProgress, FormControlLabel, Checkbox } from '@mui/material';
import { CloudUpload as UploadIcon } from '@mui/icons-material';
import { useCreateEnterpriseHistoryMutation } from '../../api/enterpriseHistoryApi';

import { CreateEnterpriseHistoryFormData } from '../../types';

export const CreateEnterpriseHistoryForm = () => {
  const { register, handleSubmit, reset } = useForm<CreateEnterpriseHistoryFormData>();
  const [createHistory, { isLoading }] = useCreateEnterpriseHistoryMutation();

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

    try {
      await createHistory(formData).unwrap();
      alert('Запись создана!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <div className="adm-card">
      <h3 className="adm-title">Создать историю предприятия</h3>
      <form onSubmit={handleSubmit(onSubmit)} className="adm-form">
        <div className="adm-form-group">
          <label className="adm-label">Заголовок</label>
          <input {...register('title')} className="adm-input" placeholder="Название предприятия" required />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Подзаголовок (общий)</label>
          <input {...register('general_subtitle')} className="adm-input" placeholder="Краткий слоган" />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Подзаголовок (детальный)</label>
          <input {...register('detail_subtitle')} className="adm-input" placeholder="Более подробный подзаголовок" />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Краткое описание</label>
          <textarea {...register('short_description')} className="adm-input adm-textarea" placeholder="Описание для ленты..." rows={3} />
        </div>
        
        <div className="adm-form-group">
          <FormControlLabel
            control={<Checkbox {...register('is_draft')} color="primary" defaultChecked />}
            label="Сохранить как черновик"
            sx={{ '& .MuiFormControlLabel-label': { fontSize: '0.9rem', fontWeight: 500 } }}
          />
        </div>

        <div className="adm-module-row" style={{ gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="adm-form-group">
            <label className="adm-label">Общее фото (для списка)</label>
            <div className="adm-file-upload" style={{ padding: '20px' }} onClick={() => document.getElementById('gen-img')?.click()}>
              <UploadIcon sx={{ fontSize: 24, color: '#ccc' }} />
              <input id="gen-img" type="file" {...register('general_main_image')} accept="image/*" style={{ display: 'none' }} />
            </div>
          </div>

          <div className="adm-form-group">
            <label className="adm-label">Детальное фото (страница)</label>
            <div className="adm-file-upload" style={{ padding: '20px' }} onClick={() => document.getElementById('det-img')?.click()}>
              <UploadIcon sx={{ fontSize: 24, color: '#ccc' }} />
              <input id="det-img" type="file" {...register('detail_main_image')} accept="image/*" style={{ display: 'none' }} />
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
