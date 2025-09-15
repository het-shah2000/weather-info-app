import axios from 'axios'

// Backend API configuration
const BACKEND_BASE_URL = 'https://weather-backend-service-383254662062.us-central1.run.app'

// Create axios instance with default config
const api = axios.create({
  baseURL: BACKEND_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

/**
 * Store weather data using our backend service
 * @param {number} latitude 
 * @param {number} longitude 
 * @param {string} startDate - YYYY-MM-DD format
 * @param {string} endDate - YYYY-MM-DD format
 * @returns {Promise<Object>} Response from backend
 */
export const storeWeatherData = async (latitude, longitude, startDate, endDate) => {
  try {
    const response = await api.post('/weather/store-weather-data', {
      latitude,
      longitude,
      start_date: startDate,
      end_date: endDate
    })

    return {
      success: true,
      data: response.data,
      error: null
    }
  } catch (error) {
    console.error('Backend API Error:', error)
    
    let errorMessage = 'Failed to store weather data'
    
    if (error.response) {
      errorMessage = `API Error: ${error.response.status} - ${error.response.data?.error || error.response.statusText}`
    } else if (error.request) {
      errorMessage = 'Network error: Unable to reach backend service'
    } else {
      errorMessage = error.message || 'Unknown error occurred'
    }

    return {
      success: false,
      data: null,
      error: errorMessage
    }
  }
}

/**
 * List all stored weather files
 * @returns {Promise<Object>} List of weather files
 */
export const listWeatherFiles = async () => {
  try {
    const response = await api.get('/weather/list-weather-files')

    return {
      success: true,
      data: response.data,
      error: null
    }
  } catch (error) {
    console.error('Backend API Error:', error)
    
    let errorMessage = 'Failed to fetch weather files'
    
    if (error.response) {
      errorMessage = `API Error: ${error.response.status} - ${error.response.data?.error || error.response.statusText}`
    } else if (error.request) {
      errorMessage = 'Network error: Unable to reach backend service'
    } else {
      errorMessage = error.message || 'Unknown error occurred'
    }

    return {
      success: false,
      data: null,
      error: errorMessage
    }
  }
}

/**
 * Get weather file content by filename
 * @param {string} filename - Name of the weather file
 * @returns {Promise<Object>} Weather file content
 */
export const getWeatherFileContent = async (filename) => {
  try {
    const response = await api.get(`/weather/weather-file-content/${filename}`)

    return {
      success: true,
      data: response.data,
      error: null
    }
  } catch (error) {
    console.error('Backend API Error:', error)
    
    let errorMessage = 'Failed to fetch weather file content'
    
    if (error.response) {
      errorMessage = `API Error: ${error.response.status} - ${error.response.data?.error || error.response.statusText}`
    } else if (error.request) {
      errorMessage = 'Network error: Unable to reach backend service'
    } else {
      errorMessage = error.message || 'Unknown error occurred'
    }

    return {
      success: false,
      data: null,
      error: errorMessage
    }
  }
}

/**
 * Check backend service health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')

    return {
      success: true,
      data: response.data,
      error: null
    }
  } catch (error) {
    console.error('Backend Health Check Error:', error)
    
    return {
      success: false,
      data: null,
      error: 'Backend service is unavailable'
    }
  }
}

/**
 * Transform weather data for chart visualization
 * @param {Object} weatherData - Raw weather data from backend
 * @returns {Object} Transformed data for charts
 */
export const transformDataForChart = (weatherData) => {
  if (!weatherData || !weatherData.daily) {
    return null
  }

  const { daily } = weatherData
  const dates = daily.time || []

  return {
    labels: dates,
    datasets: [
      {
        label: 'Max Temperature (°C)',
        data: daily.temperature_2m_max || [],
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4
      },
      {
        label: 'Min Temperature (°C)',
        data: daily.temperature_2m_min || [],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4
      },
      {
        label: 'Mean Temperature (°C)',
        data: daily.temperature_2m_mean || [],
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4
      }
    ]
  }
}

/**
 * Transform weather data for table display
 * @param {Object} weatherData - Raw weather data from backend
 * @returns {Array} Array of table rows
 */
export const transformDataForTable = (weatherData) => {
  if (!weatherData || !weatherData.daily) {
    return []
  }

  const { daily } = weatherData
  const dates = daily.time || []

  return dates.map((date, index) => ({
    id: index + 1,
    date,
    tempMax: daily.temperature_2m_max?.[index] ?? 'N/A',
    tempMin: daily.temperature_2m_min?.[index] ?? 'N/A',
    tempMean: daily.temperature_2m_mean?.[index] ?? 'N/A',
    apparentTempMax: daily.apparent_temperature_max?.[index] ?? 'N/A',
    apparentTempMin: daily.apparent_temperature_min?.[index] ?? 'N/A',
    apparentTempMean: daily.apparent_temperature_mean?.[index] ?? 'N/A'
  }))
}
