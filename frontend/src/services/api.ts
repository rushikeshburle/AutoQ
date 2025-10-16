import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (data: any) => api.post('/api/v1/auth/register', data),
  login: (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    return api.post('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  getCurrentUser: () => api.get('/api/v1/auth/me'),
}

// Documents API
export const documentsAPI = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/v1/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  process: (documentId: number) => api.post(`/api/v1/documents/${documentId}/process`),
  list: () => api.get('/api/v1/documents/'),
  get: (documentId: number) => api.get(`/api/v1/documents/${documentId}`),
  delete: (documentId: number) => api.delete(`/api/v1/documents/${documentId}`),
  getTopics: (documentId: number) => api.get(`/api/v1/documents/${documentId}/topics`),
}

// Questions API
export const questionsAPI = {
  generate: (data: any) => api.post('/api/v1/questions/generate', data),
  list: (params?: any) => api.get('/api/v1/questions/', { params }),
  get: (questionId: number) => api.get(`/api/v1/questions/${questionId}`),
  create: (data: any) => api.post('/api/v1/questions/', data),
  update: (questionId: number, data: any) => api.put(`/api/v1/questions/${questionId}`, data),
  delete: (questionId: number) => api.delete(`/api/v1/questions/${questionId}`),
}

// Question Papers API
export const papersAPI = {
  create: (data: any) => api.post('/api/v1/papers/', data),
  list: () => api.get('/api/v1/papers/'),
  get: (paperId: number) => api.get(`/api/v1/papers/${paperId}`),
  update: (paperId: number, data: any) => api.put(`/api/v1/papers/${paperId}`, data),
  delete: (paperId: number) => api.delete(`/api/v1/papers/${paperId}`),
  export: (paperId: number, format: string, includeAnswers: boolean) =>
    api.post(
      `/api/v1/papers/${paperId}/export`,
      { format, include_answers: includeAnswers },
      { responseType: 'blob' }
    ),
  publish: (paperId: number) => api.post(`/api/v1/papers/${paperId}/publish`),
}

export default api
