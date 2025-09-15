import React, { useState } from 'react'
import WeatherDashboard from './components/WeatherDashboard'
import Header from './components/Header'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <WeatherDashboard />
      </main>
    </div>
  )
}

export default App
