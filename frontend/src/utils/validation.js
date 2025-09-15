/**
 * Validation utilities for weather dashboard inputs
 */

/**
 * Validate latitude value
 * @param {number|string} latitude 
 * @returns {Object} Validation result
 */
export const validateLatitude = (latitude) => {
  const lat = parseFloat(latitude)
  
  if (isNaN(lat)) {
    return { isValid: false, error: 'Latitude must be a valid number' }
  }
  
  if (lat < -90 || lat > 90) {
    return { isValid: false, error: 'Latitude must be between -90 and 90 degrees' }
  }
  
  return { isValid: true, error: null }
}

/**
 * Validate longitude value
 * @param {number|string} longitude 
 * @returns {Object} Validation result
 */
export const validateLongitude = (longitude) => {
  const lng = parseFloat(longitude)
  
  if (isNaN(lng)) {
    return { isValid: false, error: 'Longitude must be a valid number' }
  }
  
  if (lng < -180 || lng > 180) {
    return { isValid: false, error: 'Longitude must be between -180 and 180 degrees' }
  }
  
  return { isValid: true, error: null }
}

/**
 * Validate date range
 * @param {Date} startDate 
 * @param {Date} endDate 
 * @returns {Object} Validation result
 */
export const validateDateRange = (startDate, endDate) => {
  if (!startDate || !endDate) {
    return { isValid: false, error: 'Both start and end dates are required' }
  }
  
  if (startDate > endDate) {
    return { isValid: false, error: 'Start date must be before or equal to end date' }
  }
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  if (endDate > today) {
    return { isValid: false, error: 'End date cannot be in the future' }
  }
  
  // Check if date range is too large (more than 2 years)
  const diffTime = Math.abs(endDate - startDate)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays > 730) {
    return { isValid: false, error: 'Date range cannot exceed 2 years' }
  }
  
  return { isValid: true, error: null }
}

/**
 * Validate all form inputs
 * @param {Object} formData 
 * @returns {Object} Validation result
 */
export const validateFormInputs = (formData) => {
  const { latitude, longitude, startDate, endDate } = formData
  
  // Validate latitude
  const latValidation = validateLatitude(latitude)
  if (!latValidation.isValid) {
    return latValidation
  }
  
  // Validate longitude
  const lngValidation = validateLongitude(longitude)
  if (!lngValidation.isValid) {
    return lngValidation
  }
  
  // Validate date range
  const dateValidation = validateDateRange(startDate, endDate)
  if (!dateValidation.isValid) {
    return dateValidation
  }
  
  return { isValid: true, error: null }
}

/**
 * Format coordinates for display
 * @param {number} lat 
 * @param {number} lng 
 * @returns {string} Formatted coordinates
 */
export const formatCoordinates = (lat, lng) => {
  const latDir = lat >= 0 ? 'N' : 'S'
  const lngDir = lng >= 0 ? 'E' : 'W'
  
  return `${Math.abs(lat).toFixed(4)}°${latDir}, ${Math.abs(lng).toFixed(4)}°${lngDir}`
}
