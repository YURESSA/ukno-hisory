import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { useGetAdminProjectQuery, useUpdateProjectMutation, useAddGalleryImagesMutation, useDeleteGalleryImageMutation } from '../api/projectsApi';
import { Modal } from '@/app/components/Modal';
import { resolveBackendUrl } from '@/config/env';

interface Props {
  projectId: number;
  isOpen: boolean;
  onClose: () => void;
}

export const EditProjectModal = ({ projectId, isOpen, onClose }: Props) => {
  const { data: project, isLoading: isFetching } = useGetAdminProjectQuery(projectId, { skip: !isOpen });
  const [updateProject, { isLoading: isUpdating }] = useUpdateProjectMutation();
  const [addGalleryImages] = useAddGalleryImagesMutation();
  const [deleteGalleryImage] = useDeleteGalleryImageMutation();

  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    if (project) {
      reset({
        title: project.title,
        author: project.author,
        short_description: project.short_description,
        description: project.description,
        year: project.year,
        tag_one: project.tag_one,
        tag_two: project.tag_two,
        is_draft: project.is_draft,
      });
    }
  }, [project, reset]);

  const onSubmit = async (data: any) => {
    try {
      await updateProject({ id: projectId, data }).unwrap();
      alert('Проект обновлен!');
    } catch (e) {
      console.error(e);
      alert('Ошибка при обновлении');
    }
  };

  const handleGalleryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const formData = new FormData();
      Array.from(e.target.files).forEach(file => {
        formData.append('images', file);
      });
      try {
        await addGalleryImages({ id: projectId, formData }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  if (isFetching) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Редактировать проект #${projectId}`}>
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <h3>Основные данные</h3>
          <input {...register('title')} placeholder="Название проекта" required style={inputStyle} />
          <input {...register('author')} placeholder="Автор" style={inputStyle} />
          <input type="number" {...register('year')} placeholder="Год" style={inputStyle} />
          <input {...register('tag_one')} placeholder="Тег 1" style={inputStyle} />
          <input {...register('tag_two')} placeholder="Тег 2" style={inputStyle} />
          <textarea {...register('short_description')} placeholder="Краткое описание" style={{ ...inputStyle, height: '80px' }} />
          <textarea {...register('description')} placeholder="Полное описание" style={{ ...inputStyle, height: '150px' }} />
          
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
            <input type="checkbox" {...register('is_draft')} /> 
            <span>Черновик (не показывать на сайте)</span>
          </label>

          <button type="submit" disabled={isUpdating} style={saveButtonStyle}>
            {isUpdating ? 'Сохранение...' : 'Сохранить изменения'}
          </button>
        </div>

        <div>
          <h3>Галерея</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: '10px', marginBottom: '15px' }}>
            {project?.gallery.map((img) => (
              <div key={img.id} style={{ position: 'relative', border: '1px solid #ddd', borderRadius: '4px', overflow: 'hidden' }}>
                <img 
                  src={resolveBackendUrl(img.image)} 
                  alt="" 
                  style={{ width: '100%', height: '100px', objectFit: 'cover' }} 
                />
                <button 
                  type="button"
                  onClick={() => deleteGalleryImage({ projectId, imageId: img.id })}
                  style={deleteImgButtonStyle}
                >&times;</button>
              </div>
            ))}
          </div>
          <label style={uploadButtonStyle}>
            + Добавить фото в галерею
            <input type="file" multiple onChange={handleGalleryUpload} style={{ display: 'none' }} accept="image/*" />
          </label>
        </div>
      </form>
    </Modal>
  );
};

const inputStyle = {
  padding: '10px',
  border: '1px solid #d9d9d9',
  borderRadius: '4px',
  fontSize: '14px',
};

const saveButtonStyle = {
  backgroundColor: '#1890ff',
  color: 'white',
  border: 'none',
  padding: '12px',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '16px',
  marginTop: '10px',
};

const uploadButtonStyle = {
  display: 'block',
  padding: '10px',
  border: '2px dashed #1890ff',
  color: '#1890ff',
  textAlign: 'center' as const,
  borderRadius: '4px',
  cursor: 'pointer',
};

const deleteImgButtonStyle = {
  position: 'absolute' as const,
  top: '2px',
  right: '2px',
  background: 'rgba(255,0,0,0.7)',
  color: 'white',
  border: 'none',
  borderRadius: '50%',
  width: '20px',
  height: '20px',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};
