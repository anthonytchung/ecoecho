import { useState, ChangeEvent, FormEvent } from 'react'
import { ResultItem } from '../../../types'
import axios from 'axios'
import { Upload, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button';

interface ImageUploadProps {
  onUploadSuccess: (results: ResultItem[]) => void;
}

export default function ImageUpload({ onUploadSuccess }: ImageUploadProps) {
  const [uploading, setUploading] = useState<boolean>(false)
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      setSelectedImage(file)
      setPreviewUrl(URL.createObjectURL(file))
    }
  }

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
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="flex items-center justify-center w-full">
        {/* <span className="text-gray-500 dark:text-gray-400"><Button>Upload</Button></span> */}
        <label htmlFor="image-upload" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600 overflow-hidden">
          <div className="flex flex-col items-center justify-center pt-5 pb-6 w-full h-full">
            {previewUrl ? (
              <div className="w-full h-full flex items-center justify-center">
                <img src={previewUrl} alt="Preview" className="max-w-full max-h-full object-contain" />
              </div>
            ) : (
              <>
                <Upload className="w-10 h-10 mb-3 text-gray-400" />
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">PNG, JPG or GIF (MAX. 800x400px)</p>
              </>
            )}
          </div>
          <input id="image-upload" type="file" accept="image/*" onChange={handleImageChange} className="hidden" />
        </label>
      </div>
      <button 
        type="submit" 
        disabled={!selectedImage || uploading}
        className="w-full px-4 py-3 font-bold text-white bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg hover:from-purple-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-opacity-50 transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {uploading ? (
          <>
            <Loader2 className="animate-spin mr-2" />
            Finding Alternatives...
          </>
        ) : (
          'Discover Options'
        )}
      </button> 
    </form>
  )
}