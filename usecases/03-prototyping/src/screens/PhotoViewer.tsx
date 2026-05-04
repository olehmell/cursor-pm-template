import { useState } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import Header from '../components/layout/Header'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import { Document } from '../App'

interface PhotoViewerProps {
  documents: Document[]
  currentIndex: number
  onClose: () => void
  onDelete: (id: string) => void
  onIndexChange: (index: number) => void
}

export default function PhotoViewer({
  documents,
  currentIndex,
  onClose,
  onDelete,
  onIndexChange,
}: PhotoViewerProps) {
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const currentDoc = documents[currentIndex]

  const handlePrevious = () => {
    if (currentIndex > 0) {
      onIndexChange(currentIndex - 1)
    }
  }

  const handleNext = () => {
    if (currentIndex < documents.length - 1) {
      onIndexChange(currentIndex + 1)
    }
  }

  const handleDelete = () => {
    onDelete(currentDoc.id)
    setShowDeleteModal(false)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    })
  }

  return (
    <div className="h-full flex flex-col bg-black">
      <Header
        title=""
        onBack={onClose}
        rightAction="menu"
        onMenu={() => setShowDeleteModal(true)}
      />

      {/* Photo viewer */}
      <div className="flex-1 relative flex items-center justify-center">
        <img
          src={currentDoc.url}
          alt="Document"
          className="w-full h-full object-contain"
        />

        {/* Navigation arrows */}
        {currentIndex > 0 && (
          <button
            onClick={handlePrevious}
            className="absolute left-4 w-10 h-10 bg-black/50 rounded-full flex items-center justify-center hover:bg-black/70 transition-colors"
          >
            <ChevronLeft className="w-6 h-6 text-white" />
          </button>
        )}

        {currentIndex < documents.length - 1 && (
          <button
            onClick={handleNext}
            className="absolute right-4 w-10 h-10 bg-black/50 rounded-full flex items-center justify-center hover:bg-black/70 transition-colors"
          >
            <ChevronRight className="w-6 h-6 text-white" />
          </button>
        )}
      </div>

      {/* Date and navigation hint */}
      <div className="px-6 py-4 text-center">
        <div className="text-white text-sm">
          {formatDate(currentDoc.uploadedAt)}
        </div>
        <div className="text-gray-400 text-xs mt-1">
          ← → (swipe to next/prev)
        </div>
      </div>

      {/* Delete confirmation modal */}
      <Modal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)}>
        <div className="text-center space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Delete document?
          </h3>
          <p className="text-gray-600 text-sm">
            This action cannot be undone.
          </p>

          <div className="space-y-2 pt-2">
            <Button
              variant="secondary"
              onClick={() => setShowDeleteModal(false)}
              className="w-full"
            >
              Cancel
            </Button>
            <button
              onClick={handleDelete}
              className="w-full px-6 py-3 rounded-full font-medium text-red-600 hover:bg-red-50 transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
