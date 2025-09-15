import React, { useState } from 'react'
import DatePicker from 'react-datepicker'
import { MapPin, Calendar, Search, AlertCircle } from 'lucide-react'
import { validateFormInputs, formatCoordinates } from '../utils/validation'
import "react-datepicker/dist/react-datepicker.css"

const WeatherForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: '',
    startDate: null,
    endDate: null
  })
  const [errors, setErrors] = useState({})

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null
      }))
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Validate form
    const validation = validateFormInputs(formData)
    
    if (!validation.isValid) {
      setErrors({ general: validation.error })
      return
    }
    
    // Clear errors and submit
    setErrors({})
    onSubmit({
      latitude: parseFloat(formData.latitude),
      longitude: parseFloat(formData.longitude),
      startDate: formData.startDate,
      endDate: formData.endDate
    })
  }

  const setPresetLocation = (name, lat, lng) => {
    setFormData(prev => ({
      ...prev,
      latitude: lat.toString(),
      longitude: lng.toString()
    }))
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-2 mb-6">
        <MapPin className="h-5 w-5 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-900">
          Weather Data Parameters
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Preset Locations */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quick Locations
          </label>
          <div className="flex flex-wrap gap-2">
            {[
              { name: 'New York', lat: 40.7128, lng: -74.0060 },
              { name: 'London', lat: 51.5074, lng: -0.1278 },
              { name: 'Tokyo', lat: 35.6762, lng: 139.6503 },
              { name: 'Sydney', lat: -33.8688, lng: 151.2093 }
            ].map((location) => (
              <button
                key={location.name}
                type="button"
                onClick={() => setPresetLocation(location.name, location.lat, location.lng)}
                className="btn-secondary text-xs"
              >
                {location.name}
              </button>
            ))}
          </div>
        </div>

        {/* Coordinates */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Latitude (-90 to 90)
            </label>
            <input
              type="number"
              step="any"
              value={formData.latitude}
              onChange={(e) => handleInputChange('latitude', e.target.value)}
              placeholder="e.g., 40.7128"
              className={`input-field ${errors.latitude ? 'border-red-500' : ''}`}
              required
            />
            {errors.latitude && (
              <p className="text-red-500 text-xs mt-1">{errors.latitude}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Longitude (-180 to 180)
            </label>
            <input
              type="number"
              step="any"
              value={formData.longitude}
              onChange={(e) => handleInputChange('longitude', e.target.value)}
              placeholder="e.g., -74.0060"
              className={`input-field ${errors.longitude ? 'border-red-500' : ''}`}
              required
            />
            {errors.longitude && (
              <p className="text-red-500 text-xs mt-1">{errors.longitude}</p>
            )}
          </div>
        </div>

        {/* Current coordinates display */}
        {formData.latitude && formData.longitude && (
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">
              <strong>Coordinates:</strong> {formatCoordinates(
                parseFloat(formData.latitude) || 0,
                parseFloat(formData.longitude) || 0
              )}
            </p>
          </div>
        )}

        {/* Date Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="inline h-4 w-4 mr-1" />
              Start Date
            </label>
            <DatePicker
              selected={formData.startDate}
              onChange={(date) => handleInputChange('startDate', date)}
              maxDate={new Date()}
              dateFormat="yyyy-MM-dd"
              placeholderText="Select start date"
              className="input-field w-full"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="inline h-4 w-4 mr-1" />
              End Date
            </label>
            <DatePicker
              selected={formData.endDate}
              onChange={(date) => handleInputChange('endDate', date)}
              minDate={formData.startDate}
              maxDate={new Date()}
              dateFormat="yyyy-MM-dd"
              placeholderText="Select end date"
              className="input-field w-full"
              required
            />
          </div>
        </div>

        {/* Error Display */}
        {errors.general && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <p className="text-red-700 text-sm">{errors.general}</p>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <div className="loading-spinner"></div>
              <span>Fetching Weather Data...</span>
            </>
          ) : (
            <>
              <Search className="h-4 w-4" />
              <span>Get Weather Data</span>
            </>
          )}
        </button>
      </form>
    </div>
  )
}

export default WeatherForm
