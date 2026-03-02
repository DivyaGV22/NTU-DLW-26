import React, { useState } from 'react'
import './InteractionForm.css'

function InteractionForm({ studentId, onCreateInteraction }) {
  const [formData, setFormData] = useState({
    interaction_type: 'study',
    topic: '',
    duration_minutes: 30,
    score: '',
    difficulty_level: 'medium',
    engagement_score: 0.5
  })
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    
    try {
      const interactionData = {
        ...formData,
        score: formData.score ? parseFloat(formData.score) : null,
        duration_minutes: parseFloat(formData.duration_minutes),
        engagement_score: parseFloat(formData.engagement_score)
      }
      
      await onCreateInteraction(interactionData)
      
      // Reset form
      setFormData({
        interaction_type: 'study',
        topic: '',
        duration_minutes: 30,
        score: '',
        difficulty_level: 'medium',
        engagement_score: 0.5
      })
      
      alert('Interaction recorded successfully!')
    } catch (error) {
      alert('Failed to record interaction')
      console.error(error)
    } finally {
      setSubmitting(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return (
    <div className="interaction-form-card">
      <h2>Record Learning Activity</h2>
      <p className="form-subtitle">Track your learning interactions to get better insights</p>
      
      <form onSubmit={handleSubmit} className="interaction-form">
        <div className="form-row">
          <div className="form-group">
            <label>Activity Type</label>
            <select
              name="interaction_type"
              value={formData.interaction_type}
              onChange={handleChange}
              required
            >
              <option value="study">Study</option>
              <option value="quiz">Quiz</option>
              <option value="assignment">Assignment</option>
              <option value="video">Video</option>
              <option value="reading">Reading</option>
            </select>
          </div>

          <div className="form-group">
            <label>Topic</label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              placeholder="e.g., Mathematics, Physics"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Duration (minutes)</label>
            <input
              type="number"
              name="duration_minutes"
              value={formData.duration_minutes}
              onChange={handleChange}
              min="0"
              step="1"
              required
            />
          </div>

          <div className="form-group">
            <label>Score (0-1, optional)</label>
            <input
              type="number"
              name="score"
              value={formData.score}
              onChange={handleChange}
              min="0"
              max="1"
              step="0.01"
              placeholder="0.0 - 1.0"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Difficulty Level</label>
            <select
              name="difficulty_level"
              value={formData.difficulty_level}
              onChange={handleChange}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="form-group">
            <label>Engagement Score (0-1)</label>
            <input
              type="range"
              name="engagement_score"
              value={formData.engagement_score}
              onChange={handleChange}
              min="0"
              max="1"
              step="0.1"
            />
            <span className="range-value">{(formData.engagement_score * 100).toFixed(0)}%</span>
          </div>
        </div>

        <button type="submit" className="submit-btn" disabled={submitting}>
          {submitting ? 'Recording...' : 'Record Activity'}
        </button>
      </form>
    </div>
  )
}

export default InteractionForm

