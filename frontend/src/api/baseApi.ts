import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { env } from '@/config/env';

const rawBaseQuery = fetchBaseQuery({
    baseUrl: env.apiBaseUrl, 
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
});

const baseQuery: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
  args, api, extraOptions,
) => {
  const requestToken = localStorage.getItem('token');
  const result = await rawBaseQuery(args, api, extraOptions);
  // Не сбрасываем новую сессию из-за запоздавшего ответа старого запроса.
  if (result.error?.status === 401 && requestToken && localStorage.getItem('token') === requestToken) {
    localStorage.removeItem('token');
    if (window.location.pathname === '/admin' || window.location.pathname.startsWith('/admin/')) {
      window.location.replace('/admin?session=expired');
    }
  }
  return result;
};

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery,
  tagTypes: ['Projects', 'Timeline', 'Users', 'EnterpriseHistory', 'Quiz', 'Subdistricts'],
  endpoints: () => ({}),
});
