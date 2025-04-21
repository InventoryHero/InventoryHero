import {AxiosInstance} from "axios"
import {UserPublic} from "@/api/types/user.ts"
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

    return {
        self,
        setDefaultHousehold,
        getDefaultHousehold,
    }
}