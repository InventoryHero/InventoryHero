import { AxiosInstance } from 'axios'
import { UserPublic } from './types/households'
import { ApiResponse } from './types/ApiResponse'

export default (api: AxiosInstance) => {
  const getAllUsers = async (): Promise<ApiResponse<UserPublic[]>> => {
    const response = await api.get('/admin/users')
    const success = response.status === 201
    return {
      success: success,
      data: success ? (response.data as UserPublic[]) : undefined,
      error: !success ? response.data.detail : undefined
    }
  }

  return {
    getAllUsers
  }
}
