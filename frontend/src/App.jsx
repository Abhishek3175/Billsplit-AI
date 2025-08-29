import React, { useState } from 'react'
import './App.css'
import BillUpload from './components/BillUpload'
import BillDisplay from './components/BillDisplay'
import ShareCalculator from './components/ShareCalculator'

function App() {
  const [currentBill, setCurrentBill] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleBillProcessed = (billData) => {
    console.log('Bill processed successfully:', billData)  // Debug log
    setCurrentBill(billData)
    setError(null)
  }

  const handleError = (errorMessage) => {
    setError(errorMessage)
    setCurrentBill(null)
  }

  const resetApp = () => {
    setCurrentBill(null)
    setError(null)
    setLoading(false)
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🍽️ BillSplit AI</h1>
        <p>Smart bill splitting powered by AI</p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={resetApp} className="reset-btn">
              Try Again
            </button>
          </div>
        )}

        {!currentBill && !error && (
          <BillUpload 
            onBillProcessed={handleBillProcessed}
            onError={handleError}
            setLoading={setLoading}
            loading={loading}
          />
        )}

        {currentBill && (
          <div className="bill-workflow">
            <BillDisplay bill={currentBill} />
            <ShareCalculator 
              bill={currentBill}
              onReset={resetApp}
            />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by Google Gemini Vision</p>
      </footer>
    </div>
  )
}

export default App
