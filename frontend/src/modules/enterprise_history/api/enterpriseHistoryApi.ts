import { baseApi } from '@/api/baseApi';
import { EnterpriseHistoryAdminSummary, EnterpriseHistoryAdminDetail } from '../types';

export const enterpriseHistoryApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAdminEnterpriseHistories: builder.query<EnterpriseHistoryAdminSummary[], void>({
      query: () => '/enterprise-history/admin',
      providesTags: ['EnterpriseHistory'],
    }),

    getAdminEnterpriseHistory: builder.query<EnterpriseHistoryAdminDetail, number>({
      query: (id) => `/enterprise-history/admin/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'EnterpriseHistory', id }],
    }),

    createEnterpriseHistory: builder.mutation<EnterpriseHistoryAdminDetail, FormData>({
      query: (formData) => ({
        url: '/enterprise-history',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['EnterpriseHistory'],
    }),

    updateEnterpriseHistory: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; data: Partial<EnterpriseHistoryAdminDetail> }>({
      query: ({ id, data }) => ({
        url: `/enterprise-history/${id}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: (_result, _error, { id }) => ['EnterpriseHistory', { type: 'EnterpriseHistory', id }],
    }),

    deleteEnterpriseHistory: builder.mutation<void, number>({
      query: (id) => ({
        url: `/enterprise-history/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['EnterpriseHistory'],
    }),

    addHistorySlide: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; formData: FormData }>({
      query: ({ id, formData }) => ({
        url: `/enterprise-history/${id}/how-it-was`,
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'EnterpriseHistory', id }],
    }),

    deleteHistorySlide: builder.mutation<EnterpriseHistoryAdminDetail, { historyId: number; slideId: number }>({
      query: ({ historyId, slideId }) => ({
        url: `/enterprise-history/${historyId}/how-it-was/${slideId}`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, { historyId }) => [{ type: 'EnterpriseHistory', historyId }],
    }),

    addHistoryGalleryImages: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; formData: FormData }>({
      query: ({ id, formData }) => ({
        url: `/enterprise-history/${id}/gallery`,
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'EnterpriseHistory', id }],
    }),

    
    deleteHistoryGalleryImage: builder.mutation<EnterpriseHistoryAdminDetail, { historyId: number; imageId: number }>({
      query: ({ historyId, imageId }) => ({
        url: `/enterprise-history/${historyId}/gallery/${imageId}`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, { historyId }) => [{ type: 'EnterpriseHistory', historyId }],
    }),
  }),
});

export const {
  useGetAdminEnterpriseHistoriesQuery,
  useGetAdminEnterpriseHistoryQuery,
  useCreateEnterpriseHistoryMutation,
  useUpdateEnterpriseHistoryMutation,
  useDeleteEnterpriseHistoryMutation,
  useAddHistorySlideMutation,
  useDeleteHistorySlideMutation,
  useAddHistoryGalleryImagesMutation,
  useDeleteHistoryGalleryImageMutation,
} = enterpriseHistoryApi;
