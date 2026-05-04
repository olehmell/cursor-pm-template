import { useState } from 'react'
import MobileFrame from './components/layout/MobileFrame'
import OnboardingUpload from './screens/OnboardingUpload'
import PhotoPreview from './screens/PhotoPreview'
import UploadProgress from './screens/UploadProgress'
import UploadSuccess from './screens/UploadSuccess'
import PetIdEmpty from './screens/PetIdEmpty'
import PetIdGallery from './screens/PetIdGallery'
import PhotoViewer from './screens/PhotoViewer'

export type Screen = 
  | 'onboarding'
  | 'photo-preview'
  | 'upload-progress'
  | 'upload-success'
  | 'petid-empty'
  | 'petid-gallery'
  | 'photo-viewer'

export interface Document {
  id: string
  url: string
  thumbnailUrl: string
  uploadedAt: string
}

function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('onboarding')
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null)
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDocumentIndex, setSelectedDocumentIndex] = useState<number>(0)

  const handlePhotoSelected = (photoUrl: string) => {
    setSelectedPhoto(photoUrl)
    setCurrentScreen('photo-preview')
  }

  const handleUpload = () => {
    setCurrentScreen('upload-progress')
    
    // Simulate upload
    setTimeout(() => {
      setCurrentScreen('upload-success')
      
      // Add document to list
      const newDoc: Document = {
        id: Date.now().toString(),
        url: selectedPhoto!,
        thumbnailUrl: selectedPhoto!,
        uploadedAt: new Date().toISOString(),
      }
      setDocuments(prev => [newDoc, ...prev])
      
      // Auto-close success screen
      setTimeout(() => {
        setCurrentScreen('petid-gallery')
      }, 2000)
    }, 3000)
  }

  const handleDeleteDocument = (id: string) => {
    setDocuments(prev => prev.filter(doc => doc.id !== id))
    setCurrentScreen('petid-gallery')
  }

  const handleSkip = () => {
    setCurrentScreen(documents.length > 0 ? 'petid-gallery' : 'petid-empty')
  }

  const handleViewDocument = (index: number) => {
    setSelectedDocumentIndex(index)
    setCurrentScreen('photo-viewer')
  }

  const renderScreen = () => {
    switch (currentScreen) {
      case 'onboarding':
        return <OnboardingUpload onPhotoSelected={handlePhotoSelected} onSkip={handleSkip} />
      case 'photo-preview':
        return (
          <PhotoPreview
            photoUrl={selectedPhoto!}
            onUpload={handleUpload}
            onRetake={() => setCurrentScreen('onboarding')}
            onCancel={() => setCurrentScreen('onboarding')}
          />
        )
      case 'upload-progress':
        return <UploadProgress onCancel={() => setCurrentScreen('photo-preview')} />
      case 'upload-success':
        return <UploadSuccess />
      case 'petid-empty':
        return <PetIdEmpty onUpload={() => setCurrentScreen('onboarding')} />
      case 'petid-gallery':
        return (
          <PetIdGallery
            documents={documents}
            onAddDocument={() => setCurrentScreen('onboarding')}
            onViewDocument={handleViewDocument}
          />
        )
      case 'photo-viewer':
        return (
          <PhotoViewer
            documents={documents}
            currentIndex={selectedDocumentIndex}
            onClose={() => setCurrentScreen('petid-gallery')}
            onDelete={handleDeleteDocument}
            onIndexChange={setSelectedDocumentIndex}
          />
        )
      default:
        return <OnboardingUpload onPhotoSelected={handlePhotoSelected} onSkip={handleSkip} />
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <MobileFrame>{renderScreen()}</MobileFrame>
    </div>
  )
}

export default App
