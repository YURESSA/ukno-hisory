export enum UserRole {
  ADMIN = 'admin',
  SUPER_ADMIN = 'superadmin'
}

export interface User {
  id: number;
  email: string;
  role: UserRole;
}

export interface CreateAdminRequest {
  email: string;
}

export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

export interface AdminChangePasswordRequest {
  new_password: string;
}
