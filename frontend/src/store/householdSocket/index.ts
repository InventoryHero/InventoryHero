import {defineStore} from "pinia";
import {generalSocket, socket} from '@/plugins/connections'
import {getAccessToken} from 'axios-jwt'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {i18n} from "@/lang";
import {notify} from "@kyvg/vue3-notification";
import {io} from "socket.io-client";

export const useHouseholdSocket =  defineStore("socket", {
    state: () => ({
        authStore: useAuthStore(),
        errorCallback: undefined as (undefined | (() => void)),
        socket: undefined as SocketIO|undefned
    }),
    actions: {
        bindActions(){
            socket.on('connect', () => {
                console.log("connecting")
            })
            socket.on('reconnect', () => {
                console.log("reconnecterror")
            })
            socket.on("connect_error", () => {
                console.log("connecterror")
            })
            socket.on("new-content", (msg: string) => {
                let response: SocketResponse = JSON.parse(msg)
                let content: UpdateContent = response.content as UpdateContent
                console.log("NEW CONTENT HERE")
                if(content.user === this.authStore.user.username){
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
        updateHeaders(){
            console.log(socket)
            this.socket?.disconnect()
            getAccessToken().then((token) => {
                socket.io.opts.extraHeaders = {
                    "Authorization": `Bearer ${token}`
                }
                console.log(socket)
                socket.disconnect()
                socket.connect()

                this.bindActions()
                this.joinHousehold()
            })
        },
        joinHousehold(){
            if(this.authStore.household === -1){
                return
            }
            socket.emit("join", {
                household: this.authStore.household
            }, (data: string) => {
                console.log(data)

            } )
        },
        leaveHousehold(){
            socket.emit('leave', {
                household: this.authStore.household
            })
        },
        sayHi(){
            socket.emit('hi', {
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
                    console.log("HALLO")
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
            socket.disconnect()
        }
    }
})