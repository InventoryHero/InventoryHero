import axios, {AxiosInstance, AxiosResponse} from "axios";
import {useAuthStore} from "@/store";
import {i18n} from "@/lang";
import {applyAuthTokenInterceptor, getBrowserLocalStorage, IAuthTokens} from "axios-jwt";
import {notify} from "@kyvg/vue3-notification";

export const baseURL = '/api/v1/'


async function requestRefresh(refreshToken: string): Promise<IAuthTokens | string>{
    const response = await axios.post(`${baseURL}user/refresh_token`, {}, {
            headers: {
                'Authorization': 'Bearer ' + refreshToken
            }
        }
    )
    return response.data.access_token
}

export class Endpoint {
    protected internalAxios: AxiosInstance
    protected prependHousehold: boolean = true
    protected endpoint: string = ""
    protected readonly authStore


    constructor(household: boolean = true, endpoint: string = ""){
        this.authStore = useAuthStore();

        this.prependHousehold = household
        if(endpoint !== ""){
            this.endpoint = "/" + endpoint.replace("/", "")
        }
        this.internalAxios = axios.create({
            baseURL: baseURL
        })
        this.internalAxios.interceptors.response.use((response) => response, async (error) => {
            switch (error?.response?.status)
            {
                case 400:
                    notify({
                        title: i18n.global.t(`toasts.titles.error.${error.response.data.status ?? 'invalid_request'}`),
                        text: i18n.global.t(`toasts.text.error.${error.response.data.status?? 'invalid_request'}`),
                        type: 'error'
                    })
                    break
                case 401:
                    if(error.response.data.status!== null && error.response.data.status !== undefined) {
                        notify({
                            title: i18n.global.t(`toasts.titles.error.${error.response.data.status ?? 'unauthorized'}`),
                            text: i18n.global.t(`toasts.text.error.${error.response.data.status ?? 'unauthorized'}`),
                            type: 'error'
                        })
                    }
                    await this.authStore.destroy();
                    break
                case 403:
                    if(error.response.data.status!== null && error.response.data.status !== undefined) {
                        notify({
                            title: i18n.global.t(`toasts.titles.error.${error.response.data.status ?? 'unauthorized'}`),
                            text: i18n.global.t(`toasts.text.error.${error.response.data.status ?? 'unauthorized'}`),
                            type: 'error'
                        })
                    }
                    //await this.authStore.destroy();
                    break
                case 404:
                    notify({
                        title: i18n.global.t(`toasts.titles.error.${error.response.data.status ?? 'not_found'}`),
                        text: i18n.global.t(`toasts.text.error.${error.response.data.status ?? 'not_found'}`),
                        type: 'error'
                    })
                    break
                case 409:
                    notify({
                        title: i18n.global.t(`toasts.titles.error.${error.response.data.status ?? 'conflict'}`),
                        text: i18n.global.t(`toasts.text.error.${error.response.data.status ?? 'conflict'}`),
                        type: 'error'
                    })
                    break
                case 422:
                    notify({
                        title: i18n.global.t(`toasts.titles.error.${error.response.data.status}`),
                        text: i18n.global.t(`toasts.titles.error.${error.response.data.status}`),
                        type: 'error'
                    })
                    break
                case 503:
                    if(error.response.data.status === "email_not_configured")
                    {
                        break
                    }
                    notify({
                        title: i18n.global.t('toasts.titles.error.service_not_available'),
                        text: i18n.global.t('toasts.titles.error.service_not_available'),
                        type: 'error'
                    })
                    break
                default:
                    // TODO REPORT BUTTON IN TOAST
                    notify({
                        title: i18n.global.t('toasts.titles.error.undefined_server_error'),
                        text: i18n.global.t('toasts.titles.error.undefined_server_error'),
                        type: 'error'
                    })
                    break
            }
            return error
        })

        this.internalAxios.interceptors.request.use((cfg) => {
            if(this.prependHousehold)
            {
                cfg.baseURL += `${this.authStore.household}`
            }
            cfg.url = this.endpoint + cfg.url
            return cfg
        })
        applyAuthTokenInterceptor(this.internalAxios, { requestRefresh, getStorage: getBrowserLocalStorage })
    }

    protected handleNonErrorNotifications(response: AxiosResponse){
        switch(response.status){
            case 200:
                return
            case 204:
                if(response.data.status !== null && response.data.status !== undefined)
                {
                    notify({
                        title: i18n.global.t(`toasts.titles.info.${response.data.status}`),
                        text: i18n.global.t(`toasts.text.info.${response.data.status}`),
                        type: 'info'
                    })
                }

                return
        }
    }

}



