import { Plus } from 'lucide-react'
import Header from '../components/layout/Header'
import BottomNav from '../components/layout/BottomNav'
import { Document } from '../App'

interface PetIdGalleryProps {
  documents: Document[]
  onAddDocument: () => void
  onViewDocument: (index: number) => void
}

export default function PetIdGallery({ documents, onAddDocument, onViewDocument }: PetIdGalleryProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <div className="h-full flex flex-col bg-white">
      <Header title="PetID" onBack={() => {}} />

      <div className="flex-1 overflow-y-auto px-4 py-4 pb-24">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Documents ({documents.length})
        </h3>

        {/* Grid of documents */}
        <div className="grid grid-cols-2 gap-4">
          {documents.map((doc, index) => (
            <button
              key={doc.id}
              onClick={() => onViewDocument(index)}
              className="aspect-square rounded-2xl overflow-hidden bg-gray-100 hover:opacity-80 transition-opacity"
            >
              <img
                src={doc.thumbnailUrl}
                alt={`Document ${index + 1}`}
                className="w-full h-full object-cover"
              />
              <div className="p-2 bg-white text-xs text-gray-600 text-left">
                {formatDate(doc.uploadedAt)}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Floating Action Button */}
      <button
        onClick={onAddDocument}
        className="absolute bottom-24 right-6 w-14 h-14 bg-emerald-500 rounded-full shadow-lg flex items-center justify-center hover:bg-emerald-600 active:scale-95 transition-all"
      >
        <Plus className="w-6 h-6 text-white" />
      </button>

      <BottomNav activeTab="pets" onTabChange={() => {}} />
    </div>
  )
}
