import { useForm } from 'react-hook-form';
import { Button, CircularProgress, FormControlLabel, Checkbox } from '@mui/material';
import { CloudUpload as UploadIcon } from '@mui/icons-material';
import { useCreateProjectMutation } from '../../api/projectsApi';

import { CreateProjectFormData } from '../../types';

export const CreateProjectForm = () => {
  const { register, handleSubmit, reset } = useForm<CreateProjectFormData>();
  const [createProject, { isLoading }] = useCreateProjectMutation();

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

    try {
      await createProject(formData).unwrap();
      alert('Проект создан!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <div className="adm-card">
      <h3 className="adm-title">Создать проект</h3>
      <form onSubmit={handleSubmit(onSubmit)} className="adm-form">
        <div className="adm-form-group">
          <label className="adm-label">Название проекта</label>
          <input {...register('title')} placeholder="Название" className="adm-input" required />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Автор</label>
          <input {...register('author')} placeholder="Имя студента" className="adm-input" />
        </div>

        <div className="adm-module-row" style={{ gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' }}>
          <div className="adm-form-group">
            <label className="adm-label">Год</label>
            <input type="number" {...register('year')} placeholder="2024" className="adm-input" />
          </div>
          <div className="adm-form-group">
            <label className="adm-label">Тег 1</label>
            <input {...register('tag_one')} placeholder="Web" className="adm-input" />
          </div>
          <div className="adm-form-group">
            <label className="adm-label">Тег 2</label>
            <input {...register('tag_two')} placeholder="React" className="adm-input" />
          </div>
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Краткое описание</label>
          <textarea {...register('short_description')} placeholder="Для карточки проекта..." className="adm-input adm-textarea" />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Полное описание</label>
          <textarea {...register('description')} placeholder="Детальное описание проекта..." rows={4} className="adm-input adm-textarea" />
        </div>
        
        <div className="adm-form-group">
          <FormControlLabel
            control={<Checkbox {...register('is_draft')} color="primary" />}
            label="Сохранить как черновик"
            sx={{ '& .MuiFormControlLabel-label': { fontSize: '0.9rem', fontWeight: 500 } }}
          />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Главное изображение</label>
          <div className="adm-file-upload" onClick={() => document.getElementById('file-input')?.click()}>
            <UploadIcon sx={{ fontSize: 32, color: '#ccc', mb: 1 }} />
            <p style={{ margin: 0, fontSize: '0.9rem', color: '#666' }}>Нажмите или перетащите файл</p>
            <input 
              id="file-input"
              type="file" 
              {...register('main_image')} 
              accept="image/*" 
              style={{ display: 'none' }} 
            />
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
            boxShadow: 'none'
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Создать проект'}
        </Button>
      </form>
    </div>
  );
};
