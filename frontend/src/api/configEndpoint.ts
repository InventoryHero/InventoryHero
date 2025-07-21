import {AxiosInstance} from "axios";
import {ConfigPublic} from "@/api/types/config.ts";
import {ApiResponse} from "@/api/types/ApiResponse.ts";

export default (api: AxiosInstance) => {

    const getConfig = async (): Promise<ApiResponse<ConfigPublic>> => {
        const response = await api.get("/config/")
        const success = response.status == 200
        return {
            success: success,
            data: success ? response.data : undefined,
            error: !success ? response.data?.detail ?? undefined : undefined
        }
    }

    return {
        getConfig
    }
}