export interface TimelineEvent {
  id: number;
  year: number;
  image: string;
  text: string;
}

export interface TimelineCreateRequest {
  year: number;
  text: string;
  image: File;
}
