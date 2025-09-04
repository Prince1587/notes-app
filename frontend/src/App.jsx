import React, { useEffect, useState } from 'react'
import { listNotes, createNote, updateNote, deleteNote, shareNote } from './api'

function NoteEditor({ initial, onSave, onCancel }) {
  const [title, setTitle] = useState(initial?.title || '')
  const [content, setContent] = useState(initial?.content || '')
  return (
    <div className="modal">
      <div className="card">
        <h3>{initial?.id ? 'Edit note' : 'New note'}</h3>
        <input
          className="input"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          className="textarea"
          placeholder="Write your note..."
          rows="8"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <div className="row">
          <button className="btn primary" onClick={() => onSave({ title, content })}>
            Save
          </button>
          <button className="btn" onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null)
  const [toast, setToast] = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const data = await listNotes()
      setNotes(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const save = async (payload) => {
    if (editing?.id) {
      const updated = await updateNote(editing.id, payload)
      setNotes((prev) => prev.map(n => n.id === updated.id ? updated : n))
    } else {
      const created = await createNote(payload)
      setNotes((prev) => [created, ...prev])
    }
    setEditing(null)
  }

  const destroy = async (id) => {
    if (!confirm('Delete this note?')) return
    await deleteNote(id)
    setNotes((prev) => prev.filter(n => n.id !== id))
  }

  const share = async (id) => {
    const res = await shareNote(id)
    await load()
    const url = res.share_url
    navigator.clipboard.writeText(url).catch(() => { })
    setToast(`Share link copied: ${url}`)
    setTimeout(() => setToast(null), 3000)
  }

  return (
    <div className="container">
      <header>
        <h1>Notes</h1>
        <button className="btn primary" onClick={() => setEditing({})}>+ New</button>
      </header>

      {loading ? <p>Loading...</p> : (
        notes.length === 0 ? <p>No notes yet. Create your first one!</p> : (
          <div className="grid">
            {notes.map(n => (
              <div className="card" key={n.id}>
                <div className="card-head">
                  <h3 className="title">{n.title}</h3>
                  <div className="spacer" />
                  <button className="icon" title="Share" onClick={() => share(n.id)}>🔗</button>
                  <button className="icon" title="Edit" onClick={() => setEditing(n)}>✏️</button>
                  <button className="icon" title="Delete" onClick={() => destroy(n.id)}>🗑️</button>
                </div>
                <p className="content">{n.content}</p>
                {n.share_url && <a className="share" href={n.share_url} target="_blank" rel="noreferrer">Public link</a>}
              </div>
            ))}
          </div>
        )
      )}

      {editing && <NoteEditor initial={editing} onSave={save} onCancel={() => setEditing(null)} />}
      {toast && <div className="toast">{toast}</div>}
    </div>
  )
}

export default App