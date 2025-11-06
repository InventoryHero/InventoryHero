import { AxiosError, AxiosInstance } from 'axios'
import {
  HouseholdInvitePublic,
  HouseholdInviteWithMeta,
  HouseholdMemberUpdateRole,
  HouseholdPublic,
  HouseholdUpdate,
  HouseholdWithMemberPublic,
  HouseholdWithMembersPublic,
  Role
} from '@/api/types/households.ts'
import { ApiResponse } from '@/api/types/ApiResponse.ts'

export default (api: AxiosInstance) => {
  const getAllHouseholds = async (): Promise<
    ApiResponse<Array<HouseholdWithMemberPublic>>
  > => {
    const response = await api.get('/household/')
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<Array<HouseholdWithMemberPublic>>
    }
    return {
      success: false
    }
  }

  const getHousehold = async (
    id: string
  ): Promise<ApiResponse<HouseholdPublic>> => {
    const response = await api.get(`/household/${id}`)
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<HouseholdPublic>
    }
    return {
      success: false
    }
  }

  const createHousehold = async (
    data: HouseholdPublic
  ): Promise<ApiResponse<HouseholdPublic>> => {
    const response = await api.post('/household/', data)
    if (response.status === 201) {
      return {
        success: true,
        data: response.data
      }
    }
    return {
      success: false
    }
  }

  const deleteHousehold = async (id: string): Promise<ApiResponse> => {
    const response = await api.delete(`/household/${id}`)
    return {
      success: response.status === 204
    }
  }

  const updateHousehold = async (
    householdId: string,
    updateData: HouseholdUpdate
  ): Promise<ApiResponse<HouseholdPublic>> => {
    const response = await api.patch(`/household/${householdId}`, updateData)
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      }
    }
    return {
      success: false
    }
  }

  const getAllMembers = async (
    householdId: string
  ): Promise<ApiResponse<HouseholdWithMembersPublic>> => {
    const router = useRouter()

    const response = await api.get(`/household/${householdId}/member/`)
    let success = false

    let errorMessage = undefined
    switch (response.status) {
      case 200:
        success = true
        break
      case 403:
        errorMessage = 'no_access'
        break
      case 404:
        errorMessage = 'household_not_found'
        break
      default:
        errorMessage = response.data
    }

    return {
      success: success,
      data: response.data,
      error: !success ? errorMessage : undefined
    }
  }

  const transferOwnership = async (
    householdId: string,
    newOwnerId: string
  ): Promise<ApiResponse> => {
    const response = await api.post(
      `/household/${householdId}/transfer-ownership/${newOwnerId}`
    )
    return {
      success: response.status === 200,
      error: response.data ?? ''
    }
  }

  const removeMember = async (
    householdId: string,
    userId: string
  ): Promise<ApiResponse> => {
    try {
      const response = await api.delete(
        `/household/${householdId}/member/${userId}`
      )
      return {
        success: response.status === 204,
        error: response.data ?? ''
      }
    } catch (error: any) {
      error = error as AxiosError
      return {
        success: false,
        error: error.response.data
      }
    }
  }

  const updateRole = async (
    householdId: string,
    userId: string,
    role: Role
  ): Promise<ApiResponse> => {
    try {
      const response = await api.patch(
        `/household/${householdId}/member/${userId}`,
        {
          role: role
        } as HouseholdMemberUpdateRole
      )
      return {
        success: response.status === 200,
        error: response.data ?? ''
      }
    } catch (error: any) {
      error = error as AxiosError
      return {
        success: false,
        error: error.response.data
      }
    }
  }

  const createInvite = async (
    householdId: string
  ): Promise<ApiResponse<HouseholdInvitePublic>> => {
    try {
      const response = await api.post(`/household/${householdId}/invite/`)
      const success = response.status === 200
      return {
        success: success,
        data: success ? response.data : undefined,
        error: success ? undefined : (response.data ?? '')
      }
    } catch (error: any) {
      error = error as AxiosError
      return {
        success: false,
        error: error.response.data
      }
    }
  }

  const checkInviteValidity = async (
    code: string
  ): Promise<ApiResponse<HouseholdInviteWithMeta>> => {
    try {
      const response = await api.get(`/household/invite/validate/${code}`)
      const success = response.status === 202
      return {
        success: success,
        data: success ? response.data : undefined,
        error: success ? undefined : (response.data ?? '')
      }
    } catch (error: any) {
      error = error as AxiosError
      return {
        success: false,
        error: error.response.data
      }
    }
  }

  const acceptInvite = async (code: string): Promise<ApiResponse> => {
    try {
      const response = await api.post(`/household/invite/accept/${code}`)
      const success = response.status === 200
      return {
        success: success,
        error: success ? undefined : (response.data ?? '')
      }
    } catch (error: any) {
      error = error as AxiosError
      return {
        success: false,
        error: error.response.data
      }
    }
  }

  const leaveHousehold = async (householdId: string): Promise<ApiResponse> => {
    try {
      const response = await api.delete(`/household/${householdId}/member/`)
      const success = response.status === 204
      return {
        success: success,
        error: success ? undefined : (response.data ?? '')
      }
    } catch (error: any) {
      error = error as AxiosError
      return {
        success: false,
        error: error.response.data
      }
    }
  }

  return {
    all: getAllHouseholds,
    one: getHousehold,
    create: createHousehold,
    delete: deleteHousehold,
    update: updateHousehold,
    getAllMembers,
    transferOwnership,
    removeMember,
    updateRole,
    createInvite,
    checkInviteValidity,
    acceptInvite,
    leaveHousehold
  }
}
