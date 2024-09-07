import {defineStore} from "pinia";
import {generalSocket, socket} from '@/plugins/connections'
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
        isEmailFree(email: string, errorCallback: TakenCallback){
            generalSocket.emit(
                'email',
                {
                    "email": email
                },
                (data: SocketResponse) => {
                    switch(data.status){
                        case "email_free":
                            errorCallback(false)
                            return;
                        case "email_taken":
                            errorCallback(true)
                            return;
                        default:
                            this.socketErrorHandler(data, errorCallback)
                    }
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
            })

        },

        socketErrorHandler(data: SocketResponse, callback: Callback){
            const userEndpoint = useNewAxios("user")
            let endpoint: UserEndpoint = userEndpoint.axios as UserEndpoint
            switch(data.status){
                case "token_revoked":
                case "expired_signature":
                    // DUMMY REQUEST TO REFRESH TOKEN
                    endpoint.getUser().then(() => {
                        this.updateHeaders(callback as DefaultCallback)
                    })
                    return
                case "ok":
                    break
            }
        },
    }
})