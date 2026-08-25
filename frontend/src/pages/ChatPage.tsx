import { useEffect, useRef } from 'react'
import { useChat } from '../hooks/useChat'
import { MessageBubble } from '../components/MessageBubble'
import { TypingIndicator } from '../components/TypingIndicator'
import { ChatInput } from '../components/ChatInput'
import { BotAvatar } from '../components/BotAvatar'

export function ChatPage() {
  const { messages, isLoading, error, sendMessage } = useChat()
  const bottomRef = useRef<HTMLDivElement>(null)

  // Tự cuộn xuống tin nhắn mới nhất mỗi khi có thay đổi
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="chat-page">
      <header className="chat-header">
        <BotAvatar />
        <div>
          <h1>StudyBot</h1>
          <p className="chat-header__subtitle">Trợ lý hỗ trợ sinh viên</p>
        </div>
      </header>

      <main className="chat-window">
        {messages.map((m) => (
          <MessageBubble key={m.id} message={m} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </main>

      {error && <div className="chat-error-banner">{error}</div>}

      <footer>
        <ChatInput onSend={sendMessage} disabled={isLoading} />
      </footer>
    </div>
  )
}
