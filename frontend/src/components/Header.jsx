import React from 'react'
import { Cloud, Sun, CloudRain } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1">
              <Sun className="h-8 w-8 text-yellow-500" />
              <Cloud className="h-6 w-6 text-blue-500" />
              <CloudRain className="h-7 w-7 text-blue-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gradient">
                Weather Dashboard
              </h1>
              <p className="text-gray-600 text-sm">
                Historical weather data visualization
              </p>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-gray-500">Powered by</p>
              <p className="text-sm font-medium text-gray-700">Open-Meteo API</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
