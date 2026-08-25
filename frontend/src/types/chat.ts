// Khớp với app/schemas/chat.py bên backend

export interface ChatRequest {
  session_id: string
  message: string
}

export interface ChatResponse {
  answer: string
  source: string
  timestamp: string
}

// Dùng để hiển thị bong bóng hội thoại trên UI
export type MessageRole = 'user' | 'bot'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  source?: string
  isError?: boolean
}
