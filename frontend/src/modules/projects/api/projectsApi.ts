import { baseApi } from '@/api/baseApi';

export const projectsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getProjects: builder.query<any, void>({
      query: () => '/student-projects',
    }),
  }),
});

export const { useGetProjectsQuery } = projectsApi;