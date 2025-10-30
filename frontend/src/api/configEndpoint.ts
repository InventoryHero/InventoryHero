import { AxiosInstance } from 'axios'
import { ConfigPublic } from '@/api/types/config.ts'
import { ApiResponse } from '@/api/types/ApiResponse.ts'

export default (api: AxiosInstance) => {
  const getConfig = async (): Promise<ApiResponse<ConfigPublic>> => {
    const response = await api.get('/config/')
    const success = response.status == 200
    return {
      success: success,
      data: success ? response.data : undefined,
      error: !success ? (response.data?.detail ?? undefined) : undefined
    }
  }

  const getTranslationFiles = async (locale: string): Promise<any> => {
    const response = await api.get(`/config/i18n/${locale}`)
    if (response.status === 200) {
      return response.data
    }
  }

  return {
    getConfig,
    getTranslationFiles
  }
}
