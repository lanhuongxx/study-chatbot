import { BotAvatar } from './BotAvatar'

export function TypingIndicator() {
  return (
    <div className="chat-row chat-row--bot">
      <BotAvatar size="sm" />
      <div className="chat-bubble chat-bubble--bot chat-bubble--typing">
        <span className="dot" />
        <span className="dot" />
        <span className="dot" />
      </div>
    </div>
  )
}
