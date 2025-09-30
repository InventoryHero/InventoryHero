import { AxiosInstance } from 'axios'
import { UserPublic } from './types/households'
import { ApiResponse } from './types/ApiResponse'

export default (api: AxiosInstance) => {
  const getAllUsers = async (): Promise<ApiResponse<UserPublic[]>> => {
    const response = await api.get('/admin/user/users')
    const success = response.status === 200
    return {
      success: success,
      data: success ? (response.data as UserPublic[]) : undefined,
      error: !success ? response.data.detail : undefined
    }
  }

  const getUser = async (id: string): Promise<ApiResponse<UserPublic>> => {
    const response = await api.get(`/admin/user/${id}`)
    const success = response.status === 200
    return {
      success,
      data: success ? (response.data as UserPublic) : undefined,
      error: !success ? response.data.detail : undefined
    }
  }

  return {
    getAllUsers,
    getUser
  }
}
