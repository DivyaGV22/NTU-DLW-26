import React, { useState, useEffect } from 'react'
import { getDashboardData, createInteraction, updateRecommendationStatus } from '../services/api'
import LearningStateCard from './LearningStateCard'
import RecommendationsPanel from './RecommendationsPanel'
import AnalyticsCharts from './AnalyticsCharts'
import InteractionForm from './InteractionForm'
import './Dashboard.css'

function Dashboard({ studentId }) {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadDashboardData()
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000)
    return () => clearInterval(interval)
  }, [studentId])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const data = await getDashboardData(studentId)
      setDashboardData(data)
      setError(null)
    } catch (err) {
      setError('Failed to load dashboard data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateInteraction = async (interactionData) => {
    try {
      await createInteraction(studentId, interactionData)
      await loadDashboardData() // Refresh dashboard
    } catch (err) {
      alert('Failed to record interaction')
      console.error(err)
    }
  }

  const handleUpdateRecommendation = async (recommendationId, status) => {
    try {
      await updateRecommendationStatus(recommendationId, status)
      await loadDashboardData() // Refresh dashboard
    } catch (err) {
      console.error(err)
    }
  }

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    )
  }

  if (error || !dashboardData) {
    return (
      <div className="dashboard-error">
        <p>{error || 'No data available'}</p>
        <button onClick={loadDashboardData}>Retry</button>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard-grid">
        <div className="dashboard-main">
          <LearningStateCard learningState={dashboardData.learning_state} />
          
          <AnalyticsCharts
            interactions={dashboardData.interactions}
            learningState={dashboardData.learning_state}
          />

          <InteractionForm
            studentId={studentId}
            onCreateInteraction={handleCreateInteraction}
          />
        </div>

        <div className="dashboard-sidebar">
          <RecommendationsPanel
            recommendations={dashboardData.recommendations}
            onUpdateRecommendation={handleUpdateRecommendation}
          />
        </div>
      </div>
    </div>
  )
}

export default Dashboard

