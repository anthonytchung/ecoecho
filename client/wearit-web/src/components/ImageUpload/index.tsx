import { useState, ChangeEvent, FormEvent } from 'react'
import { ResultItem } from '../../../types'
import axios from 'axios'
import { Upload, Loader2, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ImageUploadProps {
  isDarkMode: boolean;
  onUploadSuccess: (results: ResultItem[]) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ isDarkMode, onUploadSuccess }) => {
  const [uploading, setUploading] = useState<boolean>(false)
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      setSelectedImage(file)
      // setPreviewUrl(URL.createObjectURL(file))
    }
  }

  const handleDragOver = (event: any) => {
    event.preventDefault();
  };

  const handleDrop = (event: any) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    setSelectedImage(droppedFile);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!selectedImage) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedImage)

      const response = await axios.post('http://localhost:8080/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      onUploadSuccess(response.data.similarMatches)
    } catch (error: any) {
      console.error('Upload error:', error.response?.data || error.message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md space-y-6">
      <div 
          className={`w-full max-w-md p-6 rounded-lg shadow-lg ${
            isDarkMode ? 'bg-gray-800' : 'bg-white'
          } border-2 border-dashed border-gray-400 cursor-pointer`}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input
            type="file"
            onChange={handleImageChange}
            className="hidden"
            id="fileInput"
            accept="image/*"
          />
          <label htmlFor="fileInput" className="flex flex-col items-center cursor-pointer">
            <Upload size={48} className="mb-4" />
            <span className="text-lg font-semibold mb-2">
              {selectedImage ? selectedImage.name : 'Click to upload or drag and drop'}
            </span>
            <span className="text-sm text-gray-500">
              Supported formats: PNG, JPG, WebP
            </span>
          </label>
        </div>

      {selectedImage && (<Button 
        type="submit" 
        disabled={!selectedImage || uploading}
        className="w-full px-6 py-3 bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-xl font-bold text-lg flex items-center justify-center hover:from-green-600 hover:to-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {uploading ? (
          <>
            <Loader2 className="animate-spin mr-2" />
            Finding Alternatives...
          </>
        ) : (
          <>
            Discover Eco Alternatives
            <ArrowRight className="ml-2" />
          </>
        )}
      </Button>
      )}
    </form>
  )
}

export default ImageUpload