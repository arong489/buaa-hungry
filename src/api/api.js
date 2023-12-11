import axios from 'axios'
import { Toast } from 'vant'

axios.defaults.baseURL = 'http://127.0.0.1:8000/'

axios.defaults.withCredentials = true

axios.defaults.timeout = 20000

axios.interceptors.request.use(
  (config) => {
    if (localStorage.getItem('token')) {
      config.headers.token = localStorage.getItem('token')
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    Toast.fail('请求异常')
    return Promise.reject(error)
  }
)

export default axios
