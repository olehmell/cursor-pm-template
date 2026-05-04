import Button from '../components/ui/Button'
import Header from '../components/layout/Header'

interface PhotoPreviewProps {
  photoUrl: string
  onUpload: () => void
  onRetake: () => void
  onCancel: () => void
}

export default function PhotoPreview({ photoUrl, onUpload, onRetake, onCancel }: PhotoPreviewProps) {
  const originalSize = 3.2
  const compressedSize = 1.0

  return (
    <div className="h-full flex flex-col bg-white">
      <Header title="" onBack={onCancel} />

      {/* Photo preview */}
      <div className="flex-1 bg-gray-900 flex items-center justify-center overflow-hidden">
        <img
          src={photoUrl}
          alt="Preview"
          className="w-full h-full object-contain"
        />
      </div>

      {/* Info and actions */}
      <div className="px-6 py-6 space-y-4">
        <div className="text-sm text-gray-600 text-center">
          <div>File size: {originalSize} MB</div>
          <div>Will be compressed to {compressedSize} MB</div>
        </div>

        <Button
          variant="primary"
          onClick={onUpload}
          className="w-full"
        >
          ✓ Upload
        </Button>

        <button
          onClick={onRetake}
          className="w-full text-gray-600 text-sm hover:text-gray-900 transition-colors"
        >
          Retake photo
        </button>
      </div>
    </div>
  )
}
