export interface EnterpriseHistorySlide {
  id: number;
  text: string | null;
  image: string | null;
  order_index: number;
}

export interface EnterpriseHistoryGalleryImage {
  id: number;
  image: string;
  position: number | null;
}

export interface EnterpriseHistoryAdminSummary {
  id: number;
  title: string | null;
  subdistrict: string | null;
  general_subtitle: string | null;
  short_description: string | null;
  general_main_image: string | null;
  is_draft: boolean;
}

export interface EnterprisesHistoryPublicSummary {
  id: number;
  title: string;
  subtitle: string;
  subdistrict: string;
  short_description: string;
  main_image: string;
}

export interface EnterpriseHistoryPublicDetail {
  id: number;
  title: string;
  subtitle: string;
  subdistrict: string;
  short_description: string;
  main_image: string;
  how_it_was: EnterpriseHistorySlide[];
  gallery: EnterpriseHistoryGalleryImage[];
}

export interface EnterpriseHistoryAdminDetail {
  id: number;
  title: string | null;
  subdistrict: string | null;
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
  subdistrict?: string;
  general_subtitle?: string;
  detail_subtitle?: string;
  short_description?: string;
  is_draft: boolean;
  general_main_image?: File;
  detail_main_image?: File;
}

export interface CreateEnterpriseHistoryFormData {
  title: string;
  subdistrict: string;
  general_subtitle: string;
  detail_subtitle: string;
  short_description: string;
  is_draft: boolean;
  general_main_image?: FileList;
  detail_main_image?: FileList;
  gallery?: FileList;
  slides?: {
    text: string;
    image?: File;
  }[];
}

export interface UpdateEnterpriseHistoryFormData {
  title: string;
  subdistrict: string;
  general_subtitle: string;
  detail_subtitle: string;
  short_description: string;
  is_draft: boolean;
}
