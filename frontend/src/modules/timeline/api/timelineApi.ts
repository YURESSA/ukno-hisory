import { baseApi } from '@/api/baseApi';
import { TimelineEvent } from '../types';

export const timelineApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getTimeline: builder.query<TimelineEvent[], void>({
      query: () => '/timeline',
      providesTags: ['Timeline'],
    }),
    createTimeline: builder.mutation<TimelineEvent, FormData>({
      query: (formData) => ({
        url: '/timeline',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Timeline'],
    }),
    updateTimeline: builder.mutation<TimelineEvent, { id: number; data: Partial<TimelineEvent> }>({
      query: ({ id, data }) => ({
        url: `/timeline/${id}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: ['Timeline'],
    }),
    deleteTimeline: builder.mutation<void, number>({
      query: (id) => ({
        url: `/timeline/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Timeline'],
    }),
    updateTimelineImage: builder.mutation<TimelineEvent, { id: number; image: File }>({
      query: ({ id, image }) => {
        const formData = new FormData();
        formData.append('image', image);
        return {
          url: `/timeline/${id}/image`,
          method: 'PUT',
          body: formData,
        };
      },
      invalidatesTags: ['Timeline'],
    }),
    deleteTimelineImage: builder.mutation<TimelineEvent, number>({
      query: (id) => ({
        url: `/timeline/${id}/image`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Timeline'],
    }),
  }),
});

export const {
  useGetTimelineQuery,
  useCreateTimelineMutation,
  useUpdateTimelineMutation,
  useDeleteTimelineMutation,
  useUpdateTimelineImageMutation,
  useDeleteTimelineImageMutation,
} = timelineApi;
