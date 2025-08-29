import React from 'react'
import './BillDisplay.css'

const BillDisplay = ({ bill }) => {
  console.log('BillDisplay rendering with bill:', bill)  // Debug log
  
  const formatCurrency = (amount, currency = 'USD') => {
    // Format amount with rupee symbol (₹) instead of dollar sign
    const formattedAmount = new Intl.NumberFormat('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount)
    
    return `₹${formattedAmount}`
  }

  return (
    <div className="bill-display">
      <div className="bill-header">
        <h2>📋 Bill Details</h2>
        {bill?.vendor && (
          <div className="vendor-info">
            <h3>{bill.vendor}</h3>
            {bill?.bill_date && <p className="bill-date">Date: {bill.bill_date}</p>}
          </div>
        )}
      </div>

      <div className="bill-items">
        <h3>Items</h3>
        <div className="items-list">
          {bill?.items && bill.items.length > 0 ? (
            bill.items.map((item, index) => (
              <div key={index} className="item-row">
                <div className="item-details">
                  <span className="item-name">{item?.name || 'Unknown Item'}</span>
                  {item?.quantity > 1 && (
                    <span className="item-quantity">×{item.quantity}</span>
                  )}
                </div>
                <span className="item-price">
                  {formatCurrency((item?.price || 0) * (item?.quantity || 1), bill?.currency)}
                </span>
              </div>
            ))
          ) : (
            <p>No items found</p>
          )}
        </div>
      </div>

      <div className="bill-summary">
        <div className="summary-row">
          <span>Subtotal:</span>
          <span>{formatCurrency(bill?.subtotal || 0, bill?.currency)}</span>
        </div>
        <div className="summary-row">
          <span>Tax:</span>
          <span>{formatCurrency(bill?.tax || 0, bill?.currency)}</span>
        </div>
        <div className="summary-row total">
          <span>Total:</span>
          <span>{formatCurrency(bill?.total || 0, bill?.currency)}</span>
        </div>
      </div>
    </div>
  )
}

export default BillDisplay
