import { useForm } from 'react-hook-form';
import { Button, CircularProgress } from '@mui/material';
import { CloudUpload as UploadIcon } from '@mui/icons-material';
import { useCreateTimelineMutation } from '../../api/timelineApi';

import { CreateTimelineFormData } from '../../types';

export const CreateTimelineForm = () => {
  const { register, handleSubmit, reset } = useForm<CreateTimelineFormData>();
  const [createTimeline, { isLoading }] = useCreateTimelineMutation();

  const onSubmit = async (data: CreateTimelineFormData) => {
    const formData = new FormData();
    formData.append('year', data.year);
    formData.append('text', data.text);
    
    if (data.image?.[0]) {
      formData.append('image', data.image[0]);
    }

    try {
      await createTimeline(formData).unwrap();
      alert('Событие добавлено в таймлайн!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <div className="adm-card">
      <h3 className="adm-title">Добавить событие</h3>
      <form onSubmit={handleSubmit(onSubmit)} className="adm-form">
        <div className="adm-form-group">
          <label className="adm-label">Год</label>
          <input type="number" {...register('year')} className="adm-input" placeholder="Например: 1950" required />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Описание события</label>
          <textarea {...register('text')} className="adm-input adm-textarea" placeholder="Опишите что произошло..." rows={3} required />
        </div>
        
        <div className="adm-form-group">
          <label className="adm-label">Изображение</label>
          <div className="adm-file-upload" onClick={() => document.getElementById('timeline-file')?.click()}>
            <UploadIcon sx={{ fontSize: 32, color: '#ccc', mb: 1 }} />
            <p style={{ margin: 0, fontSize: '0.85rem', color: '#666' }}>Выберите фото события</p>
            <input 
              id="timeline-file"
              type="file" 
              {...register('image')} 
              className="adm-input" 
              accept="image/*" 
              required 
              style={{ display: 'none' }}
            />
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
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Добавить в таймлайн'}
        </Button>
      </form>
    </div>
  );
};
