export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  is_superuser: boolean;
}