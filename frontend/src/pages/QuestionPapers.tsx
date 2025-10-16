import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { papersAPI } from '../services/api'
import { FileQuestion, Plus, Download, Trash2, Eye } from 'lucide-react'

interface QuestionPaper {
  id: number
  title: string
  description: string
  total_marks: number
  duration_minutes: number
  is_published: boolean
  created_at: string
}

export default function QuestionPapers() {
  const [papers, setPapers] = useState<QuestionPaper[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPapers()
  }, [])

  const loadPapers = async () => {
    try {
      const response = await papersAPI.list()
      setPapers(response.data)
    } catch (error) {
      console.error('Failed to load papers:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (paperId: number, format: string) => {
    try {
      const response = await papersAPI.export(paperId, format, false)
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `question_paper.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      alert(`Question paper exported as ${format.toUpperCase()}`)
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to export paper')
    }
  }

  const handleExportWithAnswers = async (paperId: number, format: string) => {
    try {
      const response = await papersAPI.export(paperId, format, true)
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `question_paper_with_answers.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      alert(`Question paper with answers exported as ${format.toUpperCase()}`)
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to export paper')
    }
  }

  const handleDelete = async (paperId: number) => {
    if (!confirm('Are you sure you want to delete this question paper?')) return

    try {
      await papersAPI.delete(paperId)
      loadPapers()
      alert('Question paper deleted successfully!')
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to delete paper')
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Question Papers</h1>
          <p className="text-gray-600 mt-2">Create and manage question papers</p>
        </div>
        
        <Link
          to="/papers/create"
          className="flex items-center space-x-2 px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-5 w-5" />
          <span>Create Paper</span>
        </Link>
      </div>

      {/* Papers List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading question papers...</div>
        ) : papers.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <FileQuestion className="h-12 w-12 text-gray-300 mx-auto mb-3" />
            <p>No question papers created yet</p>
            <Link
              to="/papers/create"
              className="inline-block mt-4 px-6 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700"
            >
              Create Your First Paper
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {papers.map((paper) => (
              <div key={paper.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{paper.title}</h3>
                      {paper.is_published && (
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">
                          Published
                        </span>
                      )}
                    </div>
                    
                    {paper.description && (
                      <p className="text-gray-600 mb-3">{paper.description}</p>
                    )}
                    
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span>Total Marks: {paper.total_marks}</span>
                      <span>•</span>
                      <span>Duration: {paper.duration_minutes} minutes</span>
                      <span>•</span>
                      <span>Created: {new Date(paper.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 ml-4">
                    <div className="relative group">
                      <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                        <Download className="h-5 w-5" />
                      </button>
                      
                      {/* Dropdown menu */}
                      <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
                        <div className="py-1">
                          <button
                            onClick={() => handleExport(paper.id, 'pdf')}
                            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            Export as PDF
                          </button>
                          <button
                            onClick={() => handleExport(paper.id, 'docx')}
                            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            Export as Word
                          </button>
                          <div className="border-t border-gray-200 my-1"></div>
                          <button
                            onClick={() => handleExportWithAnswers(paper.id, 'pdf')}
                            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            PDF with Answers
                          </button>
                          <button
                            onClick={() => handleExportWithAnswers(paper.id, 'docx')}
                            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            Word with Answers
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <button
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title="View paper"
                    >
                      <Eye className="h-5 w-5" />
                    </button>
                    
                    <button
                      onClick={() => handleDelete(paper.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete paper"
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
