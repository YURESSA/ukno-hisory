import { baseApi } from '@/api/baseApi';
import { LoginResponse } from '../types';

export const authApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation<LoginResponse, any>({
      query: (credentials) => ({
        url: '/users/login',
        method: 'POST',
        body: credentials,
      }),
    }),
  }),
});

export const { useLoginMutation } = authApi;