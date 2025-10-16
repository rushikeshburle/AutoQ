import { useEffect, useState } from 'react'
import { documentsAPI } from '../services/api'
import { Upload, FileText, Trash2, RefreshCw, CheckCircle, Clock, XCircle } from 'lucide-react'

interface Document {
  id: number
  filename: string
  original_filename: string
  file_size: number
  is_processed: boolean
  processing_status: string
  created_at: string
}

export default function Documents() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list()
      setDocuments(response.data)
    } catch (error) {
      console.error('Failed to load documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
    try {
      await documentsAPI.upload(selectedFile)
      setSelectedFile(null)
      loadDocuments()
      alert('Document uploaded successfully!')
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to upload document')
    } finally {
      setUploading(false)
    }
  }

  const handleProcess = async (documentId: number) => {
    try {
      await documentsAPI.process(documentId)
      alert('Document processing started!')
      loadDocuments()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to process document')
    }
  }

  const handleDelete = async (documentId: number) => {
    if (!confirm('Are you sure you want to delete this document?')) return

    try {
      await documentsAPI.delete(documentId)
      loadDocuments()
      alert('Document deleted successfully!')
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to delete document')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'processing':
        return <RefreshCw className="h-5 w-5 text-blue-500 animate-spin" />
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <Clock className="h-5 w-5 text-gray-400" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Documents</h1>
        <p className="text-gray-600 mt-2">Upload and manage your PDF documents</p>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload New Document</h2>
        
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <label className="flex items-center justify-center w-full px-4 py-6 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-primary hover:bg-blue-50 transition-colors">
              <div className="text-center">
                <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-600">
                  {selectedFile ? selectedFile.name : 'Click to select a PDF file'}
                </p>
                <p className="text-xs text-gray-500 mt-1">Maximum file size: 50MB</p>
              </div>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
              />
            </label>
          </div>

          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className="px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Your Documents</h2>
        </div>

        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-3" />
            <p>No documents uploaded yet</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {documents.map((doc) => (
              <div key={doc.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 flex-1">
                    <FileText className="h-10 w-10 text-blue-500" />
                    
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{doc.original_filename}</h3>
                      <div className="flex items-center space-x-4 mt-1 text-sm text-gray-500">
                        <span>{formatFileSize(doc.file_size)}</span>
                        <span>•</span>
                        <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      {getStatusIcon(doc.processing_status)}
                      <span className="text-sm font-medium text-gray-700 capitalize">
                        {doc.processing_status}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 ml-4">
                    {!doc.is_processed && doc.processing_status !== 'processing' && (
                      <button
                        onClick={() => handleProcess(doc.id)}
                        className="px-4 py-2 bg-green-500 text-white rounded-lg text-sm font-medium hover:bg-green-600 transition-colors"
                      >
                        Process
                      </button>
                    )}
                    
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete document"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
