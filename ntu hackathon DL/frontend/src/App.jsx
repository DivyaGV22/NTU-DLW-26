import React, { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import StudentSelector from './components/StudentSelector'
import { getStudents, createStudent } from './services/api'
import './App.css'

function App() {
  const [students, setStudents] = useState([])
  const [selectedStudentId, setSelectedStudentId] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStudents()
  }, [])

  const loadStudents = async () => {
    try {
      const data = await getStudents()
      setStudents(data)
      if (data.length > 0 && !selectedStudentId) {
        setSelectedStudentId(data[0].id)
      }
    } catch (error) {
      console.error('Error loading students:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateStudent = async (name, email) => {
    try {
      const newStudent = await createStudent({ name, email })
      setStudents([...students, newStudent])
      setSelectedStudentId(newStudent.id)
    } catch (error) {
      console.error('Error creating student:', error)
      throw error
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎓 Learning Analytics Dashboard</h1>
        <p>AI-Powered Personalized Learning Guidance</p>
      </header>
      
      <StudentSelector
        students={students}
        selectedStudentId={selectedStudentId}
        onSelectStudent={setSelectedStudentId}
        onCreateStudent={handleCreateStudent}
      />

      {selectedStudentId && (
        <Dashboard studentId={selectedStudentId} />
      )}
    </div>
  )
}

export default App

