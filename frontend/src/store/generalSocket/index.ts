import {defineStore} from "pinia";
import {generalSocket, householdSocket} from '@/plugins/connections'
import {getAccessToken} from 'axios-jwt'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";




export const useGeneralSocketStore =  defineStore("generalSocket", {
    state: () => ({
        authStore: useAuthStore(),
        errorCallback: undefined as (undefined | (() => void))
    }),
    actions:{
        bindActions(){
            generalSocket.on("connect", () => {
                console.log("GENERAL SOKCET CONNECTED")
            });

            generalSocket.on("disconnect", () => {
                console.log("GENERAL SOCKET DISCONNECTED")
            });
        },
        hi(){
            generalSocket.emit(
                'hi',
                {},
                (data: string) => {
                    console.log(data)
                    let response: SocketResponse = JSON.parse(data)
                    this.socketErrorHandler(response, () => {})
                }
            )
        },
        isUserNameFree(username: string, errorCallback: (isTaken:boolean) => void){
          generalSocket.emit(
              'username',
              {
                "username": username
              },
              (data: string) => {
                  let response: SocketResponse = JSON.parse(data)
                  this.socketErrorHandler(response, errorCallback)
              }
          )
        },

        updateHeaders(){
            getAccessToken().then((token) => {
                generalSocket.io.opts.extraHeaders = {
                    Authorization: `Bearer ${token}`
                }
                generalSocket.disconnect()
                generalSocket.connect()

                if(this.errorCallback !== undefined){
                    this.errorCallback()
                    this.errorCallback = undefined
                }
            })

        },

        socketErrorHandler(data: SocketResponse, callback: () => void){
            const userEndpoint = useNewAxios("user")
            let endpoint: UserEndpoint = userEndpoint.axios as UserEndpoint
            console.log(data)
            switch(data.status){
                case "token_revoked":
                case "expired_signature":
                    // DUMMY REQUEST TO REFRESH TOKEN
                    this.errorCallback = callback
                    endpoint.getUser().then(() => {
                        this.updateHeaders()
                    })
                    return
                case "ok":
                    console.log("SUCCESS", data.content)
                    break
                case "username_taken":
                    console.log("USERNAME IS TAKEN");
                    callback()
                    return
            }
        },
    }
})