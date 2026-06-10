export interface Subdistrict {
  name: string;
  description: string | null;
  image: string | null;
}

export interface SubdistrictEnterprise {
  id: number;
  title: string;
}

export interface SubdistrictDetail extends Subdistrict {
  enterprises: SubdistrictEnterprise[];
}

export interface SubdistrictUpdateFormData {
  description: string;
}
