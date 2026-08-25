import { useCallback, useRef, useState } from 'react'
import { sendChatMessage } from '../api/chat'
import type { ChatMessage } from '../types/chat'

const SESSION_KEY = 'chat_session_id'

// Mỗi tab trình duyệt giữ 1 session_id riêng (theo yêu cầu backend: session_id bắt buộc)
function getOrCreateSessionId(): string {
  let id = sessionStorage.getItem(SESSION_KEY)
  if (!id) {
    id = crypto.randomUUID()
    sessionStorage.setItem(SESSION_KEY, id)
  }
  return id
}

export function useChat() {
  const sessionId = useRef(getOrCreateSessionId())
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: crypto.randomUUID(),
      role: 'bot',
      content: 'Xin chào! Mình là trợ lý hỗ trợ sinh viên. Bạn cần hỏi gì nào?',
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sendMessage = useCallback(async (text: string) => {
    const trimmed = text.trim()
    if (!trimmed || isLoading) return

    setError(null)

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmed,
    }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    try {
      const res = await sendChatMessage({
        session_id: sessionId.current,
        message: trimmed,
      })

      const botMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'bot',
        content: res.answer,
        source: res.source,
      }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      const message = getErrorMessage(err)
      setError(message)
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'bot',
          content: message,
          isError: true,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }, [isLoading])

  return { messages, isLoading, error, sendMessage }
}

function getErrorMessage(err: unknown): string {
  if (err && typeof err === 'object' && 'code' in err && err.code === 'ECONNABORTED') {
    return 'Server phản hồi quá lâu, vui lòng thử lại.'
  }
  if (err && typeof err === 'object' && 'response' in err) {
    return 'Không nhận được phản hồi hợp lệ từ server. Vui lòng thử lại sau.'
  }
  return 'Không thể kết nối tới server. Kiểm tra lại kết nối mạng hoặc backend có đang chạy không.'
}
