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
  }),
});

export const {
  useGetUsersQuery,
  useCreateAdminMutation,
  useDeleteUserMutation,
} = usersApi;
