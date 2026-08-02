import { askQuestion } from '../api'

export default function ChatPanel({
  message,
  setMessage,
  answer,
  upload,
  status,
  setStatus,
  setError,
  setAnswer,
}) {
  const handleAsk = async (e) => {
    e.preventDefault()
    if (!message.trim() || status === 'asking') return

    setStatus('asking')
    setAnswer(null)
    setError('')

    try {
      const data = await askQuestion(message)
      setAnswer(data)
      setStatus('idle')
      setMessage('')
    } catch (err) {
      setError(err.message)
      setStatus('idle')
    }
  }

  return (
    <div className="card">
      <form onSubmit={handleAsk}>
        <label htmlFor="chat-input">提问</label>
        <input
          id="chat-input"
          className="text-input"
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button
          type="submit"
          className={`btn${status === 'asking' ? ' loading' : ''}`}
          disabled={
            !upload ||
            !message.trim() ||
            status === 'uploading' ||
            status === 'asking'
          }
        >
          {status === 'asking' ? '思考中...' : 'Ask'}
        </button>
      </form>

      {answer && (
        <div className="answer-section">
          <p className="answer-text">{answer.answer}</p>
          <div className="citations-row">
            {answer.citations.map((page) => (
              <span key={page} className="page-chip">
                Page {page}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
