import { useForm, useFieldArray } from 'react-hook-form';
import { useEffect } from 'react';
import { 
  useGetQuizQuestionQuery, 
  useUpdateQuizQuestionMutation,
  useUpdateQuizQuestionImageMutation,
  useDeleteQuizQuestionImageMutation
} from '../../api/quizApi';
import { resolveBackendUrl } from '@/config/env';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  IconButton,
  Button,
  CircularProgress,
  Checkbox,
  Tooltip,
  Typography,
} from '@mui/material';
import { 
  Close as CloseIcon, 
  PhotoCamera as PhotoIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  CheckCircle as CorrectIcon
} from '@mui/icons-material';
import styles from '@/styles/admin.module.css';

import { QuizOption } from '../../types';

interface Props {
  questionId: number;
  isOpen: boolean;
  onClose: () => void;
}

interface EditFormData {
  question: string;
  explanation: string;
  options: QuizOption[];
}

export const EditQuizQuestionModal = ({ questionId, isOpen, onClose }: Props) => {
  const { data: question, isLoading: isFetching } = useGetQuizQuestionQuery(questionId, { skip: !isOpen });
  const [updateQuestion, { isLoading: isUpdating }] = useUpdateQuizQuestionMutation();
  const [updateImage] = useUpdateQuizQuestionImageMutation();
  const [deleteImage] = useDeleteQuizQuestionImageMutation();

  const { register, control, handleSubmit, reset } = useForm<EditFormData>();

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'options'
  });

  useEffect(() => {
    if (question) {
      reset({
        question: question.question,
        explanation: question.explanation || '',
        options: question.options.map(opt => ({ text: opt.text, is_correct: opt.is_correct }))
      });
    }
  }, [question, reset]);

  const onSubmit = async (data: EditFormData) => {
    try {
      await updateQuestion({ id: questionId, data }).unwrap();
      alert('Вопрос обновлен!');
      onClose();
    } catch (e) {
      console.error(e);
      alert('Ошибка при обновлении');
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      try {
        await updateImage({ id: questionId, image: e.target.files[0] }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  if (isFetching) return null;

  return (
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle sx={{ m: 0, p: 3, fontWeight: 800, fontSize: '22px', color: 'var(--secondary-color)' }}>
        Редактирование вопроса #{questionId}
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
        <form onSubmit={handleSubmit(onSubmit)} id="edit-quiz-form" className={styles['adm-form']}>
          <div className={styles['adm-module-row-2-1']}>
            <div className={styles['adm-flex-main']}>
              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Текст вопроса</label>
                <input {...register('question')} className={styles['adm-input']} required />
              </div>

              <div className={styles['adm-form-group']}>
                <label className={styles['adm-label']}>Объяснение</label>
                <textarea {...register('explanation')} className={`${styles['adm-input']} ${styles['adm-textarea']}`} rows={3} />
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
            </div>

            <div className={styles['adm-flex-sidebar']}>
              <h4 className={`${styles['adm-label']} ${styles['adm-form-divider']}`}>
                Изображение вопроса
              </h4>
              
              {question?.image ? (
                <div className={styles['adm-img-preview-43']}>
                  <img src={resolveBackendUrl(question.image)} className={styles['adm-img-full']} alt="" />
                  <IconButton 
                    size="small"
                    onClick={() => { if(confirm('Удалить фото?')) deleteImage(questionId); }}
                    sx={{ position: 'absolute', top: 8, right: 8, bgcolor: 'rgba(255,255,255,0.9)', color: 'var(--error-color)', '&:hover': { bgcolor: 'var(--error-color)', color: '#fff' } }}
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </div>
              ) : (
                <div className={`${styles['adm-file-upload']} ${styles['adm-mb-15']}`}>
                  <PhotoIcon sx={{ fontSize: 32, color: '#ccc' }} />
                  <Typography variant="caption" sx={{ display: 'block', mt: 1, color: '#999' }}>Нет фото</Typography>
                </div>
              )}
              
              <Button
                component="label"
                variant="outlined"
                size="small"
                startIcon={<PhotoIcon />}
                fullWidth
                sx={{ borderRadius: '8px', textTransform: 'none' }}
              >
                {question?.image ? 'Заменить фото' : 'Загрузить фото'}
                <input type="file" onChange={handleImageUpload} hidden accept="image/*" />
              </Button>
            </div>
          </div>
        </form>
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 2 }}>
        <Button onClick={onClose} sx={{ color: '#666', fontWeight: 600 }}>
          Отмена
        </Button>
        <Button 
          type="submit" 
          form="edit-quiz-form" 
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
