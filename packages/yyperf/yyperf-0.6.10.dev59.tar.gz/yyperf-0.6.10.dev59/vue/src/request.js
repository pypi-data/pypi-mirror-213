import axios from 'axios'

const service = axios.create({
  // baseURL: apiUrl, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 60000, // request timeout
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: true
})


service.interceptors.request.use(
  config => {
    // config.headers['X-CSRFToken'] = getLocalStorage("csrftoken")
    // config.headers['Content-Type'] = 'multipart/form-data'
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    return response
  },
  error => {
    console.log(error.message)
    return Promise.reject(error)
  }
)
export default service
