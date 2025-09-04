import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
})

export const listNotes = () => api.get('/notes').then(r => r.data)
export const createNote = (data) => api.post('/notes', data).then(r => r.data)
export const updateNote = (id, data) => api.put(`/notes/${id}`, data).then(r => r.data)
export const deleteNote = (id) => api.delete(`/notes/${id}`).then(r => r.data)
export const shareNote = (id) => api.post(`/notes/${id}/share`).then(r => r.data)
export const fetchShared = (slug) => api.get(`/share/${slug}`).then(r => r.data)

export default api