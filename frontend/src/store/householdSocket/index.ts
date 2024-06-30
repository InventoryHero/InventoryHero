import {defineStore} from "pinia";
import {householdSocket} from '@/plugins/connections'
import {getAccessToken} from 'axios-jwt'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {i18n} from "@/lang";
import {notify} from "@kyvg/vue3-notification";

export const useHouseholdSocket =  defineStore("socket", {
    state: () => ({
        authStore: useAuthStore(),
        errorCallback: undefined as (undefined | (() => void))
    }),
    actions: {
        bindActions(){
            householdSocket.on("hi", (msg) => {
                notify({
                    title: "SOCKET",
                    text: msg,
                    type: "info"
                })
            })
            householdSocket.on("new-content", (msg: string) => {
                let response: SocketResponse = JSON.parse(msg)
                let content: UpdateContent = response.content as UpdateContent
                if(content.user === this.authStore.user.username){
                    return
                }
                notify({
                    title: i18n.global.t('toasts.titles.new-content.new', {user: content.user}),
                    text: i18n.global.t('toasts.text.new-content.new', {user: content.user}),
                    group: 'newContent',
                    type: 'new-content',
                    data: () => {console.log('i am so great')}
                })
            })

        },
        updateHeaders(){
            getAccessToken().then((token) => {
                householdSocket.io.opts.extraHeaders = {
                    Authorization: `Bearer ${token}`
                }
                householdSocket.disconnect()
                householdSocket.connect()
                this.joinHousehold()

                if(this.errorCallback !== undefined){
                    this.errorCallback()
                    this.errorCallback = undefined
                }
            })

        },
        joinHousehold(){
            householdSocket.emit("join", {
                household: this.authStore.household
            })
        },
        leaveHousehold(){
            householdSocket.emit('leave', {
                household: this.authStore.household
            })
        },
        sayHi(){
            householdSocket.emit('hi', {
                household: this.authStore.household
            }, (data: string) => {
                let response: SocketResponse = JSON.parse(data)
                this.socketErrorHandler(response, this.sayHi)
            } )
        },
        socketErrorHandler(data: SocketResponse, callback: () => void){
            const socketStore = useHouseholdSocket()
            const userEndpoint = useNewAxios("user")
            let endpoint: UserEndpoint = userEndpoint.axios as UserEndpoint
            switch(data.status){
                case "join_first":
                    console.log("NEED TO JOIN HOUSEHOLD BEFORE INTERACTION POSSIBLE")
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
            console.log("disconnecting ... ")
            householdSocket.disconnect()
        }
    }
})