import { baseApi } from '@/api/baseApi';
import { StudentProject, AdminProjectListItem } from '../types';

export const projectsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Получить все проекты для админа 
    getAdminProjects: builder.query<AdminProjectListItem[], void>({
      query: () => '/student-projects/admin',
      providesTags: ['Projects'],
    }),

    // Создать проект 
    // Используем FormData, так как бэк ждет multipart/form-data
    createProject: builder.mutation<StudentProject, FormData>({
      query: (formData) => ({
        url: '/student-projects',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Projects'],
    }),

    // Обновить данные проекта [cite: 10]
    updateProject: builder.mutation<StudentProject, { id: number; data: Partial<StudentProject> }>({
      query: ({ id, data }) => ({
        url: `/student-projects/${id}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: ['Projects'],
    }),

    // Удалить проект 
    deleteProject: builder.mutation<string, number>({
      query: (id) => ({
        url: `/student-projects/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Projects'],
    }),
  }),
});

export const {
  useGetAdminProjectsQuery,
  useCreateProjectMutation,
  useUpdateProjectMutation,
  useDeleteProjectMutation,
} = projectsApi;