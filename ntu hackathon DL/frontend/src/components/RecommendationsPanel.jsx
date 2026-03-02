import React, { useState } from 'react'
import './RecommendationsPanel.css'

function RecommendationsPanel({ recommendations, onUpdateRecommendation }) {
  const [expandedId, setExpandedId] = useState(null)

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="recommendations-panel">
        <h2>Recommendations</h2>
        <div className="no-recommendations">
          <p>No recommendations at this time.</p>
          <p className="subtext">Keep learning to receive personalized guidance!</p>
        </div>
      </div>
    )
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return '#e53e3e'
      case 'high': return '#ed8936'
      case 'medium': return '#4299e1'
      case 'low': return '#48bb78'
      default: return '#718096'
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'study': return '📚'
      case 'practice': return '💪'
      case 'review': return '🔄'
      case 'break': return '☕'
      case 'accelerate': return '🚀'
      default: return '💡'
    }
  }

  const handleStatusUpdate = (id, status) => {
    onUpdateRecommendation(id, status)
  }

  return (
    <div className="recommendations-panel">
      <h2>Personalized Recommendations</h2>
      <p className="panel-subtitle">AI-powered guidance tailored to your learning</p>
      
      <div className="recommendations-list">
        {recommendations.map((rec) => {
          const isExpanded = expandedId === rec.id
          const actionItems = rec.action_items ? JSON.parse(rec.action_items) : []
          const supportingData = rec.supporting_data ? JSON.parse(rec.supporting_data) : {}

          return (
            <div
              key={rec.id}
              className={`recommendation-card priority-${rec.priority}`}
              style={{ borderLeftColor: getPriorityColor(rec.priority) }}
            >
              <div className="recommendation-header">
                <div className="recommendation-title-section">
                  <span className="recommendation-icon">{getTypeIcon(rec.recommendation_type)}</span>
                  <div>
                    <h3>{rec.title}</h3>
                    <span
                      className="priority-badge"
                      style={{ backgroundColor: getPriorityColor(rec.priority) }}
                    >
                      {rec.priority}
                    </span>
                  </div>
                </div>
                <button
                  className="expand-btn"
                  onClick={() => setExpandedId(isExpanded ? null : rec.id)}
                >
                  {isExpanded ? '−' : '+'}
                </button>
              </div>

              <p className="recommendation-description">{rec.description}</p>

              {rec.suggested_topic && (
                <div className="recommendation-meta">
                  <span className="meta-item">📖 Topic: {rec.suggested_topic}</span>
                  {rec.suggested_duration && (
                    <span className="meta-item">⏱️ {rec.suggested_duration} min</span>
                  )}
                </div>
              )}

              {isExpanded && (
                <div className="recommendation-details">
                  <div className="reasoning-section">
                    <h4>Why this recommendation?</h4>
                    <p>{rec.reasoning}</p>
                  </div>

                  {actionItems.length > 0 && (
                    <div className="action-items-section">
                      <h4>Action Items:</h4>
                      <ul>
                        {actionItems.map((item, idx) => (
                          <li key={idx}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {Object.keys(supportingData).length > 0 && (
                    <div className="supporting-data-section">
                      <h4>Supporting Data:</h4>
                      <div className="data-grid">
                        {Object.entries(supportingData).map(([key, value]) => (
                          <div key={key} className="data-item">
                            <span className="data-key">{key.replace(/_/g, ' ')}:</span>
                            <span className="data-value">
                              {typeof value === 'number' ? value.toFixed(2) : String(value)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="recommendation-actions">
                    <button
                      className="btn-action btn-view"
                      onClick={() => handleStatusUpdate(rec.id, 'viewed')}
                    >
                      Mark as Viewed
                    </button>
                    <button
                      className="btn-action btn-complete"
                      onClick={() => handleStatusUpdate(rec.id, 'completed')}
                    >
                      Mark as Completed
                    </button>
                    <button
                      className="btn-action btn-dismiss"
                      onClick={() => handleStatusUpdate(rec.id, 'dismissed')}
                    >
                      Dismiss
                    </button>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default RecommendationsPanel

