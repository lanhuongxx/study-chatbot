import { GraduationCap } from 'lucide-react'

export function BotAvatar({ size = 'md' }: { size?: 'sm' | 'md' }) {
  return (
    <div className={`bot-avatar bot-avatar--${size}`}>
      <GraduationCap strokeWidth={2.2} />
    </div>
  )
}
