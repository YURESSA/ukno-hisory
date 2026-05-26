export interface EnterpriseHistorySlide {
  id: number;
  text: string | null;
  image: string | null;
  order_index: number;
}

export interface EnterpriseHistoryGalleryImage {
  id: number;
  image: string;
  position: number;
}

export interface EnterpriseHistoryAdminSummary {
  id: number;
  title: string | null;
  general_subtitle: string | null;
  short_description: string | null;
  general_main_image: string | null;
  is_draft: boolean;
}

export interface EnterpriseHistoryAdminDetail {
  id: number;
  title: string | null;
  general_subtitle: string | null;
  detail_subtitle: string | null;
  short_description: string | null;
  general_main_image: string | null;
  detail_main_image: string | null;
  is_draft: boolean;
  how_it_was: EnterpriseHistorySlide[];
  gallery: EnterpriseHistoryGalleryImage[];
}

export interface EnterpriseHistoryCreateRequest {
  title?: string;
  general_subtitle?: string;
  detail_subtitle?: string;
  short_description?: string;
  is_draft: boolean;
  general_main_image?: File;
  detail_main_image?: File;
}

export interface CreateEnterpriseHistoryFormData {
  title: string;
  general_subtitle: string;
  detail_subtitle: string;
  short_description: string;
  is_draft: boolean;
  general_main_image?: FileList;
  detail_main_image?: FileList;
}

export interface UpdateEnterpriseHistoryFormData {
  title: string;
  general_subtitle: string;
  detail_subtitle: string;
  short_description: string;
  is_draft: boolean;
}
