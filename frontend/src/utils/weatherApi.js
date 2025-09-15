import axios from 'axios'

const OPEN_METEO_BASE_URL = 'https://archive-api.open-meteo.com/v1/archive'

// Weather variables we need to fetch
const DAILY_VARIABLES = [
  'temperature_2m_max',
  'temperature_2m_min', 
  'temperature_2m_mean',
  'apparent_temperature_max',
  'apparent_temperature_min',
  'apparent_temperature_mean'
]

/**
 * Fetch weather data from Open-Meteo API
 * @param {number} latitude 
 * @param {number} longitude 
 * @param {string} startDate - YYYY-MM-DD format
 * @param {string} endDate - YYYY-MM-DD format
 * @returns {Promise<Object>} Weather data
 */
export const fetchWeatherData = async (latitude, longitude, startDate, endDate) => {
  try {
    const params = {
      latitude,
      longitude,
      start_date: startDate,
      end_date: endDate,
      daily: DAILY_VARIABLES.join(','),
      timezone: 'auto'
    }

    const response = await axios.get(OPEN_METEO_BASE_URL, { params })
    
    if (response.data && response.data.daily) {
      return {
        success: true,
        data: response.data,
        error: null
      }
    } else {
      throw new Error('Invalid response format from weather API')
    }
  } catch (error) {
    console.error('Weather API Error:', error)
    
    let errorMessage = 'Failed to fetch weather data'
    
    if (error.response) {
      // API responded with error status
      errorMessage = `API Error: ${error.response.status} - ${error.response.statusText}`
    } else if (error.request) {
      // Request was made but no response received
      errorMessage = 'Network error: Unable to reach weather service'
    } else {
      // Something else happened
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
 * Transform weather data for chart visualization
 * @param {Object} weatherData - Raw weather data from API
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
 * @param {Object} weatherData - Raw weather data from API
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
