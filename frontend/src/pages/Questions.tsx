import { useEffect, useState } from 'react'
import { questionsAPI, documentsAPI } from '../services/api'
import { BookOpen, Plus, Trash2, Edit, Sparkles } from 'lucide-react'

interface Question {
  id: number
  question_text: string
  question_type: string
  difficulty: string
  correct_answer: string
  suggested_marks: number
  created_at: string
}

interface Document {
  id: number
  original_filename: string
  is_processed: boolean
}

export default function Questions() {
  const [questions, setQuestions] = useState<Question[]>([])
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [showGenerateModal, setShowGenerateModal] = useState(false)
  const [generateConfig, setGenerateConfig] = useState({
    document_id: 0,
    num_questions: 10,
    question_types: ['mcq', 'short_answer'],
    difficulty_easy: 0.4,
    difficulty_medium: 0.4,
    difficulty_hard: 0.2,
  })
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    loadQuestions()
    loadDocuments()
  }, [])

  const loadQuestions = async () => {
    try {
      const response = await questionsAPI.list()
      setQuestions(response.data)
    } catch (error) {
      console.error('Failed to load questions:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list()
      setDocuments(response.data.filter((doc: Document) => doc.is_processed))
    } catch (error) {
      console.error('Failed to load documents:', error)
    }
  }

  const handleGenerate = async () => {
    if (!generateConfig.document_id) {
      alert('Please select a document')
      return
    }

    setGenerating(true)
    try {
      await questionsAPI.generate(generateConfig)
      alert('Questions generated successfully!')
      setShowGenerateModal(false)
      loadQuestions()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to generate questions')
    } finally {
      setGenerating(false)
    }
  }

  const handleDelete = async (questionId: number) => {
    if (!confirm('Are you sure you want to delete this question?')) return

    try {
      await questionsAPI.delete(questionId)
      loadQuestions()
      alert('Question deleted successfully!')
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to delete question')
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'hard':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      mcq: 'MCQ',
      true_false: 'True/False',
      short_answer: 'Short Answer',
      long_answer: 'Long Answer',
      fill_blank: 'Fill in Blank',
      programming: 'Programming',
    }
    return labels[type] || type
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Questions</h1>
          <p className="text-gray-600 mt-2">Manage your question bank</p>
        </div>
        
        <button
          onClick={() => setShowGenerateModal(true)}
          className="flex items-center space-x-2 px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          <Sparkles className="h-5 w-5" />
          <span>Generate Questions</span>
        </button>
      </div>

      {/* Questions List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading questions...</div>
        ) : questions.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <BookOpen className="h-12 w-12 text-gray-300 mx-auto mb-3" />
            <p>No questions generated yet</p>
            <button
              onClick={() => setShowGenerateModal(true)}
              className="mt-4 px-6 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700"
            >
              Generate Your First Questions
            </button>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {questions.map((question) => (
              <div key={question.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(question.difficulty)}`}>
                        {question.difficulty}
                      </span>
                      <span className="px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800">
                        {getTypeLabel(question.question_type)}
                      </span>
                      <span className="text-xs text-gray-500">
                        {question.suggested_marks} marks
                      </span>
                    </div>
                    
                    <p className="text-gray-900 font-medium mb-2">{question.question_text}</p>
                    
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Answer:</span> {question.correct_answer.substring(0, 100)}
                      {question.correct_answer.length > 100 && '...'}
                    </p>
                  </div>

                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title="Edit question"
                    >
                      <Edit className="h-5 w-5" />
                    </button>
                    
                    <button
                      onClick={() => handleDelete(question.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete question"
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

      {/* Generate Modal */}
      {showGenerateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Generate Questions</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Document
                </label>
                <select
                  value={generateConfig.document_id}
                  onChange={(e) => setGenerateConfig({ ...generateConfig, document_id: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
                >
                  <option value={0}>Choose a document...</option>
                  {documents.map((doc) => (
                    <option key={doc.id} value={doc.id}>
                      {doc.original_filename}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Questions: {generateConfig.num_questions}
                </label>
                <input
                  type="range"
                  min="5"
                  max="50"
                  value={generateConfig.num_questions}
                  onChange={(e) => setGenerateConfig({ ...generateConfig, num_questions: parseInt(e.target.value) })}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Question Types
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {['mcq', 'true_false', 'short_answer', 'long_answer', 'fill_blank'].map((type) => (
                    <label key={type} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={generateConfig.question_types.includes(type)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setGenerateConfig({
                              ...generateConfig,
                              question_types: [...generateConfig.question_types, type],
                            })
                          } else {
                            setGenerateConfig({
                              ...generateConfig,
                              question_types: generateConfig.question_types.filter((t) => t !== type),
                            })
                          }
                        }}
                        className="rounded"
                      />
                      <span className="text-sm text-gray-700">{getTypeLabel(type)}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Easy: {(generateConfig.difficulty_easy * 100).toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={generateConfig.difficulty_easy}
                    onChange={(e) => setGenerateConfig({ ...generateConfig, difficulty_easy: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Medium: {(generateConfig.difficulty_medium * 100).toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={generateConfig.difficulty_medium}
                    onChange={(e) => setGenerateConfig({ ...generateConfig, difficulty_medium: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Hard: {(generateConfig.difficulty_hard * 100).toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={generateConfig.difficulty_hard}
                    onChange={(e) => setGenerateConfig({ ...generateConfig, difficulty_hard: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-4 mt-6">
              <button
                onClick={() => setShowGenerateModal(false)}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleGenerate}
                disabled={generating}
                className="px-6 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                {generating ? 'Generating...' : 'Generate'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
