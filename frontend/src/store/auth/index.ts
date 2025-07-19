import {defineStore} from "pinia";
import {Household, IRegisterRequest} from "@/types";
import {clearAuthTokens} from "axios-jwt";
import {useLocalStorage} from "@vueuse/core";
import {HouseholdEndpoint, UserEndpoint} from "@/api/http";
import {useGeneralSocketStore, useHouseholdSocketStore} from "@/store";
import {Permissions, User} from "@/types/api.ts";
import useAxiosOld from "@/composables/useAxiosOld.ts";
import {notify} from "@kyvg/vue3-notification";
import {i18n} from "@/lang";
import {HouseholdPublic} from "@/api/types/households.ts";
import {UserPublic} from "@/api/types/user.ts";


interface UserStore {
    user?: User,
    household?: Household,
    authorized?: boolean
}


export const useAuthStore = defineStore('auth', {
    state: () => {
        return ({
            _user: useLocalStorage<UserStore>(
                "user", {},
                {
                    // eslint-disable-next-line @typescript-eslint/no-unused-vars
                    mergeDefaults: (storageValue, _) => storageValue,
                    serializer: {
                        read: (v: string) => v ? JSON.parse(v) : null,
                        write: (v: UserStore) => JSON.stringify(v),
                    },
                },
            ),
            user: undefined as UserPublic|undefined,
            household: undefined as (HouseholdPublic | undefined),
            authorized: false,
            _households: [] as Array<Household>,
            permissions: {} as Permissions,
            userEndpoint: useAxiosOld<UserEndpoint>("user"),
            returnUrl: null as (null | string),
        });
    },
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
            this.returnUrl = null
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
                return {
                    success: false,
                    message: ""
                }
            }
            this.whoami()

            return {
                success: true
            }
        },
        async logout()
        {
            const {auth} = useAxios()
            this.returnUrl = null;
            /*const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
            const generalSocketStore = useGeneralSocketStore()
            generalSocketStore.leave()*/
            await auth.logout()

            await this.reset()

            this.$router.push("/login")
        },
        changeHousehold(household: Household | undefined)
        {
            const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
            this._user!.household = household
            if(household)
            {
                socketStore.joinHousehold()
            }
        },
        async destroy(){
            const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
            const generalSocketStore = useGeneralSocketStore()
            generalSocketStore.leave()
            await this.reset()
            await this.$router.push("/login")

        },
        async register(username: string, password: string, email: string)
        {
            const data: IRegisterRequest = {
                username: username,
                password: password,
                email: email
            }
            return await this.userEndpoint.axios.register(data)
        },
        async isAuthorized(){
            const {userEndpoint} = useAxios()
            const {success, data: defaultHousehold}  = await userEndpoint.getDefaultHousehold()
            this.household = defaultHousehold
            this.authorized = success
            return success
        },
        setReturnUrl(url: string)
        {
            this.returnUrl = url
        },
        async followReturnUrl(){
            const returnUrl = this.returnUrl
            this.returnUrl = null

            if(returnUrl === null)
            {
                return;
            }

           await this.$router.push(returnUrl)
        },
        async fetchPermissions(){
            if(!(await this.isAuthorized())){
                return false
            }
            this.permissions = await this.userEndpoint.axios.getPermissions()
            return true
        },
        async fetchHouseholds(){
            if(!(await this.isAuthorized())){
                return
            }
            const {axios: householdEndpoint} = useAxiosOld<HouseholdEndpoint>("household")
            this._households = await householdEndpoint.getHouseholds()
            this._households.sort((a, b) => a.name.localeCompare(b.name))
        },
        async init(){
            const isAuthorized = await this.isAuthorized()
            if(!isAuthorized){
                await this.reset()
                return
            }
            await this.whoami()
        },
        updateUser(toUpdate: User){
            this._user.user = {
                ...toUpdate,
                isAdmin: undefined
            }
        },
        addHousehold(household: Household){
            this._households.push(household)
            this._households.sort((a, b) => a.name.localeCompare(b.name))
        },
        leftHousehold(household: Household){
            this._households = this._households.filter(h => h.id !== household.id)
        },
        removeHousehold(id: number, action: string){
            const household = this._households.find(h => h.id === id)
            if(!household){
                return
            }
            const currentHousehold = this.household?.id
            const removedName = household.name
            this._households = this._households.filter(h => h.id !== id)
            const notification = {
                title: i18n.global.t(`toasts.titles.info.household_${action}`),
                text: i18n.global.t(`toasts.text.info.household_${action}`, {name: removedName}),
                type: 'info',
            }
            if(id === currentHousehold){

                this.changeHousehold(undefined)
                this.$router.push("/households").then(() => {
                    notify(notification)
                })
            } else {
                notify(notification)
            }
        },
        updateHousehold(id: number, updateData: Partial<Household>){
            const household = this._households.findIndex(h => h.id === id)
            if(household === -1)
                return
            this._households[household] = {
                ...this._households[household],
                ...updateData
            }
        },
        ownHousehold(id: number){
            const household = this._households.find(h => h.id === id)
            if(!household){
                return
            }
            household.creator = this.user!.id
            notify({
                title: i18n.global.t('toasts.titles.info.ownership_received', {household: household.name}),
                text: i18n.global.t('toasts.text.info.ownership_received'),
                type: 'info'
            })
        },
        async resendConfirmation(username: string){
            const success = await this.userEndpoint.axios.resendConfirmationEmail(username)
            return success
        }
    },
    getters: {
        households: state => state._households,

        householdName: state => state._user.household?.name ?? '',
        userSet: state => {return state._user !== null},
        isAdmin: state => {
            return state.permissions.admin ?? false
        }
    }
})