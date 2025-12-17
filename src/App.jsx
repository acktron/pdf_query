import React, { useState } from 'react'
import './App.css'

if (!window.BACKEND_URL) {
  window.BACKEND_URL = 'http://127.0.0.1:8000'
}

const BASE_URL = window.BACKEND_URL
const HEALTH_URL = `${BASE_URL}/debug-query-pdf`
const QUERY_URL = `${BASE_URL}/query-pdf`

function App() {
  const [file, setFile] = useState(null)
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState('')
  const [error, setError] = useState('')
  const [fileName, setFileName] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setFileName(selectedFile.name)
      setError('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!file || !question.trim()) {
      setError('Please select a PDF file and enter a question.')
      return
    }

    setLoading(true)
    setError('')
    setAnswer('')

    try {
      const healthResponse = await fetch(HEALTH_URL)
      if (!healthResponse.ok) {
        throw new Error('Backend not reachable. Check server URL/port.')
      }

      const formData = new FormData()
      formData.append('file', file)
      formData.append('question', question.trim())

      const response = await fetch(QUERY_URL, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({
          detail: `HTTP ${response.status}: ${response.statusText}`
        }))
        throw new Error(errorData.detail || 'An error occurred')
      }

      const data = await response.json()
      setAnswer(data.answer)
      
      if (data.context_truncated) {
        setAnswer(prev => prev + '\n\n(Note: PDF content was truncated due to length)')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">PDF Query System</h1>
        <p className="subtitle">Upload a PDF and ask questions about its content</p>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="pdfInput" className="label">
              Select PDF File
            </label>
            <div className="file-input-wrapper">
              <input
                type="file"
                id="pdfInput"
                accept=".pdf"
                onChange={handleFileChange}
                className="file-input"
                disabled={loading}
              />
              {fileName && (
                <span className="file-name">{fileName}</span>
              )}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="questionInput" className="label">
              Enter your question
            </label>
            <input
              type="text"
              id="questionInput"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="What would you like to know about this PDF?"
              className="text-input"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading || !file || !question.trim()}
            className="submit-btn"
          >
            {loading ? 'Processing...' : 'Submit Query'}
          </button>
        </form>

        {loading && (
          <div className="loader">
            <div className="spinner"></div>
            <p>Processing your request...</p>
          </div>
        )}

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {answer && (
          <div className="answer-box">
            <h2 className="answer-title">Answer</h2>
            <div className="answer-content">{answer}</div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

