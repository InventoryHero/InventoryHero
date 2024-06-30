import {defineStore} from "pinia";
import {Household, IRegisterRequest} from "@/types";
import {isLoggedIn} from "axios-jwt";
import {useLocalStorage} from "@vueuse/core";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useHouseholdSocket} from "@/store";
import {Permissions} from "@/types/api.ts";





export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: useLocalStorage(
            "user", null,
             {
                mergeDefaults: (storageValue, defaults) => storageValue,
                serializer: {
                    read: (v: any) => v ? JSON.parse(v) : null,
                    write: (v: any) => JSON.stringify(v),
                },
            },
        ),
        permissions: {} as Permissions,
        userEndpoint: useNewAxios("user") as {axios: UserEndpoint},
        returnUrl: null as (null|string),
    }),
    actions: {
        reset() {
            this.user = null;
            this.permissions = {}
            this.returnUrl = null
        },
        async login(username: string, password: string)
        {
            let loginSuccess = await this.userEndpoint.axios.login({
                username: username,
                password: password
            })
            if(!loginSuccess){
                return
            }
            if(!isLoggedIn()) {
                return;
            }


           let userData =  await this.userEndpoint.axios.getUser()

            if(userData !== undefined && userData !== null)
            {
                this.user = {...userData, authorized: true}
            }
            await this.fetchPermissions()
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
            this.user.authorized = false
            await this.$router.push("/logout")
            const socketStore = useHouseholdSocket()
            socketStore.leaveHousehold()



            const success = await this.userEndpoint.axios.logout()
            this.user = null;
            if(!success)
            {
                // TODO notify
            }
            this.reset()
            this.$router.push("/login")
        },
        async changeHousehold(household: Household | undefined)
        {
            if(household === undefined)
            {
                return;
            }

            const socketStore = useHouseholdSocket()
            socketStore.leaveHousehold()
            this.user.household  = {
                id: household.id,
                name: household.name
            }
            socketStore.joinHousehold()
        },
        async destroy(){
            const socketStore = useHouseholdSocket()
            socketStore.leaveHousehold()
            this.user = null;
            await this.$router.push("/login")
            this.reset()
        },
        async register(username: string, password: string, email: string, localized_error="")
        {
            let data: IRegisterRequest = {
                username: username,
                password: password,
                email: email
            }
            return await this.userEndpoint.axios.register(data)
        },
        isAuthorized(){
            return this.user?.authorized ?? false
        },
        setReturnUrl(url: string)
        {
            this.returnUrl = url
        },
        async followReturnUrl(){
            let returnUrl = this.returnUrl
            this.returnUrl = null

            if(returnUrl === null)
            {
                return;
            }

           await this.$router.push(returnUrl)
        },
        async fetchPermissions(){
            if(!this.isAuthorized()){
                return
            }
            this.permissions = await this.userEndpoint.axios.getPermissions()
            console.log(this.permissions)
        },
        async init(){
            await this.fetchPermissions()
        }
    },
    getters: {
        household: state => {return state.user?.household?.id ?? -1},
        userSet: state => {return state.user !== null},
        isAdmin: state => { return state.permissions.admin ?? false}
    }
})