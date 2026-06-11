import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { env } from '@/config/env';

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ 
    baseUrl: env.apiBaseUrl, 
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Projects', 'Timeline', 'Users', 'EnterpriseHistory', 'Quiz', 'Subdistricts'],
  endpoints: () => ({}),
});
