import {defineStore} from "pinia";
import {Household, IRegisterRequest} from "@/types";
import {clearAuthTokens, getAccessToken, isLoggedIn} from "axios-jwt";
import {useLocalStorage} from "@vueuse/core";
import {UserEndpoint} from "@/api/http";
import {useGeneralSocketStore, useHouseholdSocketStore} from "@/store";
import {Permissions, User} from "@/types/api.ts";
import useAxios from "@/composables/useAxios.ts";


interface UserStore {
    user?: User,
    household?: Household,
    authorized?: boolean
}


export const useAuthStore = defineStore('auth', {
    state: () => ({
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
        permissions: {} as Permissions,
        userEndpoint: useAxios<UserEndpoint>("user"),
        returnUrl: null as (null|string),
    }),
    actions: {
        async reset() {
            this._user = {};
            this.permissions = {}
            this.returnUrl = null
            await clearAuthTokens()
            const generalSocket = useGeneralSocketStore()
            const householdSocket = useHouseholdSocketStore()
            generalSocket.updateHeaders()
            householdSocket.updateHeaders()

        },
        async login(username: string, password: string)
        {
            const loginSuccess = await this.userEndpoint.axios.login({
                username: username,
                password: password
            })
            if(!loginSuccess){
                return
            }
            if(!(await isLoggedIn())) {
                return;
            }

           const userData =  await this.userEndpoint.axios.getUser()
            if(userData !== undefined && userData !== null)
            {
                this._user.user = {
                    ...userData,
                    isAdmin: undefined
                }
                this._user.authorized = true
            }
            await this.fetchPermissions()
            getAccessToken().then((token) => {
                const generalSocket = useGeneralSocketStore()
                const householdSocket = useHouseholdSocketStore()
                generalSocket.updateHeaders(token)
                householdSocket.updateHeaders(token)
            })
            if(this.returnUrl === null)
            {
                await this.$router.push("/");
                return;
            }
            await this.$router.push(this.returnUrl)
        },
        async logout()
        {
            this.returnUrl = null;
            const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
            const success = await this.userEndpoint.axios.logout()
            if(!success)
            {
                // TODO notify
                console.log("WTF")
            }
            await this.reset()
            this.$router.push("/login")
        },
        async changeHousehold(household: Household | undefined)
        {
            if(household === undefined)
            {
                return;
            }
            const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
            this._user!.household  = {
                ...household,
                members: []
            }
            socketStore.joinHousehold()
        },
        async destroy(){
            const socketStore = useHouseholdSocketStore()
            socketStore.leaveHousehold()
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
            return await isLoggedIn();
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
                return
            }
            this.permissions = await this.userEndpoint.axios.getPermissions()
        },
        async init(){
            await this.fetchPermissions()
        },
        updateUser(toUpdate: User){
            this._user.user = {
                ...toUpdate,
                isAdmin: undefined
            }
        }
    },
    getters: {
        user: state => state._user.user,
        household: state => {return state._user.household?.id ?? -1},
        householdName: state => state._user.household?.name ?? '',
        userSet: state => {return state._user !== null},
        isAdmin: state => {
            return state.permissions.admin ?? false
        },
        authorized: state => state._user.authorized ?? false
    }
})