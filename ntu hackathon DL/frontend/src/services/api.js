import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Student endpoints
export const getStudents = () => api.get('/students').then(res => res.data)
export const getStudent = (id) => api.get(`/students/${id}`).then(res => res.data)
export const createStudent = (data) => api.post('/students', data).then(res => res.data)

// Interaction endpoints
export const getInteractions = (studentId) => 
  api.get(`/students/${studentId}/interactions`).then(res => res.data)
export const createInteraction = (studentId, data) => 
  api.post(`/students/${studentId}/interactions`, data).then(res => res.data)

// Learning state endpoints
export const getLearningState = (studentId) => 
  api.get(`/students/${studentId}/state`).then(res => res.data)

// Recommendation endpoints
export const getRecommendations = (studentId) => 
  api.get(`/students/${studentId}/recommendations`).then(res => res.data)
export const updateRecommendationStatus = (recommendationId, status) => 
  api.put(`/recommendations/${recommendationId}/status?status=${status}`).then(res => res.data)

// Dashboard endpoint
export const getDashboardData = (studentId) => 
  api.get(`/students/${studentId}/dashboard`).then(res => res.data)

export default api

