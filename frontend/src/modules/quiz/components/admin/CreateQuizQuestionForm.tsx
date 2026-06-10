import { useForm, useFieldArray, useWatch } from 'react-hook-form';
import { Button, CircularProgress, Checkbox, IconButton, Tooltip, Typography } from '@mui/material';
import { 
  CloudUpload as UploadIcon, 
  Add as AddIcon, 
  Delete as DeleteIcon,
  CheckCircle as CorrectIcon
} from '@mui/icons-material';
import { useCreateQuizQuestionMutation } from '../../api/quizApi';
import styles from '@/styles/admin.module.css';

import { CreateQuizQuestionFormData } from '../../types';

export const CreateQuizQuestionForm = () => {
  const { register, control, handleSubmit, reset } = useForm<CreateQuizQuestionFormData>({
    defaultValues: {
      question: '',
      explanation: '',
      image: null,
      options: [
        { text: '', is_correct: false },
        { text: '', is_correct: false }
      ]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'options'
  });

  const [createQuestion, { isLoading }] = useCreateQuizQuestionMutation();

  const selectedImage = useWatch({ control, name: 'image' });

  const onSubmit = async (data: CreateQuizQuestionFormData) => {
    try {
      const formData = new FormData();
      formData.append('question', data.question);
      if (data.explanation) formData.append('explanation', data.explanation);
      
      formData.append('options', JSON.stringify(data.options));
      
      if (data.image && data.image[0]) {
        formData.append('image', data.image[0]);
      }

      await createQuestion(formData).unwrap();
      reset();
      alert('Вопрос создан!');
    } catch (err) {
      console.error('Ошибка создания вопроса:', err);
      alert('Ошибка при создании вопроса');
    }
  };

  return (
    <div className={styles['adm-card']}>
      <h3 className={styles['adm-title']}>Создать вопрос квиза</h3>
      <form onSubmit={handleSubmit(onSubmit)} className={styles['adm-form']}>
        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Текст вопроса</label>
          <input {...register('question')} placeholder="Например: Какого цвета небо?" className={styles['adm-input']} required />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Объяснение (показывается после ответа)</label>
          <textarea {...register('explanation')} placeholder="Необязательно..." className={`${styles['adm-input']} ${styles['adm-textarea']}`} rows={2} />
        </div>

        <div className={styles['adm-form-group']}>
          <label className={styles['adm-label']}>Изображение вопроса</label>
          <div 
            className={`${styles['adm-file-upload']} ${styles['adm-file-upload-compact']} ${selectedImage?.[0] ? styles['adm-file-upload-active'] : ''}`}
            onClick={() => document.getElementById('quiz-img')?.click()}
          >
            <UploadIcon sx={{ fontSize: 24, color: selectedImage?.[0] ? 'var(--primary-color)' : '#ccc' }} />
            <p className={styles['adm-file-upload-text']}>
              {selectedImage?.[0] ? `Выбрано: ${selectedImage[0].name}` : 'Нажмите для выбора фото'}
            </p>
            <input id="quiz-img" {...register('image')} type="file" accept="image/*" style={{ display: 'none' }} />
          </div>
        </div>

        <div className={styles['adm-options-editor']}>
          <Typography className={styles['adm-options-title']}>Варианты ответа:</Typography>
          {fields.map((field, index) => (
            <div key={field.id} className={`${styles['adm-quiz-option-row']} ${styles['adm-quiz-option-edit']}`}>
              <input 
                {...register(`options.${index}.text` as const)} 
                placeholder={`Вариант ${index + 1}`} 
                required 
                className={`${styles['adm-input']} ${styles['adm-input-ghost']}`}
              />
              <Tooltip title="Отметить как правильный">
                <Checkbox 
                  {...register(`options.${index}.is_correct` as const)} 
                  checkedIcon={<CorrectIcon />}
                  color="success"
                />
              </Tooltip>
              <IconButton size="small" onClick={() => remove(index)} color="error">
                <DeleteIcon fontSize="small" />
              </IconButton>
            </div>
          ))}
          <Button 
            type="button" 
            variant="outlined"
            onClick={() => append({ text: '', is_correct: false })}
            startIcon={<AddIcon />}
            size="small"
            sx={{ mt: 1, borderRadius: '8px', textTransform: 'none' }}
          >
            Добавить вариант
          </Button>
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
            mt: 2
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Создать вопрос'}
        </Button>
      </form>
    </div>
  );
};
