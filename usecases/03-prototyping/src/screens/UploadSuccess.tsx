import { useEffect, useState } from 'react'

export default function UploadSuccess() {
  const [show, setShow] = useState(false)

  useEffect(() => {
    // Trigger animation
    setTimeout(() => setShow(true), 100)
  }, [])

  return (
    <div className="h-full flex flex-col items-center justify-center bg-white">
      <div
        className={`transition-all duration-500 ${
          show ? 'scale-100 opacity-100' : 'scale-50 opacity-0'
        }`}
      >
        {/* Checkmark animation */}
        <div className="w-24 h-24 bg-emerald-500 rounded-full flex items-center justify-center mb-6 shadow-lg">
          <svg
            className="w-12 h-12 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={3}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>

        <h2 className="text-xl font-semibold text-gray-900 text-center">
          Document uploaded!
        </h2>
      </div>
    </div>
  )
}
