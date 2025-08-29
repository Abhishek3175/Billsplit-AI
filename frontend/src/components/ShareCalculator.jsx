import React, { useState } from 'react'
import axios from 'axios'
import './ShareCalculator.css'

const ShareCalculator = ({ bill, onReset }) => {
  console.log('ShareCalculator rendering with bill:', bill)  // Debug log
  
  const [selectedItems, setSelectedItems] = useState([])
  const [calculation, setCalculation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleItemToggle = (item, index) => {
    setSelectedItems(prev => {
      const existingIndex = prev.findIndex(selected => 
        selected.name === item.name && selected.quantity === item.quantity
      )
      
      if (existingIndex >= 0) {
        // Remove item
        return prev.filter((_, i) => i !== existingIndex)
      } else {
        // Add item
        return [...prev, { ...item, originalIndex: index }]
      }
    })
    
    // Clear previous calculation
    setCalculation(null)
    setError(null)
  }

  const isItemSelected = (item) => {
    return selectedItems.some(selected => 
      selected.name === item.name && selected.quantity === item.quantity
    )
  }

  const calculateShare = async () => {
    if (selectedItems.length === 0) {
      setError('Please select at least one item')
      return
    }

    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post('/api/calculate-share', {
        bill_id: bill.bill_id,
        consumed_items: selectedItems
      })

      setCalculation(response.data)
    } catch (error) {
      console.error('Calculation error:', error)
      if (error.response?.data?.error) {
        setError(error.response.data.error)
      } else {
        setError('Failed to calculate share. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (amount, currency = 'USD') => {
    // Format amount with rupee symbol (₹) instead of dollar sign
    const formattedAmount = new Intl.NumberFormat('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount)
    
    return `₹${formattedAmount}`
  }

  return (
    <div className="share-calculator">
      <div className="calculator-header">
        <h2>💰 Calculate Your Share</h2>
        <p>Select the items you consumed:</p>
      </div>

      <div className="items-selection">
        {bill.items && bill.items.map((item, index) => (
          <div 
            key={index} 
            className={`item-selector ${isItemSelected(item) ? 'selected' : ''}`}
            onClick={() => handleItemToggle(item, index)}
          >
            <div className="item-info">
              <span className="item-name">{item.name}</span>
              <span className="item-quantity">×{item.quantity}</span>
              <span className="item-price">
                {formatCurrency(item.price * item.quantity, bill.currency)}
              </span>
            </div>
            <div className="selection-indicator">
              {isItemSelected(item) ? '✓' : '○'}
            </div>
          </div>
        ))}
      </div>

      {selectedItems.length > 0 && (
        <div className="selected-summary">
          <h3>Selected Items ({selectedItems.length})</h3>
          <div className="selected-items-list">
            {selectedItems.map((item, index) => (
              <div key={index} className="selected-item">
                <span>{item.name} ×{item.quantity}</span>
                <span>{formatCurrency(item.price * item.quantity, bill.currency)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="calculator-actions">
        <button
          className="calculate-btn"
          onClick={calculateShare}
          disabled={selectedItems.length === 0 || loading}
        >
          {loading ? 'Calculating...' : 'Calculate My Share'}
        </button>
        
        <button className="reset-btn" onClick={onReset}>
          Start Over
        </button>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {calculation && (
        <div className="calculation-result">
          <h3>Your Share Breakdown</h3>
          <div className="result-details">
            <div className="result-row">
              <span>Items Subtotal:</span>
              <span>{formatCurrency(calculation.user_subtotal, calculation.currency)}</span>
            </div>
            <div className="result-row">
              <span>Tax Share:</span>
              <span>{formatCurrency(calculation.user_tax_share, calculation.currency)}</span>
            </div>
            <div className="result-row total">
              <span>Your Total:</span>
              <span>{formatCurrency(calculation.user_total, calculation.currency)}</span>
            </div>
          </div>
          <div className="bill-context">
            <p>Bill Total: {formatCurrency(calculation.bill_total, calculation.currency)}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ShareCalculator
