import React, { useState } from 'react'
import './StudentSelector.css'

function StudentSelector({ students, selectedStudentId, onSelectStudent, onCreateStudent }) {
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [creating, setCreating] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setCreating(true)
    try {
      await onCreateStudent(name, email)
      setName('')
      setEmail('')
      setShowCreateForm(false)
    } catch (error) {
      alert('Error creating student. Please try again.')
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="student-selector">
      <div className="selector-controls">
        <label>Select Student:</label>
        <select
          value={selectedStudentId || ''}
          onChange={(e) => onSelectStudent(Number(e.target.value))}
        >
          {students.map(student => (
            <option key={student.id} value={student.id}>
              {student.name} ({student.email})
            </option>
          ))}
        </select>
        <button
          className="btn-create"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : '+ New Student'}
        </button>
      </div>

      {showCreateForm && (
        <form className="create-student-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Student Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit" disabled={creating}>
            {creating ? 'Creating...' : 'Create Student'}
          </button>
        </form>
      )}
    </div>
  )
}

export default StudentSelector

