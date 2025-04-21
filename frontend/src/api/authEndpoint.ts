import {AxiosInstance} from "axios";

export default (api: AxiosInstance) => {

    const login = async (loginFormData: FormData): Promise<boolean> => {
        const response = await api.post("/auth/token", loginFormData)
        return !(response.status < 200 || response.status > 299);
    }

    const logout = async(): Promise<void> => {
        const response = await api.post("/auth/logout")
    }

    const refreshToken = async(refreshInstance: AxiosInstance): Promise<boolean> => {
        const response = await refreshInstance.get("/auth/refresh")
        return response.status === 200
    }


    return {
        login, logout, refreshToken
    }
}