import {Endpoint, baseURL} from "./Endpoint.ts";
import {ILoginRequest, ILoginResponse, IRegisterRequest} from "@/types";
import {clearAuthTokens, getRefreshToken, setAuthTokens} from "axios-jwt";
import {notify} from "@kyvg/vue3-notification";
import {i18n} from "@/lang";
import {Permissions, User} from "@/types/api.ts";
import axios, {AxiosError} from "axios";


export class UserEndpoint extends Endpoint{

    constructor(){
        super(false, "/user")
    }

    public async getUser():Promise<User|undefined> {
        const response = await this.internalAxios.get("");
        if(response.status === 200)
        {
            return response.data
        }

        this.handleNonErrorNotifications(response)
        return undefined
    }

    public async login(loginParams: ILoginRequest){
        const response = await this.internalAxios.post('/login', loginParams)
        if(response.status === 200)
        {
            let data: ILoginResponse = response.data as ILoginResponse

            await setAuthTokens({
                accessToken: data.access_token,
                refreshToken: data.refresh_token
            })
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async logout(){
        const refreshToken = await getRefreshToken() ?? ""

        let body = {
            data: {
                refreshToken: refreshToken
            }
        }
        const response = await this.internalAxios.delete("/logout", body)
        console.log(response)
        if(response.status === 200)
        {
            await clearAuthTokens()
            return true
        }
        return false
    }

    public async register(data: IRegisterRequest){
        const response = await this.internalAxios.post("/register", data)
        if(response.status === 200)
        {

            if(!response.data.confirmation){
                notify({
                    title: i18n.global.t('toasts.titles.success.register', {name: response.data.user}),
                    text: i18n.global.t('toasts.text.success.confirm_email'),
                    type: "success"
                })

            }else {
                notify({
                    title: i18n.global.t('toasts.titles.success.register', {name: response.data.user}),
                    text: i18n.global.t('toasts.text.success.register'),
                    type: "success"
                })
            }
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async getPermissions(){
        const response = await this.internalAxios.get("/permissions")
        if(response.status === 200)
        {
            return response.data as Permissions
        }
        this.handleNonErrorNotifications(response)
        return {} as Permissions
    }

    public async updateUser(updated: Partial<User>, user: Partial<User>){
        if(user.id === undefined){
            return {
                success: false,
                msg: undefined,
                user: undefined
            }
        }
        const response = await this.internalAxios.post(`/update/${user.id}`, updated)
        if(response.status === 200){
            return {
                success: true,
                msg: response.data.status,
                user: response.data.user
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            msg: undefined,
            user: undefined
        }
    }

    public async updateMe(updated: Partial<User>){
        console.log(updated)
        const response = await this.internalAxios.post(`/update`, updated)
        console.log(response)
        if(response.status === 200){
            return {
                success: true,
                msg: response.data.status,
                user: response.data.user
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            msg: undefined,
            user: undefined
        }
    }

    public async createUser(toCreate: Partial<User>){
        const response = await this.internalAxios.post("/create", toCreate)
        if(response.status === 200){
            return {
                success: true,
                user: response.data.user
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            user: undefined
        }
    }

    public async deleteUser(toDelete: number){
        const response = await this.internalAxios.delete(`/delete/${toDelete}`)
        if(response.status === 200){
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async resetPasswordRequest(userId?: number)
    {
        let url = "/reset-password"
        if(userId){
            url += `/${userId}`
        }
        // TODO IF SENDING_EMAIL IS DISABLED HIDE RESET BUTTON
        const response = await this.internalAxios.get(url)
        if(response.status === 200){
            return {
                success: true,
                message: response.data.status
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            // @ts-expect-error
            message: response.response.data.status
        }
    }

    public async resetPassword(oldPassword: string, newPassword: string){
        const response = await this.internalAxios.post(`/reset-password`, {
            oldPassword, newPassword
        })
        if(response.status === 200){
            return {
                success: true
            };
        }
        this.handleNonErrorNotifications(response);
        return {
            success: false
        }
    }


    // functions that use separate axios
    public async forgotPassword(email: string){
        // this should not happen with axios instance where a user might be logged in
        const passwordResetAxios = axios.create()
        try{
            const response = await passwordResetAxios.get(`${baseURL}user/reset-password/${email}`)
            if(response.status === 200){
                return {
                    success: true,
                    message: ""
                };
            }
        } catch(error: any){
            return {
                success: false,
                message: error.response.data.status
            }
        }
    }

    public async resetPasswordPreflight(code: string){
        // this should not happen with axios instance where a user might be logged in
        const passwordResetAxios = axios.create()
        try{
            const response = await passwordResetAxios.put(`${baseURL}user/reset-password/${code}`)
            if(response.status === 200){
                return {
                    success: true,
                    message: ""
                };
            }
        } catch(error: any){
            return {
                success: false,
                message: error.response.data.status
            }
        }
    }

    public async resetPasswordMail(code: string, password: string){
        const passwordResetAxios = axios.create()
        try{
            const response = await passwordResetAxios.post(`${baseURL}user/reset-password/${code}`, {
                password
            })
            if(response.status === 200){
                return {
                    success: true,
                    message: ""
                };
            }
        } catch(error: any){
            return {
                success: false,
                message: error.response.data.status
            }
        }
    }

    public async confirmEmail(code: string){
        const confirmAxios = axios.create()
        try{
            const response = await confirmAxios.post(`${baseURL}user/confirm/${code}`)
            console.log(response)
            return {
                success: response.status === 200,
                verified: response.status === 200,
                status: response.data?.status
            }

        } catch(error: any){
            console.log(error)
            return {
                success: false,
                verified: undefined,
                status: error.response.data.status
            }
        }
        // TODO HANDLE ERRORS
    }


}