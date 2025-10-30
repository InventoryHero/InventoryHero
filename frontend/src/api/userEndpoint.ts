import { AxiosInstance } from 'axios'
import {
  ChangePasswordForm,
  ResetPasswordResponse,
  ResetPasswordForm,
  TokenValidationResponse,
  UserCreate,
  UserPublic,
  UserUpdate,
  ChangePasswordFormBase
} from '@/api/types/user.ts'
import { ApiResponse } from '@/api/types/ApiResponse.ts'
import {
  HouseholdPublic,
  HouseholdSelection,
  HouseholdWithMemberPublic
} from '@/api/types/households.ts'

export default (api: AxiosInstance) => {
  const self = async (): Promise<ApiResponse<UserPublic>> => {
    const response = await api.get('/user/self')
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<UserPublic>
    }
    return {
      success: false
    }
  }

  const setDefaultHousehold = async (
    household: HouseholdSelection
  ): Promise<ApiResponse<HouseholdPublic>> => {
    const response = await api.post('/user/current-household', household)
    return {
      success: response.status === 200,
      data: response.data
    }
  }

  const getDefaultHousehold = async (): Promise<
    ApiResponse<HouseholdWithMemberPublic | undefined>
  > => {
    try {
      const response = await api.get('/user/current-household')
      if (response.status === 200) {
        return {
          success: true,
          data: response.data
        }
      }
    } catch (error) {}
    return {
      success: false
    }
  }

  const updateUser = async (
    to_update: UserUpdate
  ): Promise<ApiResponse<UserPublic>> => {
    const response = await api.put('/user/self', to_update)
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<UserPublic>
    }
    return {
      success: false
    }
  }

  const changePassword = async (
    passwordForm: ChangePasswordForm
  ): Promise<ApiResponse<void>> => {
    const response = await api.post('/user/change-password', passwordForm)
    return {
      success: response.status === 200,
      error: response.data?.detail ?? undefined
    }
  }

  const resetPassword = async (
    payload: ResetPasswordForm
  ): Promise<ApiResponse<void>> => {
    const response = await api.post('/user/reset-password', payload)
    return {
      success: response.status === 200,
      error: response.data?.detail ?? undefined
    }
  }

  const resetPasswordWithToken = async (
    code: string,
    payload: ChangePasswordFormBase
  ): Promise<ApiResponse<ResetPasswordResponse>> => {
    const response = await api.post(`/user/reset-password/${code}`, payload)
    const success = response.status === 200
    return {
      success: success,
      data: success ? response.data : undefined,
      error: success ? undefined : (response.data?.detail ?? undefined)
    }
  }

  const register = async (payload: UserCreate): Promise<ApiResponse<void>> => {
    const response = await api.post('/user/register', payload)
    return {
      success: response.status === 201,
      error: response.data?.detail ?? undefined
    }
  }

  const confirmEmail = async (code: string): Promise<ApiResponse<void>> => {
    const response = await api.post(`/user/confirm-email/${code}`)
    return {
      success: response.status === 204,
      error: response.data?.detail ?? undefined
    }
  }

  const requestEmailConfirmation = async (): Promise<ApiResponse<void>> => {
    const response = await api.get(`/user/request-confirmation`)
    return {
      success: response.status === 204,
      error: response.data?.detail ?? undefined
    }
  }

  const checkPasswordResetCode = async (
    code: string
  ): Promise<ApiResponse<TokenValidationResponse>> => {
    const response = await api.get(`/user/validate-password-token/${code}`)
    const success = response.status === 200
    return {
      success: success,
      data: success ? response.data : undefined,
      error: !success ? (response.data?.detail ?? undefined) : undefined
    }
  }

  return {
    self,
    setDefaultHousehold,
    getDefaultHousehold,
    updateUser,
    changePassword,
    resetPassword,
    register,
    confirmEmail,
    requestEmailConfirmation,
    checkPasswordResetCode,
    resetPasswordWithToken
  }
}
