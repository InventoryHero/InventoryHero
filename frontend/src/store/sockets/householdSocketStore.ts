import {defineStore} from "pinia";
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {i18n} from "@/lang";
import {notify} from "@kyvg/vue3-notification";
import {io} from "socket.io-client";
import {SocketResponse} from "@/types/sockets.ts";

const householdSocket = io("/household", {
    autoConnect: false
})

export const useHouseholdSocketStore =  defineStore("socket", {
    state: () => ({
        authStore: useAuthStore(),
        errorCallback: undefined as (undefined | (() => void)),
    }),
    actions: {
        bindActions(){
            householdSocket.on('connect', () => {
                console.log("HOUSEHOLD SOCKET CONNECTED")
            })
            householdSocket.on('reconnect', () => {
                console.log("HOUSEHOLD SOCKET RECONNECTED")
            })
            householdSocket.on("connect_error", () => {
                console.log("HOUSEHOLD SOCKET CONNECT ERROR")
            })
            householdSocket.on("disconnect", () => {
                console.log("HOUSEHOLD SOCKET DISCONNECTED")
            })
            householdSocket.on("new-content", (msg: string) => {
                const response: SocketResponse = JSON.parse(msg)
                const content = response.content as { user: string }
                if(content.user === this.authStore.user?.username){
                    return
                }
                notify({
                    title: i18n.global.t('toasts.titles.new-content.new', {user: content.user}),
                    text: i18n.global.t('toasts.text.new-content.new', {user: content.user}),
                    group: 'newContent',
                    type: 'new-content',
                    data: () => {}
                })
            })



        },
        updateHeaders(token?: string){
            householdSocket.io.opts.extraHeaders = {
                "Authorization": `Bearer ${token}`
            }
            householdSocket.disconnect()
            if(token){
                householdSocket.connect()
                this.bindActions()
                this.joinHousehold()
            }
        },
        joinHousehold(){
            if(!this.authStore.household?.id){
                return
            }
            householdSocket.emit("join", {
                household: this.authStore.household.id
            })
        },
        leaveHousehold(){
            if(!this.authStore.household?.id){
                return
            }
            householdSocket.emit('leave', {
                household: this.authStore.household.id
            })
        },
        socketErrorHandler(data: SocketResponse, callback: () => void){
            const socketStore = useHouseholdSocketStore()
            const userEndpoint = useNewAxios("user")
            const endpoint: UserEndpoint = userEndpoint.axios as UserEndpoint
            switch(data.status){
                case "join_first":
                    socketStore.joinHousehold()
                    callback()
                    return
                case "token_revoked":
                case "expired_signature":
                    // DUMMY REQUEST TO REFRESH TOKEN
                    this.errorCallback = callback
                    endpoint.getUser().then(() => {
                        socketStore.updateHeaders()
                    })
                    return
            }
        },
        disconnect(){
            householdSocket.disconnect()
        }
    }
})