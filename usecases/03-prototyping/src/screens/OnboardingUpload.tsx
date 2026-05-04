import { Camera, Image as ImageIcon } from 'lucide-react'
import Button from '../components/ui/Button'
import Header from '../components/layout/Header'

interface OnboardingUploadProps {
  onPhotoSelected: (photoUrl: string) => void
  onSkip: () => void
}

export default function OnboardingUpload({ onPhotoSelected, onSkip }: OnboardingUploadProps) {
  const handleTakePhoto = () => {
    // Simulate camera - use placeholder image
    const placeholderUrl = 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&q=80'
    onPhotoSelected(placeholderUrl)
  }

  const handleChooseFromGallery = () => {
    // Simulate gallery - use different placeholder
    const placeholderUrl = 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800&q=80'
    onPhotoSelected(placeholderUrl)
  }

  return (
    <div className="h-full flex flex-col bg-white">
      <Header title="" rightAction="skip" onRightAction={onSkip} />
      
      <div className="flex-1 flex flex-col items-center justify-center px-8 pb-16">
        {/* Step indicator */}
        <div className="text-sm text-gray-500 mb-8">Step 3/3</div>

        {/* Illustration */}
        <div className="w-48 h-48 mb-8 bg-gradient-to-br from-emerald-100 to-emerald-50 rounded-3xl flex items-center justify-center">
          <div className="relative">
            <div className="w-32 h-40 bg-white rounded-lg shadow-lg flex items-center justify-center">
              <svg className="w-16 h-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div className="absolute -bottom-2 -right-2 w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center shadow-lg">
              <Camera className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-2xl font-bold text-gray-900 mb-3 text-center">
          Upload your pet's passport
        </h1>

        {/* Subtitle */}
        <p className="text-gray-600 text-center mb-12 max-w-xs">
          Keep all medical records in one place
        </p>

        {/* CTAs */}
        <div className="w-full space-y-3">
          <Button
            variant="primary"
            onClick={handleTakePhoto}
            className="w-full flex items-center justify-center gap-2"
          >
            <Camera className="w-5 h-5" />
            Take Photo
          </Button>

          <Button
            variant="secondary"
            onClick={handleChooseFromGallery}
            className="w-full flex items-center justify-center gap-2"
          >
            <ImageIcon className="w-5 h-5" />
            Choose from Gallery
          </Button>
        </div>

        {/* Skip link */}
        <button
          onClick={onSkip}
          className="mt-6 text-gray-500 text-sm hover:text-gray-700 transition-colors"
        >
          Skip for now
        </button>
      </div>
    </div>
  )
}
