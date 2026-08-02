import { useState } from 'react'
import PdfUploader from './components/PdfUploader'
import ChatPanel from './components/ChatPanel'

function App() {
  const [file, setFile] = useState(null)
  const [upload, setUpload] = useState(null)
  const [message, setMessage] = useState('')
  const [answer, setAnswer] = useState(null)
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')

  return (
    <div className="container">
      <div className="header">
        <h1>SmartLearn</h1>
        <p>Your AI-powered learning assistant</p>
      </div>

      {error && (
        <div role="alert" className="error-alert">
          {error}
        </div>
      )}

      <PdfUploader
        file={file}
        setFile={setFile}
        upload={upload}
        status={status}
        setStatus={setStatus}
        setError={setError}
        setUpload={setUpload}
        setAnswer={setAnswer}
      />

      <ChatPanel
        message={message}
        setMessage={setMessage}
        answer={answer}
        upload={upload}
        status={status}
        setStatus={setStatus}
        setError={setError}
        setAnswer={setAnswer}
      />
    </div>
  )
}

export default App
