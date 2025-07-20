import {defineStore} from "pinia";
import {Household, IRegisterRequest} from "@/types";
import {useGeneralSocketStore, useHouseholdSocketStore} from "@/store";
import {Permissions, User} from "@/types/api.ts";
import {HouseholdPublic} from "@/api/types/households.ts";
import {UserPublic} from "@/api/types/user.ts";


interface UserStore {
    user?: User,
    household?: Household,
    authorized?: boolean
}


export const useAuthStore = defineStore('auth', {
    state: () =>({
        user: undefined as UserPublic|undefined,
        household: undefined as (HouseholdPublic | undefined),
        authorized: false,
        permissions: {} as Permissions,
    }),
    actions: {
        async whoami(){
            const {userEndpoint} = useAxios()
            const {success, data: user} = await userEndpoint.self()
            if(!success){
                // TODO ERROR AND LOGOUT
            }
            this.user = user
        },
        async reset() {
            this.user = undefined
            this.household = undefined
            this.authorized = false
            /*const generalSocket = useGeneralSocketStore()
            const householdSocket = useHouseholdSocketStore()
            generalSocket.updateHeaders()
            householdSocket.updateHeaders()*/

        },
        async login(username: string, password: string)
        {
            // reset auth store, to prevent any poisoning
            await this.reset()
            const { auth, userEndpoint} = useAxios()
            const loginFormData = new FormData()
            loginFormData.append("username", username)
            loginFormData.append("password", password)
            const loginSuccessful = await auth.login(loginFormData)
            if(!loginSuccessful){
                // TODO
                return {
                    success: false,
                    message: ""
                }
            }
            const {success, data: user} = await userEndpoint.self()
            if(!success){
                // TODO
            }
            this.user = user
            return {
                success: true
            }
        },
        async logout()
        {
            const {auth} = useAxios()
            await auth.logout()
            await this.reset()
        },

        async destroy(){
            const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
            const generalSocketStore = useGeneralSocketStore()
            generalSocketStore.leave()
            await this.reset()
        },
        async register(username: string, password: string, email: string)
        {
            const data: IRegisterRequest = {
                username: username,
                password: password,
                email: email
            }
            // TODO REGISTER
        },
        async isAuthorized(){
            const {userEndpoint} = useAxios()
            const {success, data: defaultHousehold}  = await userEndpoint.getDefaultHousehold()
            this.household = defaultHousehold
            this.authorized = success
            return success
        },

        async init(){
            const isAuthorized = await this.isAuthorized()
            if(!isAuthorized){
                await this.reset()
                return
            }
            await this.whoami()
        },

    },
    getters: {
        isAdmin: state => {
            return state.permissions.admin ?? false
        }
    }
})