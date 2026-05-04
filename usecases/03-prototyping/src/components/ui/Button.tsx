import { ButtonHTMLAttributes, ReactNode } from 'react'
import { clsx } from 'clsx'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  children: ReactNode
}

export default function Button({ variant = 'primary', children, className, ...props }: ButtonProps) {
  return (
    <button
      className={clsx(
        'px-6 py-3 rounded-full font-medium transition-all duration-200',
        {
          'bg-emerald-500 text-white hover:bg-emerald-600 active:scale-95': variant === 'primary',
          'bg-gray-100 text-gray-700 hover:bg-gray-200 active:scale-95': variant === 'secondary',
          'text-gray-600 hover:text-gray-900': variant === 'ghost',
        },
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
