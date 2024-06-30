import {defineStore} from "pinia";
import {generalSocket, householdSocket} from '@/plugins/connections'
import {getAccessToken} from 'axios-jwt'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";

type DefaultCallback = () => void
type TakenCallback = (is_taken: boolean) => void

type Callback = DefaultCallback | TakenCallback;


export const useGeneralSocketStore =  defineStore("generalSocket", {
    state: () => ({
        authStore: useAuthStore(),
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
        isUserNameFree(username: string, errorCallback: TakenCallback){
          generalSocket.emit(
              'username',
              {
                "username": username
              },
              (data: SocketResponse) => {
                  switch(data.status){
                      case "username_free":
                          errorCallback(false)
                          return;
                      case "username_taken":
                          errorCallback(true)
                          return;
                      default:
                          this.socketErrorHandler(data, errorCallback)
                  }
              }
          )
        },

        updateHeaders(callback: DefaultCallback){
            getAccessToken().then((token) => {
                generalSocket.io.opts.extraHeaders = {
                    Authorization: `Bearer ${token}`
                }
                generalSocket.disconnect()
                generalSocket.connect()
                callback()
            })

        },

        socketErrorHandler(data: SocketResponse, callback: Callback){
            const userEndpoint = useNewAxios("user")
            let endpoint: UserEndpoint = userEndpoint.axios as UserEndpoint
            console.log(data)
            switch(data.status){
                case "token_revoked":
                case "expired_signature":
                    // DUMMY REQUEST TO REFRESH TOKEN
                    endpoint.getUser().then(() => {
                        this.updateHeaders(callback as DefaultCallback)
                    })
                    return
                case "ok":
                    console.log("SUCCESS", data.content)
                    break
            }
        },
    }
})