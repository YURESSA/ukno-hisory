import { baseApi } from '@/api/baseApi';
import { QuizQuestion } from '../types';

export const quizApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getQuizQuestions: builder.query<QuizQuestion[], void>({
      query: () => '/quiz',
      providesTags: ['Quiz'],
    }),
    
    getQuizQuestion: builder.query<QuizQuestion, number>({
      query: (id) => `/quiz/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'Quiz', id }],
    }),

    createQuizQuestion: builder.mutation<QuizQuestion, FormData>({
      query: (formData) => ({
        url: '/quiz',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Quiz'],
    }),

    updateQuizQuestion: builder.mutation<QuizQuestion, { id: number; data: Partial<QuizQuestion> }>({
      query: ({ id, data }) => ({
        url: `/quiz/${id}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: (_result, _error, { id }) => ['Quiz', { type: 'Quiz', id }],
    }),

    deleteQuizQuestion: builder.mutation<void, number>({
      query: (id) => ({
        url: `/quiz/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Quiz'],
    }),

    updateQuizQuestionImage: builder.mutation<QuizQuestion, { id: number; image: File }>({
      query: ({ id, image }) => {
        const formData = new FormData();
        formData.append('image', image);
        return {
          url: `/quiz/${id}/image`,
          method: 'PUT',
          body: formData,
        };
      },
      invalidatesTags: (_result, _error, { id }) => [{ type: 'Quiz', id }],
    }),

    deleteQuizQuestionImage: builder.mutation<QuizQuestion, number>({
      query: (id) => ({
        url: `/quiz/${id}/image`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, id) => [{ type: 'Quiz', id }],
    }),
  }),
});

export const {
  useGetQuizQuestionsQuery,
  useGetQuizQuestionQuery,
  useCreateQuizQuestionMutation,
  useUpdateQuizQuestionMutation,
  useDeleteQuizQuestionMutation,
  useUpdateQuizQuestionImageMutation,
  useDeleteQuizQuestionImageMutation,
} = quizApi;
