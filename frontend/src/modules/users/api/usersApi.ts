import { baseApi } from '@/api/baseApi';
import { User, CreateAdminRequest } from '../types';

export const usersApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getUsers: builder.query<User[], void>({
      query: () => '/users/users',
      providesTags: ['Users'],
    }),
    createAdmin: builder.mutation<User, CreateAdminRequest>({
      query: (data) => ({
        url: '/users/create-admin',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Users'],
    }),
    deleteUser: builder.mutation<void, number>({
      query: (id) => ({
        url: `/users/users/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Users'],
    }),
    changePassword: builder.mutation<void, any>({
      query: (data) => ({
        url: '/users/change-password',
        method: 'POST',
        body: data,
      }),
    }),
    requestPasswordReset: builder.mutation<void, { email: string }>({
      query: (data) => ({
        url: '/users/request-password-reset',
        method: 'POST',
        body: data,
      }),
    }),
    resetPassword: builder.mutation<void, any>({
      query: (data) => ({
        url: '/users/reset-password',
        method: 'POST',
        body: data,
      }),
    }),
    adminChangePassword: builder.mutation<void, { userId: number; data: any }>({
      query: ({ userId, data }) => ({
        url: `/users/users/${userId}/change-password`,
        method: 'POST',
        body: data,
      }),
    }),
    transferSuperadmin: builder.mutation<void, number>({
      query: (userId) => ({
        url: `/users/transfer-superadmin/${userId}`,
        method: 'POST',
      }),
      invalidatesTags: ['Users'],
    }),
  }),
});

export const {
  useGetUsersQuery,
  useCreateAdminMutation,
  useDeleteUserMutation,
  useChangePasswordMutation,
  useRequestPasswordResetMutation,
  useResetPasswordMutation,
  useAdminChangePasswordMutation,
  useTransferSuperadminMutation,
} = usersApi;
