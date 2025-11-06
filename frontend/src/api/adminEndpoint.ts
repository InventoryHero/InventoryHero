import { AxiosInstance } from 'axios'
import { UserPublic } from './types/households'
import { ApiResponse } from './types/ApiResponse'
import { AdminUserCreate, AdminUserUpdate } from './types/user'
import { AppConfig } from './types/config'

export default (api: AxiosInstance) => {
  const getAllUsers = async (): Promise<ApiResponse<UserPublic[]>> => {
    const response = await api.get('/admin/user/users')
    const success = response.status === 200
    return {
      success: success,
      data: success ? (response.data as UserPublic[]) : undefined,
      error: !success ? response.data : undefined
    }
  }

  const getUser = async (id: string): Promise<ApiResponse<UserPublic>> => {
    const response = await api.get(`/admin/user/${id}`)
    const success = response.status === 200
    return {
      success,
      data: success ? (response.data as UserPublic) : undefined,
      error: !success ? response.data : undefined
    }
  }

  const updateUser = async (
    id: string,
    to_update: AdminUserUpdate
  ): Promise<ApiResponse<UserPublic>> => {
    const response = await api.put(`/admin/user/${id}`, to_update)

    const success = response.status === 200
    return {
      success,
      data: success ? (response.data as UserPublic) : undefined,
      error: !success ? response.data : undefined
    }
  }

  const resetUserPassword = async (
    id: string
  ): Promise<ApiResponse<string>> => {
    const response = await api.put(`/admin/user/${id}/reset-password`)
    const success = response.status === 200
    return {
      success,
      data: success ? (response.data as string) : undefined,
      error: !success ? response.data : undefined
    }
  }

  const createUser = async (
    newUser: AdminUserCreate
  ): Promise<ApiResponse<UserPublic>> => {
    const response = await api.post('/admin/user/create', newUser)
    const success = response.status === 201
    return {
      success,
      data: success ? response.data : undefined,
      error: !success ? response.data : undefined
    }
  }

  const deleteUser = async (id: string): Promise<ApiResponse<void>> => {
    const response = await api.delete(`/admin/user/${id}`)
    const success = response.status === 204
    return {
      success
    }
  }

  const resendEmailConfirmation = async (
    id: string
  ): Promise<ApiResponse<void>> => {
    const response = await api.post(`/admin/user/${id}/resend-confirmation`)
    return {
      success: response.status === 204
    }
  }

  const getAppConfig = async (): Promise<ApiResponse<AppConfig>> => {
    const response = await api.get('/admin/config/')
    const success = response.status === 200
    return {
      success,
      data: success ? response.data : undefined
    }
  }

  const sendTestEmail = async (email: string): Promise<ApiResponse> => {
    const response = await api.post('/admin/config/email/test', null, {
      params: {
        email
      }
    })
    return {
      success: response.status === 204
    }
  }

  return {
    getAllUsers,
    getUser,
    updateUser,
    resetUserPassword,
    createUser,
    deleteUser,
    resendEmailConfirmation,
    getAppConfig,
    sendTestEmail
  }
}
