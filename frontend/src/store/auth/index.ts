import {defineStore} from "pinia";
import {Household, IRegisterRequest} from "@/types";
import {isLoggedIn} from "axios-jwt";
import {useLocalStorage} from "@vueuse/core";
import useNewAxios from "@/composables/useNewAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useSocketStore} from "@/store";





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
        userEndpoint: useNewAxios("user") as {axios: UserEndpoint},
        returnUrl: null as (null|string),
    }),
    actions: {
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
            const socketStore = useSocketStore()
            socketStore.leaveHousehold()



            const success = await this.userEndpoint.axios.logout()
            this.user = null;
            if(!success)
            {
                // TODO notify
            }
            this.$router.push("/login")
        },
        async changeHousehold(household: Household | undefined)
        {
            if(household === undefined)
            {
                return;
            }

            const socketStore = useSocketStore()
            socketStore.leaveHousehold()
            this.user.household  = {
                id: household.id,
                name: household.name
            }
            socketStore.joinHousehold()
        },
        async destroy(){
            const socketStore = useSocketStore()
            socketStore.leaveHousehold()
            this.user = null;
            await this.$router.push("/login")
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
        }
    },
    getters: {
        household: state => {return state.user?.household?.id ?? -1},
        userSet: state => {return state.user !== null}
    }
})