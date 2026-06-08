import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

export default {
  getProfile: () => api.get('/profile'),
  getProjects: () => api.get('/projects'),
  getArticles: () => api.get('/articles'),
  getLife: () => api.get('/life'),
  getFriends: () => api.get('/friends'),
  submitContact: (data) => api.post('/contact', data),
}
