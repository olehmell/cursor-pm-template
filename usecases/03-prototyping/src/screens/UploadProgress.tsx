import { useState, useEffect } from 'react'
import ProgressBar from '../components/ui/ProgressBar'
import Button from '../components/ui/Button'

interface UploadProgressProps {
  onCancel: () => void
}

export default function UploadProgress({ onCancel }: UploadProgressProps) {
  const [progress, setProgress] = useState(0)
  const totalSize = 3.2
  const uploadedSize = (totalSize * progress) / 100

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 2
      })
    }, 60)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="h-full flex flex-col items-center justify-center bg-white px-8">
      <div className="w-full max-w-xs space-y-6">
        <h2 className="text-xl font-semibold text-gray-900 text-center">
          Uploading...
        </h2>

        <ProgressBar progress={progress} />

        <div className="text-sm text-gray-600 text-center">
          {uploadedSize.toFixed(1)} MB / {totalSize} MB
        </div>

        <Button
          variant="ghost"
          onClick={onCancel}
          className="w-full"
        >
          Cancel
        </Button>
      </div>
    </div>
  )
}
