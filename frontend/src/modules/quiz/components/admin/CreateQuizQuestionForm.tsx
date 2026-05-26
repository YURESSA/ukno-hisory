import { useForm, useFieldArray } from 'react-hook-form';
import { Button, CircularProgress, Checkbox, IconButton, Tooltip } from '@mui/material';
import { 
  CloudUpload as UploadIcon, 
  Add as AddIcon, 
  Delete as DeleteIcon,
  CheckCircle as CorrectIcon
} from '@mui/icons-material';
import { useCreateQuizQuestionMutation } from '../../api/quizApi';

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
    <div className="adm-card">
      <h3 className="adm-title">Создать вопрос квиза</h3>
      <form onSubmit={handleSubmit(onSubmit)} className="adm-form">
        <div className="adm-form-group">
          <label className="adm-label">Текст вопроса</label>
          <input {...register('question')} placeholder="Например: Какого цвета небо?" className="adm-input" required />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Объяснение (показывается после ответа)</label>
          <textarea {...register('explanation')} placeholder="Необязательно..." className="adm-input adm-textarea" rows={2} />
        </div>

        <div className="adm-form-group">
          <label className="adm-label">Изображение вопроса</label>
          <div className="adm-file-upload" style={{ padding: '20px' }} onClick={() => document.getElementById('quiz-img')?.click()}>
            <UploadIcon sx={{ fontSize: 24, color: '#ccc' }} />
            <input id="quiz-img" {...register('image')} type="file" accept="image/*" style={{ display: 'none' }} />
          </div>
        </div>

        <div className="adm-options-editor" style={{ background: '#fcfcfc', padding: '20px', borderRadius: '12px' }}>
          <h4 style={{ margin: '0 0 15px 0', fontSize: '0.95rem' }}>Варианты ответа:</h4>
          {fields.map((field, index) => (
            <div key={field.id} className="adm-quiz-option-row" style={{ border: '1px solid #e0e0e0' }}>
              <input 
                {...register(`options.${index}.text` as const)} 
                placeholder={`Вариант ${index + 1}`} 
                required 
                className="adm-input"
                style={{ border: 'none', background: 'transparent', padding: '5px' }}
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
