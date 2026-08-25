import { apiClient } from './axios'
import type { ChatRequest, ChatResponse } from '../types/chat'

/**
 * Gửi câu hỏi lên backend, nhận câu trả lời (từ FAQ rule-based hoặc Gemini fallback)
 */
export async function sendChatMessage(payload: ChatRequest): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>('/api/chat', payload)
  return data
}
