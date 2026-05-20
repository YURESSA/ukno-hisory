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
