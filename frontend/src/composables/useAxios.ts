import axios, {
  AxiosError,
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse
} from 'axios'
import authEndpoint from '@/api/authEndpoint.ts'
import userEndpoint from '@/api/userEndpoint.ts'
import householdEndpoint from '@/api/householdEndpoint.ts'
import itemsEndpoint from '@/api/itemsEndpoint.ts'
import storageEndpoint from '@/api/storageEndpoint.ts'
import configEndpoint from '@/api/configEndpoint.ts'
import adminEndpoint from '@/api/adminEndpoint'

import type { FastAPIError } from '@/api/types/FastAPIError'
import { useNotification } from '@kyvg/vue3-notification'
import { i18n } from '@/plugins/i18n'

interface CustomAxiosRequestConfig extends AxiosRequestConfig {
  _retry?: boolean
}

let instance: AxiosInstance | null = null
let refreshInstance: AxiosInstance | null = null

async function refreshToken() {
  try {
    // if this fails we know, that the refresh token is invalid
    const response = await refreshInstance!.get('/auth/refresh')
    return response.status === 200
  } catch (refreshError) {
    // this is user not logged in
    // check if auth state is correct
  }
  return false
}

export default (baseURL = '/api') => {
  if (!instance) {
    instance = axios.create({
      baseURL,
      withCredentials: true
    })
    refreshInstance = axios.create({
      baseURL: baseURL,
      withCredentials: true
    })
    instance.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as CustomAxiosRequestConfig

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true
          if (await refreshToken()) {
            return instance!(originalRequest)
          } else {
            return error.response
          }
        }

        const errorPayload: FastAPIError | undefined = error.response?.data

        const { notify } = useNotification()
        let title = undefined
        if (typeof errorPayload.detail === 'string') {
          title = errorPayload.detail
        } else {
          title = i18n.global.t('unknown_error')
        }

        console.error(error.response)
        notify({
          title: title,
          type: 'error'
        })

        return error.response ?? error
      }
    )
    instance.interceptors.request.use((config) => {
      return config
    })
  }

  const { ...auth } = authEndpoint(instance)
  const user = userEndpoint(instance)
  const household = householdEndpoint(instance)
  const items = itemsEndpoint(instance)
  const storage = storageEndpoint(instance)
  const config = configEndpoint(instance)
  const admin = adminEndpoint(instance)

  return {
    api: instance,
    auth,
    userEndpoint: user,
    household,
    items,
    storage,
    config,
    admin
  }
}
