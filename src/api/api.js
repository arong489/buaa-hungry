import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000/'

axios.defaults.withCredentials = true

axios.defaults.timeout = 20000

axios.interceptors.request.use((config) => {
  if (localStorage.getItem('token')) {
    config.headers.Authorization = localStorage.getItem('token')
  }
  return config
})

export default axios
