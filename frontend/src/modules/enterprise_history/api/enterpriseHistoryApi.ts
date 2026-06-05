import { baseApi } from '@/api/baseApi';
import { EnterpriseHistoryAdminSummary, EnterpriseHistoryAdminDetail, EnterpriseHistoryPublicSummary } from '../types';

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

    getPublicEnterpriseHistory: builder.query<EnterpriseHistoryPublicSummary[], void>({
      query: () => '/enterprise-history',
      providesTags: ['EnterpriseHistory']
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

    updateHistoryGeneralMainImage: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; image: File }>({
      query: ({ id, image }) => {
        const formData = new FormData();
        formData.append('image', image);
        return {
          url: `/enterprise-history/${id}/general-main-image`,
          method: 'PUT',
          body: formData,
        };
      },
      invalidatesTags: (_result, _error, { id }) => [{ type: 'EnterpriseHistory', id }],
    }),

    updateHistoryDetailMainImage: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; image: File }>({
      query: ({ id, image }) => {
        const formData = new FormData();
        formData.append('image', image);
        return {
          url: `/enterprise-history/${id}/detail-main-image`,
          method: 'PUT',
          body: formData,
        };
      },
      invalidatesTags: (_result, _error, { id }) => [{ type: 'EnterpriseHistory', id }],
    }),

    reorderHistorySlides: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; slideIds: number[] }>({
      query: ({ id, slideIds }) => ({
        url: `/enterprise-history/${id}/how-it-was/order`,
        method: 'PUT',
        body: { slide_ids: slideIds },
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'EnterpriseHistory', id }],
    }),

    reorderHistoryGallery: builder.mutation<EnterpriseHistoryAdminDetail, { id: number; imageIds: number[] }>({
      query: ({ id, imageIds }) => ({
        url: `/enterprise-history/${id}/gallery/order`,
        method: 'PUT',
        body: { image_ids: imageIds },
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'EnterpriseHistory', id }],
    }),
  }),
});

export const {
  useGetAdminEnterpriseHistoriesQuery,
  useGetAdminEnterpriseHistoryQuery,
  useGetPublicEnterpriseHistoryQuery,
  useCreateEnterpriseHistoryMutation,
  useUpdateEnterpriseHistoryMutation,
  useDeleteEnterpriseHistoryMutation,
  useAddHistorySlideMutation,
  useDeleteHistorySlideMutation,
  useAddHistoryGalleryImagesMutation,
  useDeleteHistoryGalleryImageMutation,
  useUpdateHistoryGeneralMainImageMutation,
  useUpdateHistoryDetailMainImageMutation,
  useReorderHistorySlidesMutation,
  useReorderHistoryGalleryMutation,
} = enterpriseHistoryApi;
