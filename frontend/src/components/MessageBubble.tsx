import { Sparkles, BookOpenCheck } from 'lucide-react'
import type { ChatMessage } from '../types/chat'
import { BotAvatar } from './BotAvatar'

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user'

  return (
    <div className={`chat-row ${isUser ? 'chat-row--user' : 'chat-row--bot'}`}>
      {!isUser && <BotAvatar size="sm" />}
      <div
        className={`chat-bubble ${isUser ? 'chat-bubble--user' : 'chat-bubble--bot'} ${
          message.isError ? 'chat-bubble--error' : ''
        }`}
      >
        <p>{message.content}</p>
        {message.source && (
          <span className="chat-bubble__source">
            {message.source === 'faq' ? (
              <>
                <BookOpenCheck size={12} /> Từ danh sách FAQ
              </>
            ) : (
              <>
                <Sparkles size={12} /> Trả lời bởi AI
              </>
            )}
          </span>
        )}
      </div>
    </div>
  )
}
