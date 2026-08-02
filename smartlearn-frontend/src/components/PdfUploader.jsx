import { uploadPDF } from '../api'

export default function PdfUploader({
  file,
  setFile,
  upload,
  status,
  setStatus,
  setError,
  setUpload,
  setAnswer,
}) {
  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a PDF file')
      return
    }

    setStatus('uploading')
    setError('')
    setUpload(null)
    setAnswer(null)

    try {
      const data = await uploadPDF(file)
      setUpload(data)
      setStatus('idle')
    } catch (err) {
      setError(err.message)
      setStatus('idle')
    }
  }

  return (
    <div className="card">
      <form onSubmit={handleUpload}>
        <label htmlFor="file-upload">选择 PDF</label>
        <input
          id="file-upload"
          className="file-input"
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button
          type="submit"
          className={`btn${status === 'uploading' ? ' loading' : ''}`}
          disabled={!file || status === 'uploading' || status === 'asking'}
        >
          {status === 'uploading' ? '上传中...' : 'Upload'}
        </button>
      </form>

      {upload && (
        <p className="success-badge">
          ✅ 已上传，共 {upload.page_count} 页，{upload.character_count} 字符
        </p>
      )}
    </div>
  )
}
