import React, { useState } from 'react'
import axios from 'axios'
import './BillUpload.css'

const BillUpload = ({ onBillProcessed, onError, setLoading, loading }) => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        onError('Please select an image file (JPEG, PNG, etc.)')
        return
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        onError('File size must be less than 10MB')
        return
      }

      setSelectedFile(file)
      
      // Create preview URL
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      onError('Please select a file first')
      return
    }

    setLoading(true)
    
    try {
      const formData = new FormData()
      formData.append('image', selectedFile)

      const response = await axios.post('/api/upload-bill', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (response.data.success) {
        onBillProcessed({
          ...response.data.data,
          bill_id: response.data.bill_id
        })
      } else {
        onError(response.data.error || 'Failed to process bill')
      }
    } catch (error) {
      console.error('Upload error:', error)
      if (error.response?.data?.error) {
        onError(error.response.data.error)
      } else {
        onError('Failed to upload bill. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      if (file.type.startsWith('image/')) {
        setSelectedFile(file)
        const url = URL.createObjectURL(file)
        setPreviewUrl(url)
      }
    }
  }

  return (
    <div className="bill-upload">
      <div className="upload-container">
        <h2>Upload Your Bill</h2>
        <p>Take a photo or upload an image of your restaurant bill</p>
        
        <div 
          className="file-drop-zone"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          {previewUrl ? (
            <div className="image-preview">
              <img src={previewUrl} alt="Bill preview" />
              <button 
                className="remove-image"
                onClick={() => {
                  setSelectedFile(null)
                  setPreviewUrl(null)
                }}
              >
                ✕
              </button>
            </div>
          ) : (
            <div className="upload-placeholder">
              <div className="upload-icon">📷</div>
              <p>Drag & drop your bill image here</p>
              <p>or click to browse</p>
            </div>
          )}
          
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="file-input"
            id="file-input"
          />
          <label htmlFor="file-input" className="file-input-label">
            Choose File
          </label>
        </div>

        {selectedFile && (
          <div className="file-info">
            <p>Selected: {selectedFile.name}</p>
            <p>Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        )}

        <button
          className="upload-btn"
          onClick={handleUpload}
          disabled={!selectedFile || loading}
        >
          {loading ? 'Processing...' : 'Process Bill'}
        </button>

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>AI is analyzing your bill...</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default BillUpload
