
export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
}

export interface Persona {
  id: string;
  username: string;
  public_name: string;
  bio?: string;
  tagline?: string;
  welcome_message?: string;
  profile_image_url?: string;
  social_links?: Record<string, any>;
}

export interface ChatInitResponse {
  session_id: string;
}

export interface ChatInvokeRequest {
  input_message: string;
}
