export interface GalleryImage {
  id: number;
  image: string;
  position: number;
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

export interface AdminProjectListItem {
  id: number;
  title: string;
  author: string;
  short_description: string;
  main_image: string;
  is_draft: boolean;
}