import { useState } from 'react'
import type { FormEvent, KeyboardEvent } from 'react'
import { Send } from 'lucide-react'

interface Props {
  onSend: (text: string) => void
  disabled: boolean
}

export function ChatInput({ onSend, disabled }: Props) {
  const [value, setValue] = useState('')

  const submit = (e: FormEvent) => {
    e.preventDefault()
    if (!value.trim() || disabled) return
    onSend(value)
    setValue('')
  }

  // Enter để gửi, Shift+Enter để xuống dòng
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit(e)
    }
  }

  return (
    <form className="chat-input" onSubmit={submit}>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Nhập câu hỏi của bạn..."
        rows={1}
        disabled={disabled}
      />
      <button type="submit" disabled={disabled || !value.trim()} aria-label="Gửi câu hỏi">
        <Send size={18} />
      </button>
    </form>
  )
}
