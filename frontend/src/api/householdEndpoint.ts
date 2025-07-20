import {AxiosError, AxiosInstance} from "axios"
import {
    HouseholdInvitePublic, HouseholdInviteWithMeta,
    HouseholdMemberUpdateRole,
    HouseholdPublic,
    HouseholdUpdate, HouseholdWithMemberPublic,
    HouseholdWithMembersPublic, Role
} from "@/api/types/households.ts"
import {ApiResponse} from "@/api/types/ApiResponse.ts"

export default (api: AxiosInstance) => {
    const getAllHouseholds = async (): Promise<ApiResponse<Array<HouseholdWithMemberPublic>>> => {
        const response = await api.get("/household/")
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<Array<HouseholdWithMemberPublic>>
        }
        return {
            success: false
        }
    }

    const getHousehold = async (id: string): Promise<ApiResponse<HouseholdPublic>> => {
        const response = await api.get(`/household/${id}`)
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<HouseholdPublic>
        }
        return {
            success: false
        }
    }

    const createHousehold = async (data: HouseholdPublic): Promise<ApiResponse<HouseholdPublic>> => {
        const response = await api.post("/household/", data)
        if (response.status === 201){
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

    const updateHousehold = async (householdId: string, updateData: HouseholdUpdate): Promise<ApiResponse<HouseholdPublic>> => {
        const response = await api.patch(`/household/${householdId}`, updateData)
        if (response.status === 200){
            return {
                success: true,
                data: response.data
            }
        }
        return {
            success: false
        }
    }

    const getAllMembers = async (householdId: string): Promise<ApiResponse<HouseholdWithMembersPublic>> => {
        try{
            const response = await api.get(`/household/${householdId}/member/`)
            return {
                success: response.status === 200,
                data: response.data,
                error: response.data?.detail ?? undefined
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }


    const transferOwnership = async (householdId: string, newOwnerId: string): Promise<ApiResponse> => {
        try{
            const response = await api.post(`/household/${householdId}/transfer-ownership/${newOwnerId}`)
            return {
                success: response.status === 200,
                error: response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            console.log(error)
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }

    const removeMember = async (householdId: string, userId: string): Promise<ApiResponse> => {
        try{
            const response = await api.delete(`/household/${householdId}/member/${userId}`)
            return {
                success: response.status === 204,
                error: response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }

    const updateRole = async (householdId: string, userId: string, role: Role): Promise<ApiResponse> => {
        try{
            const response = await api.patch(`/household/${householdId}/member/${userId}`, {
                role: role
            } as HouseholdMemberUpdateRole)
            return {
                success: response.status === 200,
                error: response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }

    const createInvite = async (householdId: string): Promise<ApiResponse<HouseholdInvitePublic>> => {
        try{
            const response = await api.post(`/household/${householdId}/invite/`)
            const success = response.status === 200;
            return {
                success: success,
                data: success ? response.data : undefined,
                error: success ? undefined : response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }

    const checkInviteValidity = async (code: string): Promise<ApiResponse<HouseholdInviteWithMeta>> => {
        try{
            const response = await api.get(`/household/invite/validate/${code}`)
            const success = response.status === 202;
            return {
                success: success,
                data: success ? response.data : undefined,
                error: success ? undefined : response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }

    const acceptInvite = async (code: string): Promise<ApiResponse> => {
        try{
            const response = await api.post(`/household/invite/accept/${code}`)
            const success = response.status === 200;
            return {
                success: success,
                error: success ? undefined : response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
            }
        }
    }

    const leaveHousehold = async (householdId: string): Promise<ApiResponse> => {
        try{
            const response = await api.delete(`/household/${householdId}/member/`)
            const success = response.status === 204;
            return {
                success: success,
                error: success ? undefined : response.data?.detail ?? ''
            }
        } catch(error: any){
            error = error as AxiosError
            return {
                success: false,
                error: error.response.data.detail
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