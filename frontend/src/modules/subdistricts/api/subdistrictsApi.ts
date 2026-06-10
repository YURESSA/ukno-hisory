import { baseApi } from '@/api/baseApi';
import { Subdistrict, SubdistrictDetail, SubdistrictUpdateFormData } from '../types';

export const subdistrictsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getSubdistricts: builder.query<Subdistrict[], void>({
      query: () => '/subdistricts',
      providesTags: ['Subdistricts'],
    }),
    getSubdistrictDetail: builder.query<SubdistrictDetail, string>({
      query: (name) => `/subdistricts/${name}`,
      providesTags: (_result, _error, name) => [{ type: 'Subdistricts', id: name }],
    }),
    updateSubdistrict: builder.mutation<SubdistrictDetail, { name: string; data: SubdistrictUpdateFormData }>({
      query: ({ name, data }) => ({
        url: `/subdistricts/${name}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: (_result, _error, { name }) => ['Subdistricts', { type: 'Subdistricts', id: name }],
    }),
    updateSubdistrictImage: builder.mutation<SubdistrictDetail, { name: string; image: File }>({
      query: ({ name, image }) => {
        const formData = new FormData();
        formData.append('image', image);
        return {
          url: `/subdistricts/${name}/image`,
          method: 'PUT',
          body: formData,
        };
      },
      invalidatesTags: (_result, _error, { name }) => ['Subdistricts', { type: 'Subdistricts', id: name }],
    }),
    deleteSubdistrictImage: builder.mutation<SubdistrictDetail, string>({
      query: (name) => ({
        url: `/subdistricts/${name}/image`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, name) => ['Subdistricts', { type: 'Subdistricts', id: name }],
    }),
  }),
});

export const {
  useGetSubdistrictsQuery,
  useGetSubdistrictDetailQuery,
  useUpdateSubdistrictMutation,
  useUpdateSubdistrictImageMutation,
  useDeleteSubdistrictImageMutation,
} = subdistrictsApi;
