import {AxiosInstance} from "axios"
import {ChangePasswordForm, ResetPasswordForm, UserPublic, UserUpdate} from "@/api/types/user.ts"
import {ApiResponse} from "@/api/types/ApiResponse.ts"
import {HouseholdPublic, HouseholdSelection, HouseholdWithMemberPublic} from "@/api/types/households.ts";

export default (api: AxiosInstance) => {
    const self = async (): Promise<ApiResponse<UserPublic>> => {
        const response = await api.get("/user/self")
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<UserPublic>
        }
        return {
            success: false
        }
    }

    const setDefaultHousehold = async(household: HouseholdSelection): Promise<ApiResponse<HouseholdPublic>> => {
        const response = await api.post("/user/current-household", household)
        return {
            success: response.status === 200,
            data: response.data
        }
    }

    const getDefaultHousehold = async (): Promise<ApiResponse<HouseholdWithMemberPublic|undefined>> => {
        try{
            const response = await api.get("/user/current-household")
            if(response.status === 200){
                return {
                    success: true,
                    data: response.data
                }
            }
        } catch(error){

        }
        return {
            success: false
        }
    }

    const updateUser = async (to_update: UserUpdate): Promise<ApiResponse<UserPublic>> => {
        const response = await api.put("/user/self", to_update)
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<UserPublic>
        }
        return {
            success: false
        }
    }

    const changePassword = async (passwordForm: ChangePasswordForm): Promise<ApiResponse<void>> => {
        const response = await api.post("/user/change-password", passwordForm)
        return {
            success: response.status === 200,
            error: response.data?.detail ?? undefined
        }
    }

    const resetPassword = async (payload: ResetPasswordForm): Promise<ApiResponse<void>> => {
        console.log(payload)
        const response = await api.post("/user/reset-password", payload)
        return {
            success: response.status === 200,
            error: response.data?.detail ?? undefined
        }
    }

    return {
        self,
        setDefaultHousehold,
        getDefaultHousehold,
        updateUser,
        changePassword,
        resetPassword,
    }
}