import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { questionsAPI, papersAPI } from '../services/api'
import { ArrowLeft, CheckSquare } from 'lucide-react'

interface Question {
  id: number
  question_text: string
  question_type: string
  difficulty: string
  suggested_marks: number
}

export default function CreatePaper() {
  const navigate = useNavigate()
  const [questions, setQuestions] = useState<Question[]>([])
  const [selectedQuestions, setSelectedQuestions] = useState<number[]>([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  
  const [paperConfig, setPaperConfig] = useState({
    title: '',
    description: '',
    total_marks: 100,
    duration_minutes: 60,
    instructions: 'Read all questions carefully before answering.',
    institution_name: 'Your Institution',
  })

  useEffect(() => {
    loadQuestions()
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

  const toggleQuestion = (questionId: number) => {
    if (selectedQuestions.includes(questionId)) {
      setSelectedQuestions(selectedQuestions.filter((id) => id !== questionId))
    } else {
      setSelectedQuestions([...selectedQuestions, questionId])
    }
  }

  const handleCreate = async () => {
    if (!paperConfig.title) {
      alert('Please enter a title for the question paper')
      return
    }

    if (selectedQuestions.length === 0) {
      alert('Please select at least one question')
      return
    }

    setCreating(true)
    try {
      await papersAPI.create({
        ...paperConfig,
        question_ids: selectedQuestions,
      })
      
      alert('Question paper created successfully!')
      navigate('/papers')
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to create question paper')
    } finally {
      setCreating(false)
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
      <div className="flex items-center space-x-4">
        <button
          onClick={() => navigate('/papers')}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="h-6 w-6 text-gray-600" />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Create Question Paper</h1>
          <p className="text-gray-600 mt-2">Configure and select questions for your paper</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Paper Configuration</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  value={paperConfig.title}
                  onChange={(e) => setPaperConfig({ ...paperConfig, title: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
                  placeholder="Mid-term Exam 2024"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={paperConfig.description}
                  onChange={(e) => setPaperConfig({ ...paperConfig, description: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
                  rows={3}
                  placeholder="Optional description"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Total Marks
                </label>
                <input
                  type="number"
                  value={paperConfig.total_marks}
                  onChange={(e) => setPaperConfig({ ...paperConfig, total_marks: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Duration (minutes)
                </label>
                <input
                  type="number"
                  value={paperConfig.duration_minutes}
                  onChange={(e) => setPaperConfig({ ...paperConfig, duration_minutes: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Institution Name
                </label>
                <input
                  type="text"
                  value={paperConfig.institution_name}
                  onChange={(e) => setPaperConfig({ ...paperConfig, institution_name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
                />
              </div>

              <div className="pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Selected Questions</span>
                  <span className="text-lg font-bold text-primary">{selectedQuestions.length}</span>
                </div>
              </div>

              <button
                onClick={handleCreate}
                disabled={creating || selectedQuestions.length === 0}
                className="w-full px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {creating ? 'Creating...' : 'Create Paper'}
              </button>
            </div>
          </div>
        </div>

        {/* Questions Selection */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Select Questions</h2>
              <p className="text-sm text-gray-600 mt-1">Click on questions to add them to your paper</p>
            </div>

            {loading ? (
              <div className="p-8 text-center text-gray-500">Loading questions...</div>
            ) : questions.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                <p>No questions available. Please generate questions first.</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {questions.map((question) => {
                  const isSelected = selectedQuestions.includes(question.id)
                  
                  return (
                    <div
                      key={question.id}
                      onClick={() => toggleQuestion(question.id)}
                      className={`p-6 cursor-pointer transition-colors ${
                        isSelected ? 'bg-blue-50 border-l-4 border-primary' : 'hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex items-start">
                        <div className="flex-shrink-0 mt-1">
                          <CheckSquare
                            className={`h-5 w-5 ${
                              isSelected ? 'text-primary' : 'text-gray-300'
                            }`}
                          />
                        </div>
                        
                        <div className="ml-4 flex-1">
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
                          
                          <p className="text-gray-900">{question.question_text}</p>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
