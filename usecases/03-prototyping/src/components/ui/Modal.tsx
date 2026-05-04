import { ReactNode } from 'react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: ReactNode
}

export default function Modal({ isOpen, onClose, children }: ModalProps) {
  if (!isOpen) return null

  return (
    <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-3xl p-6 m-6 max-w-sm w-full" onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}
