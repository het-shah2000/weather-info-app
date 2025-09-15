import React, { useState, useMemo } from 'react'
import { ChevronLeft, ChevronRight, Table, Download } from 'lucide-react'

const WeatherTable = ({ data, title = "Weather Data" }) => {
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(10)

  const paginatedData = useMemo(() => {
    if (!data || !Array.isArray(data)) return []
    
    const startIndex = (currentPage - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    return data.slice(startIndex, endIndex)
  }, [data, currentPage, itemsPerPage])

  const totalPages = Math.ceil((data?.length || 0) / itemsPerPage)

  const handlePageChange = (newPage) => {
    setCurrentPage(Math.max(1, Math.min(newPage, totalPages)))
  }

  const exportToCSV = () => {
    if (!data || data.length === 0) return

    const headers = [
      'Date',
      'Max Temp (°C)',
      'Min Temp (°C)',
      'Mean Temp (°C)',
      'Max Apparent Temp (°C)',
      'Min Apparent Temp (°C)',
      'Mean Apparent Temp (°C)'
    ]

    const csvContent = [
      headers.join(','),
      ...data.map(row => [
        row.date,
        row.tempMax,
        row.tempMin,
        row.tempMean,
        row.apparentTempMax,
        row.apparentTempMin,
        row.apparentTempMean
      ].join(','))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `weather-data-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  if (!data || data.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center justify-center h-32 text-gray-500">
          <p>No table data available</p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Table className="h-5 w-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={exportToCSV}
            className="btn-secondary flex items-center space-x-1 text-xs"
          >
            <Download className="h-3 w-3" />
            <span>Export CSV</span>
          </button>
          
          <select
            value={itemsPerPage}
            onChange={(e) => {
              setItemsPerPage(Number(e.target.value))
              setCurrentPage(1)
            }}
            className="text-xs border border-gray-300 rounded px-2 py-1"
          >
            <option value={10}>10 per page</option>
            <option value={20}>20 per page</option>
            <option value={50}>50 per page</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Max Temp (°C)
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Min Temp (°C)
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Mean Temp (°C)
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Max App. Temp (°C)
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Min App. Temp (°C)
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Mean App. Temp (°C)
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.map((row, index) => (
              <tr key={row.id || index} className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  {row.date}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {typeof row.tempMax === 'number' ? row.tempMax.toFixed(1) : row.tempMax}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {typeof row.tempMin === 'number' ? row.tempMin.toFixed(1) : row.tempMin}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {typeof row.tempMean === 'number' ? row.tempMean.toFixed(1) : row.tempMean}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {typeof row.apparentTempMax === 'number' ? row.apparentTempMax.toFixed(1) : row.apparentTempMax}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {typeof row.apparentTempMin === 'number' ? row.apparentTempMin.toFixed(1) : row.apparentTempMin}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {typeof row.apparentTempMean === 'number' ? row.apparentTempMean.toFixed(1) : row.apparentTempMean}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
        <div className="text-sm text-gray-700">
          Showing {((currentPage - 1) * itemsPerPage) + 1} to {Math.min(currentPage * itemsPerPage, data.length)} of {data.length} entries
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className="p-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          
          <div className="flex items-center space-x-1">
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              let pageNum
              if (totalPages <= 5) {
                pageNum = i + 1
              } else if (currentPage <= 3) {
                pageNum = i + 1
              } else if (currentPage >= totalPages - 2) {
                pageNum = totalPages - 4 + i
              } else {
                pageNum = currentPage - 2 + i
              }
              
              return (
                <button
                  key={pageNum}
                  onClick={() => handlePageChange(pageNum)}
                  className={`px-3 py-1 rounded-lg text-sm ${
                    currentPage === pageNum
                      ? 'bg-primary-600 text-white'
                      : 'border border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {pageNum}
                </button>
              )
            })}
          </div>
          
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="p-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  )
}

export default WeatherTable
