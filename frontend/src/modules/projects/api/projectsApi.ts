import { baseApi } from '@/api/baseApi';
import { StudentProject, AdminProjectListItem, ProjectDetail } from '../types';

export interface PublicProjectListItem {
  id: number;
  title: string;
  author: string | null;
  short_description: string | null;
  main_image: string | null;
}

export const projectsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getPublicProjects: builder.query<PublicProjectListItem[], void>({
      query: () => '/student-projects',
      providesTags: ['Projects'],
    }),

    getPublicProject: builder.query<ProjectDetail, number>({
      query: (id) => `/student-projects/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'Projects', id }],
    }),

    getAdminProjects: builder.query<AdminProjectListItem[], void>({
      query: () => '/student-projects/admin',
      providesTags: ['Projects'],
    }),

    getAdminProject: builder.query<StudentProject, number>({
      query: (id) => `/student-projects/admin/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'Projects', id }],
    }),

    createProject: builder.mutation<StudentProject, FormData>({
      query: (formData) => ({
        url: '/student-projects',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Projects'],
    }),

    updateProject: builder.mutation<StudentProject, { id: number; data: Partial<StudentProject> }>({
      query: ({ id, data }) => ({
        url: `/student-projects/${id}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: (_result, _error, { id }) => ['Projects', { type: 'Projects', id }],
    }),

    deleteProject: builder.mutation<string, number>({
      query: (id) => ({
        url: `/student-projects/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Projects'],
    }),

    addGalleryImages: builder.mutation<StudentProject, { id: number; formData: FormData }>({
      query: ({ id, formData }) => ({
        url: `/student-projects/${id}/gallery`,
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'Projects', id }],
    }),

    deleteGalleryImage: builder.mutation<StudentProject, { projectId: number; imageId: number }>({
      query: ({ projectId, imageId }) => ({
        url: `/student-projects/${projectId}/gallery/${imageId}`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, { projectId }) => [{ type: 'Projects', projectId }],
    }),

    updateProjectMainImage: builder.mutation<StudentProject, { id: number; image: File }>({
      query: ({ id, image }) => {
        const formData = new FormData();
        formData.append('main_image', image);
        return {
          url: `/student-projects/${id}/main-image`,
          method: 'PUT',
          body: formData,
        };
      },
      invalidatesTags: (_result, _error, { id }) => [{ type: 'Projects', id }],
    }),

    deleteProjectMainImage: builder.mutation<StudentProject, number>({
      query: (id) => ({
        url: `/student-projects/${id}/main-image`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, id) => [{ type: 'Projects', id }],
    }),

    reorderProjectGallery: builder.mutation<StudentProject, { id: number; imageIds: number[] }>({
      query: ({ id, imageIds }) => ({
        url: `/student-projects/${id}/gallery/order`,
        method: 'PUT',
        body: { image_ids: imageIds },
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'Projects', id }],
    }),
  }),
});

export const {
  useGetPublicProjectsQuery,
  useGetPublicProjectQuery,
  useGetAdminProjectsQuery,
  useGetAdminProjectQuery,
  useCreateProjectMutation,
  useUpdateProjectMutation,
  useDeleteProjectMutation,
  useAddGalleryImagesMutation,
  useDeleteGalleryImageMutation,
  useUpdateProjectMainImageMutation,
  useDeleteProjectMainImageMutation,
  useReorderProjectGalleryMutation,
} = projectsApi;