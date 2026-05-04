import { Home, Dog, Stethoscope, User } from 'lucide-react'
import { clsx } from 'clsx'

type Tab = 'home' | 'pets' | 'vets' | 'profile'

interface BottomNavProps {
  activeTab: Tab
  onTabChange: (tab: Tab) => void
}

export default function BottomNav({ activeTab, onTabChange }: BottomNavProps) {
  const tabs = [
    { id: 'home' as Tab, label: 'Home', icon: Home },
    { id: 'pets' as Tab, label: 'Pets', icon: Dog },
    { id: 'vets' as Tab, label: 'Vets', icon: Stethoscope },
    { id: 'profile' as Tab, label: 'Profile', icon: User },
  ]

  return (
    <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-200 pb-6">
      <div className="flex items-center justify-around px-4 pt-2">
        {tabs.map((tab) => {
          const Icon = tab.icon
          const isActive = activeTab === tab.id
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className="flex flex-col items-center gap-1 py-2 px-4 transition-colors"
            >
              <Icon
                className={clsx('w-6 h-6', {
                  'text-emerald-500': isActive,
                  'text-gray-400': !isActive,
                })}
              />
              <span
                className={clsx('text-xs font-medium', {
                  'text-emerald-500': isActive,
                  'text-gray-600': !isActive,
                })}
              >
                {tab.label}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
