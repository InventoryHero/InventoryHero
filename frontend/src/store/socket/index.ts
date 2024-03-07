import {defineStore} from "pinia";
import {io, Socket} from "socket.io-client";
import {getAccessToken} from 'axios-jwt'
import {useAuthStore} from "@/store";
import {notify} from "@kyvg/vue3-notification";
import {reactive} from "vue";
import useNewAxios from "@/composables/useNewAxios.ts";
import {UserEndpoint} from "@/api/http";
import {i18n} from "@/lang";

export const useSocketStore =  defineStore("socket", {
    state: () => ({
        connected: false,
        socket: null as null|Socket,
        authStore: useAuthStore(),
        errorCallback: undefined as (undefined | (() => void))
    }),
    actions: {
        async init(){
            if(this.socket === null)
            {

                this.socket = io(`/household`, {
                    extraHeaders:{
                        Authorization: `Bearer ${await getAccessToken()}`
                    }
                });
            }
        },
        async bindActions(){
            if(this.socket === null)
            {
                await this.init()
            }
            this.socket?.on("connect", () => {
                this.connected = true;
            });

            this.socket?.on("disconnect", () => {
                this.connected = false;
            });
            this.socket?.on("hi", (msg) => {
                notify({
                    title: "SOCKET",
                    text: msg,
                    type: "info"
                })
            })
            this.socket?.on("new-content", (msg: Object) => {
                console.log(msg)
                if(msg.user === this.authStore.user.username){
                    return
                }
                notify({
                    title: i18n.global.t('toasts.titles.new-content.new', {user: msg.user}),
                    text: i18n.global.t('toasts.text.new-content.new', {user: msg.user}),
                    group: 'newContent',
                    type: 'new-content',
                    data: () => {console.log('i am so great')}
                })
            })

        },
        updateHeaders(){

            getAccessToken().then((token) => {
                if(this.socket === null)
                    return
                this.socket!.io.opts.extraHeaders = {
                    Authorization: `Bearer ${token}`
                }
                this.socket.disconnect().connect()
                this.joinHousehold()

                if(this.errorCallback !== undefined){
                    this.errorCallback()
                    this.errorCallback = undefined
                }
            })

        },
        joinHousehold(){
            this.socket?.emit("join", {
                household: this.authStore.household
            })
        },
        leaveHousehold(){
            this.socket?.emit('leave', {
                household: this.authStore.household
            })
        },
        sayHi(){
            this.socket?.emit('hi', {
                household: this.authStore.household
            }, (data: Object) => {this.socketErrorHandler(data, this.sayHi)} )
        },
        socketErrorHandler(data: Object, callback: () => void){
            const socketStore = useSocketStore()
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
            this.socket?.disconnect()
            this.socket = null
        }
    }
})