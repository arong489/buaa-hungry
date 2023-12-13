import axios from 'axios'
import { Toast } from 'vant'
import router from '@/router'

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
    Toast.fail('请求异常')
    // console.log(error)
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  response => {
    if (response.data.status === -2) {
      Toast.fail({
        message: '登录过期',
        forbidClick: true
      })
      router.push('/login')
    }
    return response
  },
  error => {
    Toast.fail('请求异常')
    // console.log(error)
    return Promise.reject(error)
  }
)

export default axios
