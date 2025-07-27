import axios, {AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse} from "axios";
import authEndpoint from "@/api/authEndpoint.ts";
import userEndpoint from "@/api/userEndpoint.ts";
import householdEndpoint from "@/api/householdEndpoint.ts";
import itemsEndpoint from "@/api/itemsEndpoint.ts";
import storageEndpoint from "@/api/storageEndpoint.ts";
import configEndpoint from "@/api/configEndpoint.ts";

interface CustomAxiosRequestConfig extends AxiosRequestConfig {
    _retry?: boolean;
}

let instance: AxiosInstance | null = null;
let refreshInstance: AxiosInstance | null = null;

export default (baseURL = "/api")=> {
    if(!instance){
        instance = axios.create({
            baseURL,
            withCredentials: true
        })
        refreshInstance = axios.create({
            baseURL: baseURL,
            withCredentials: true
        })
        instance.interceptors.response.use((response: AxiosResponse) => response, async (error: AxiosError) => {
            const originalRequest = error.config as CustomAxiosRequestConfig;
            console.log(error)
            if(error.response?.status === 401 && !originalRequest._retry){
                originalRequest._retry = true
                try {
                    // if this fails we know, that the refresh token is invalid
                    const success = await refreshToken(refreshInstance!)

                    if(success){
                        return instance!(originalRequest);
                    }
                } catch (refreshError) {

                    console.error(refreshError);
                }
            }


            switch(error.response?.status){
                case 401:
                    console.error(error)
                    return error.response
            }
            return error.response ?? error;
        })
        instance.interceptors.request.use((config) => {
            return config;
        })
    }

    const {refreshToken, ...auth} = authEndpoint(instance)
    const user = userEndpoint(instance)
    const household = householdEndpoint(instance)
    const items = itemsEndpoint(instance)
    const storage = storageEndpoint(instance)
    const config = configEndpoint(instance)

    return {
        api: instance,
        auth,
        userEndpoint: user,
        household,
        items,
        storage,
        config
    }

}