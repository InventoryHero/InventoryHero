import {Endpoint} from "./Endpoint.ts";
import {ILoginRequest, ILoginResponse, IRegisterRequest, IUser} from "@/types";
import {clearAuthTokens, getRefreshToken, setAuthTokens} from "axios-jwt";
import {notify} from "@kyvg/vue3-notification";
import {i18n} from "@/lang";
import {Permissions, User} from "@/types/api.ts";





export class UserEndpoint extends Endpoint{

    constructor(){
        super(false, "/user")
    }

    public async getUser():Promise<IUser|undefined> {
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
            notify({
                title: i18n.global.t('toasts.titles.success.register', {name: response.data.user}),
                text: i18n.global.t('toasts.text.success.register'),
                type: "success"
            })
            if(!response.data.confirmation){
                notify({
                    title: i18n.global.t('toasts.titles.info.confirm_email'),
                    text: i18n.global.t('toasts.text.info.confirm_email'),
                    type: 'info'
                })
            }
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async confirmEmail(code: string){
        const response = await this.internalAxios.post(`/confirm/${code}`)
        if(response.status === 200)
        {
            return {
                verified: true,
                status: ""
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            verified: false,
            status: response.data.status
        }
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
}