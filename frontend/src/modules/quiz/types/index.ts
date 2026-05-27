export interface QuizOption {
  id?: number;
  text: string;
  is_correct: boolean;
  position?: number;
}

export interface QuizQuestion {
  id: number;
  question: string;
  explanation?: string;
  image?: string | null;
  options: QuizOption[];
}

export interface CreateQuizQuestionRequest {
  question: string;
  explanation?: string;
  options: QuizOption[];
  image?: File;
}

export interface CreateQuizQuestionFormData {
  question: string;
  explanation: string;
  image?: FileList | null;
  options: QuizOption[];
}
