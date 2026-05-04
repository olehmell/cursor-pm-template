import { ArrowLeft, Share2, MoreVertical } from 'lucide-react'

interface HeaderProps {
  title: string
  onBack?: () => void
  onShare?: () => void
  onMenu?: () => void
  rightAction?: 'share' | 'menu' | 'add' | 'skip'
  onRightAction?: () => void
}

export default function Header({ title, onBack, onShare, onMenu, rightAction, onRightAction }: HeaderProps) {
  return (
    <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
      <div className="w-10">
        {onBack && (
          <button onClick={onBack} className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </button>
        )}
      </div>
      
      <h1 className="text-lg font-semibold text-gray-900">{title}</h1>
      
      <div className="w-10 flex justify-end">
        {rightAction === 'share' && onShare && (
          <button onClick={onShare} className="text-emerald-500 font-medium">
            Share
          </button>
        )}
        {rightAction === 'menu' && onMenu && (
          <button onClick={onMenu} className="p-2 -mr-2 hover:bg-gray-100 rounded-full transition-colors">
            <MoreVertical className="w-5 h-5" />
          </button>
        )}
        {rightAction === 'skip' && onRightAction && (
          <button onClick={onRightAction} className="text-gray-600 font-medium">
            Skip
          </button>
        )}
      </div>
    </div>
  )
}
