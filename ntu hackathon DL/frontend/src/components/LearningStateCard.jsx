import React from 'react'
import './LearningStateCard.css'

function LearningStateCard({ learningState }) {
  if (!learningState) return null

  const proficiency = learningState.overall_proficiency
  const engagement = learningState.engagement_level
  const riskLevel = learningState.risk_level
  const isActive = learningState.is_active

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'high': return '#e53e3e'
      case 'medium': return '#ed8936'
      case 'low': return '#48bb78'
      default: return '#718096'
    }
  }

  const getProficiencyColor = (value) => {
    if (value >= 0.8) return '#48bb78'
    if (value >= 0.6) return '#38b2ac'
    if (value >= 0.4) return '#ed8936'
    return '#e53e3e'
  }

  return (
    <div className="learning-state-card">
      <h2>Learning State Overview</h2>
      
      <div className="state-metrics">
        <div className="metric">
          <div className="metric-header">
            <span className="metric-label">Overall Proficiency</span>
            <span className="metric-value" style={{ color: getProficiencyColor(proficiency) }}>
              {(proficiency * 100).toFixed(0)}%
            </span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${proficiency * 100}%`,
                backgroundColor: getProficiencyColor(proficiency)
              }}
            />
          </div>
        </div>

        <div className="metric">
          <div className="metric-header">
            <span className="metric-label">Engagement Level</span>
            <span className="metric-value" style={{ color: getProficiencyColor(engagement) }}>
              {(engagement * 100).toFixed(0)}%
            </span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${engagement * 100}%`,
                backgroundColor: getProficiencyColor(engagement)
              }}
            />
          </div>
        </div>

        <div className="metric">
          <div className="metric-header">
            <span className="metric-label">Learning Velocity</span>
            <span className="metric-value">
              {learningState.learning_velocity > 0 ? '+' : ''}
              {(learningState.learning_velocity * 100).toFixed(1)}%
            </span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${Math.abs(learningState.learning_velocity) * 500}%`,
                backgroundColor: learningState.learning_velocity > 0 ? '#48bb78' : '#e53e3e',
                maxWidth: '100%'
              }}
            />
          </div>
        </div>

        <div className="metric">
          <div className="metric-header">
            <span className="metric-label">Consistency Score</span>
            <span className="metric-value">
              {(learningState.consistency_score * 100).toFixed(0)}%
            </span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${learningState.consistency_score * 100}%`,
                backgroundColor: '#667eea'
              }}
            />
          </div>
        </div>
      </div>

      <div className="state-indicators">
        <div className="indicator">
          <span className="indicator-label">Status:</span>
          <span className={`indicator-badge ${isActive ? 'active' : 'inactive'}`}>
            {isActive ? '✓ Active' : '○ Inactive'}
          </span>
        </div>
        <div className="indicator">
          <span className="indicator-label">Risk Level:</span>
          <span
            className="indicator-badge risk"
            style={{ backgroundColor: getRiskColor(riskLevel) }}
          >
            {riskLevel.toUpperCase()}
          </span>
        </div>
        {learningState.days_since_last_activity > 0 && (
          <div className="indicator">
            <span className="indicator-label">Days Since Last Activity:</span>
            <span className="indicator-value">{learningState.days_since_last_activity}</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default LearningStateCard

