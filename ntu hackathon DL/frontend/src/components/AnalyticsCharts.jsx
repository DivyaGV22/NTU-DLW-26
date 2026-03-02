import React from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { format, parseISO, subDays } from 'date-fns'
import './AnalyticsCharts.css'

function AnalyticsCharts({ interactions, learningState }) {
  if (!interactions || interactions.length === 0) {
    return (
      <div className="analytics-charts">
        <div className="no-data">
          <p>No interaction data available yet.</p>
          <p className="subtext">Start learning to see your analytics!</p>
        </div>
      </div>
    )
  }

  // Process data for score trend chart
  const scoreData = interactions
    .filter(i => i.score !== null)
    .map(i => ({
      date: format(parseISO(i.timestamp), 'MMM dd'),
      score: i.score * 100,
      timestamp: i.timestamp
    }))
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
    .slice(-20) // Last 20 interactions

  // Process data for topic distribution
  const topicCounts = {}
  interactions.forEach(i => {
    topicCounts[i.topic] = (topicCounts[i.topic] || 0) + 1
  })
  const topicData = Object.entries(topicCounts)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 5)

  // Process data for study time over time
  const timeData = interactions
    .reduce((acc, i) => {
      const date = format(parseISO(i.timestamp), 'MMM dd')
      if (!acc[date]) {
        acc[date] = 0
      }
      acc[date] += i.duration_minutes || 0
      return acc
    }, {})
  
  const timeChartData = Object.entries(timeData)
    .map(([date, minutes]) => ({ date, minutes: Math.round(minutes) }))
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(-14) // Last 14 days

  // Topic proficiencies pie chart
  const topicProficiencies = learningState?.topic_proficiencies 
    ? JSON.parse(learningState.topic_proficiencies)
    : {}
  
  const proficiencyData = Object.entries(topicProficiencies)
    .map(([name, value]) => ({ name, value: Math.round(value * 100) }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 6)

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#48bb78']

  return (
    <div className="analytics-charts">
      <h2>Learning Analytics</h2>
      
      <div className="charts-grid">
        {scoreData.length > 0 && (
          <div className="chart-card">
            <h3>Score Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#667eea"
                  strokeWidth={2}
                  name="Score (%)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {topicData.length > 0 && (
          <div className="chart-card">
            <h3>Topic Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topicData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#764ba2" name="Interactions" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {timeChartData.length > 0 && (
          <div className="chart-card">
            <h3>Study Time (Last 14 Days)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={timeChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="minutes" fill="#48bb78" name="Minutes" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {proficiencyData.length > 0 && (
          <div className="chart-card">
            <h3>Topic Proficiencies</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={proficiencyData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {proficiencyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}

export default AnalyticsCharts

