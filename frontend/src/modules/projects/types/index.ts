export interface GalleryImage {
  id: number;
  image: string;
  position: number;
}

export interface ProjectTags {
  author: string | null;
  year: number | null;
  tag_one: string | null;
  tag_two: string | null;
}

export interface ProjectDetail {
  id: number;
  title: string;
  main_image: string | null;
  short_description?: string | null;
  description: string | null;
  tags: ProjectTags;
  gallery: GalleryImage[];
}

export interface StudentProject {
  id: number;
  title: string;
  author: string | null;
  short_description: string | null;
  description: string | null;
  main_image: string | null;
  year: number | null;
  tag_one: string | null;
  tag_two: string | null;
  is_draft: boolean;
  gallery: GalleryImage[];
}

export interface CreateProjectFormData {
  title: string;
  author: string;
  short_description: string;
  description: string;
  year: string;
  tag_one: string;
  tag_two: string;
  is_draft: boolean;
  main_image?: FileList;
  gallery?: FileList;
}

export interface UpdateProjectFormData {
  title: string;
  author: string;
  short_description: string;
  description: string;
  year: number;
  tag_one: string;
  tag_two: string;
  is_draft: boolean;
}

export interface AdminProjectListItem {
  id: number;
  title: string;
  author: string;
  short_description: string;
  main_image: string;
  is_draft: boolean;
}