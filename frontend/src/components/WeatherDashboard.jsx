import React, { useState } from 'react'
import WeatherForm from './WeatherForm'
import WeatherChart from './WeatherChart'
import WeatherTable from './WeatherTable'
import { storeWeatherData, getWeatherFileContent, transformDataForChart, transformDataForTable } from '../utils/backendApi'
import { AlertCircle, CheckCircle, Info } from 'lucide-react'

const WeatherDashboard = () => {
  const [loading, setLoading] = useState(false)
  const [weatherData, setWeatherData] = useState(null)
  const [chartData, setChartData] = useState(null)
  const [tableData, setTableData] = useState([])
  const [error, setError] = useState(null)
  const [lastQuery, setLastQuery] = useState(null)

  const handleFormSubmit = async (formData) => {
    setLoading(true)
    setError(null)
    
    try {
      const { latitude, longitude, startDate, endDate } = formData
      
      // Format dates for API
      const startDateStr = startDate.toISOString().split('T')[0]
      const endDateStr = endDate.toISOString().split('T')[0]
      
      // Store weather data using backend service
      const storeResult = await storeWeatherData(latitude, longitude, startDateStr, endDateStr)
      
      if (storeResult.success) {
        // Get the filename from the store response
        const filename = storeResult.data.filename
        
        // Fetch the stored weather data content
        const contentResult = await getWeatherFileContent(filename)
        
        if (contentResult.success) {
          setWeatherData(contentResult.data)
          setChartData(transformDataForChart(contentResult.data))
          setTableData(transformDataForTable(contentResult.data))
          setLastQuery({
            latitude,
            longitude,
            startDate: startDateStr,
            endDate: endDateStr,
            location: `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`,
            filename: filename
          })
        } else {
          setError(contentResult.error)
          setWeatherData(null)
          setChartData(null)
          setTableData([])
        }
      } else {
        setError(storeResult.error)
        setWeatherData(null)
        setChartData(null)
        setTableData([])
      }
    } catch (err) {
      setError('An unexpected error occurred while fetching weather data')
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Form Section */}
      <WeatherForm onSubmit={handleFormSubmit} loading={loading} />
      
      {/* Status Messages */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 animate-fade-in">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
            <div>
              <h4 className="text-red-800 font-medium">Error</h4>
              <p className="text-red-700 text-sm mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {lastQuery && !loading && !error && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 animate-fade-in">
          <div className="flex items-center space-x-2">
            <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
            <div>
              <h4 className="text-green-800 font-medium">Data Stored & Loaded Successfully</h4>
              <p className="text-green-700 text-sm mt-1">
                Weather data for {lastQuery.location} from {lastQuery.startDate} to {lastQuery.endDate}
                {lastQuery.filename && <span className="block text-xs mt-1">Stored as: {lastQuery.filename}</span>}
              </p>
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 animate-fade-in">
          <div className="flex items-center space-x-2">
            <div className="loading-spinner"></div>
            <div>
              <h4 className="text-blue-800 font-medium">Processing Weather Data</h4>
              <p className="text-blue-700 text-sm mt-1">
                Storing weather data to cloud storage and preparing visualization...
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Data Visualization Section */}
      {chartData && !loading && (
        <div className="space-y-6 animate-slide-up">
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="card text-center">
              <h4 className="text-sm font-medium text-gray-600 mb-2">Total Days</h4>
              <p className="text-2xl font-bold text-primary-600">{tableData.length}</p>
            </div>
            <div className="card text-center">
              <h4 className="text-sm font-medium text-gray-600 mb-2">Avg Max Temp</h4>
              <p className="text-2xl font-bold text-red-500">
                {tableData.length > 0 
                  ? (tableData.reduce((sum, row) => sum + (typeof row.tempMax === 'number' ? row.tempMax : 0), 0) / tableData.length).toFixed(1)
                  : 'N/A'
                }°C
              </p>
            </div>
            <div className="card text-center">
              <h4 className="text-sm font-medium text-gray-600 mb-2">Avg Min Temp</h4>
              <p className="text-2xl font-bold text-blue-500">
                {tableData.length > 0 
                  ? (tableData.reduce((sum, row) => sum + (typeof row.tempMin === 'number' ? row.tempMin : 0), 0) / tableData.length).toFixed(1)
                  : 'N/A'
                }°C
              </p>
            </div>
          </div>

          {/* Chart */}
          <WeatherChart 
            data={chartData} 
            title={`Temperature Trends - ${lastQuery?.location || 'Location'}`}
          />
          
          {/* Table */}
          <WeatherTable 
            data={tableData}
            title={`Detailed Weather Data (${tableData.length} days)`}
          />
        </div>
      )}

      {/* Help Section */}
      {!weatherData && !loading && !error && (
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-start space-x-3">
            <Info className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-blue-800 font-medium mb-2">How to use this dashboard</h4>
              <ul className="text-blue-700 text-sm space-y-1">
                <li>• Enter valid latitude (-90 to 90) and longitude (-180 to 180) coordinates</li>
                <li>• Select a date range (up to 2 years, historical data only)</li>
                <li>• Click "Get Weather Data" to fetch and visualize the information</li>
                <li>• Use the chart to see temperature trends over time</li>
                <li>• Browse detailed data in the paginated table below</li>
                <li>• Export data as CSV for further analysis</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default WeatherDashboard
