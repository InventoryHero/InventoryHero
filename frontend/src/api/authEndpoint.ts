import { AxiosInstance } from 'axios'
import { ResetPasswordForm } from '@/api/types/user.ts'
import { ApiResponse } from '@/api/types/ApiResponse.ts'

export default (api: AxiosInstance) => {
  const login = async (loginFormData: FormData): Promise<ApiResponse<void>> => {
    const response = await api.post('/auth/token', loginFormData)
    const success = !(response.status < 200 || response.status > 299)
    return {
      success: success,
      error: !success ? (response.data.detail ?? '') : undefined
    }
  }

  const logout = async (): Promise<void> => {
    const response = await api.post('/auth/logout')
  }

  const refreshToken = async (
    refreshInstance: AxiosInstance
  ): Promise<boolean> => {
    const response = await refreshInstance.get('/auth/refresh')
    return response.status === 200
  }

  return {
    login,
    logout,
    refreshToken
  }
}
