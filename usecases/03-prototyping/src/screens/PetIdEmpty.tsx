import { FolderOpen } from 'lucide-react'
import Button from '../components/ui/Button'
import Header from '../components/layout/Header'
import BottomNav from '../components/layout/BottomNav'

interface PetIdEmptyProps {
  onUpload: () => void
}

export default function PetIdEmpty({ onUpload }: PetIdEmptyProps) {
  return (
    <div className="h-full flex flex-col bg-white">
      <Header title="PetID" onBack={() => {}} />

      <div className="flex-1 flex flex-col items-center justify-center px-8 pb-24">
        {/* Empty state illustration */}
        <div className="w-32 h-32 mb-8 bg-gray-100 rounded-3xl flex items-center justify-center">
          <FolderOpen className="w-16 h-16 text-gray-300" />
        </div>

        {/* Title */}
        <h2 className="text-xl font-semibold text-gray-900 mb-3 text-center">
          No documents yet
        </h2>

        {/* Description */}
        <p className="text-gray-600 text-center mb-8 max-w-xs">
          Upload your pet's passport, vaccination records, or medical documents
        </p>

        {/* CTA */}
        <Button
          variant="primary"
          onClick={onUpload}
          className="flex items-center gap-2"
        >
          <span className="text-xl">+</span>
          Upload Document
        </Button>
      </div>

      <BottomNav activeTab="pets" onTabChange={() => {}} />
    </div>
  )
}
