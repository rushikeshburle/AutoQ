import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { documentsAPI, questionsAPI, papersAPI } from '../services/api'
import { FileText, BookOpen, FileQuestion, Plus, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const [stats, setStats] = useState({
    documents: 0,
    questions: 0,
    papers: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const [docsRes, questionsRes, papersRes] = await Promise.all([
        documentsAPI.list(),
        questionsAPI.list(),
        papersAPI.list(),
      ])

      setStats({
        documents: docsRes.data.length,
        questions: questionsRes.data.length,
        papers: papersRes.data.length,
      })
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Documents',
      value: stats.documents,
      icon: FileText,
      color: 'bg-blue-500',
      link: '/documents',
    },
    {
      title: 'Questions',
      value: stats.questions,
      icon: BookOpen,
      color: 'bg-green-500',
      link: '/questions',
    },
    {
      title: 'Question Papers',
      value: stats.papers,
      icon: FileQuestion,
      color: 'bg-purple-500',
      link: '/papers',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to AutoQ - Your Question Paper Generator</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((card) => {
          const Icon = card.icon
          return (
            <Link
              key={card.title}
              to={card.link}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{card.title}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {loading ? '...' : card.value}
                  </p>
                </div>
                <div className={`${card.color} rounded-full p-3`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </Link>
          )
        })}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/documents"
            className="flex items-center space-x-4 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-blue-50 transition-colors"
          >
            <div className="bg-primary rounded-lg p-3">
              <Plus className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Upload Document</h3>
              <p className="text-sm text-gray-600">Upload a PDF to get started</p>
            </div>
          </Link>

          <Link
            to="/papers/create"
            className="flex items-center space-x-4 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-blue-50 transition-colors"
          >
            <div className="bg-green-500 rounded-lg p-3">
              <FileQuestion className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Create Question Paper</h3>
              <p className="text-sm text-gray-600">Generate a new question paper</p>
            </div>
          </Link>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="h-5 w-5 mr-2 text-primary" />
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mb-3">
              1
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Upload PDF</h3>
            <p className="text-sm text-gray-600">Upload your lecture notes or textbook</p>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mb-3">
              2
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Process Document</h3>
            <p className="text-sm text-gray-600">AI extracts key concepts and topics</p>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mb-3">
              3
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Generate Questions</h3>
            <p className="text-sm text-gray-600">Create questions with one click</p>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mb-3">
              4
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Export Paper</h3>
            <p className="text-sm text-gray-600">Download as PDF or Word</p>
          </div>
        </div>
      </div>
    </div>
  )
}
