import {defineStore} from "pinia";
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {io} from "socket.io-client";
import {getAccessToken} from "axios-jwt";
import useAxios from "@/composables/useAxios.ts";
import {SocketResponse} from "@/types/sockets.ts";

type DefaultCallback = () => void
type TakenCallback = (is_taken: boolean) => void

type Callback = DefaultCallback | TakenCallback;





const generalSocket = io("/general", {
    autoConnect: false
})

export const useGeneralSocketStore =  defineStore("generalSocket", {
    state: () => ({
        authStore: useAuthStore(),
    }),
    actions:{
        bindActions() {
            generalSocket.on("connect", () => {
                console.log("GENERAL SOCKET CONNECTED")
            })
            generalSocket.on('reconnect', () => {
                console.log("GENERAL SOCKET RECONNECTING")
            })
            generalSocket.on("connect_error", () => {
                console.log("GENERAL SOCKET CONNECT ERROR")
            })
            generalSocket.on("disconnect", () => {
                console.log("GENERAL SOCKET DISCONNECTED")
            })
            generalSocket.on("kicked", (data: SocketResponse) => {
                if(data.status !== "ok"){
                    return
                }
                const content = data.content as {household: number}
                this.authStore.removeHousehold(content.household, "kick")
            })
            generalSocket.on("ownership_received", (data: SocketResponse) => {
                if(data.status !== "ok"){
                    return
                }

                const content = data.content as {household: number}
                this.authStore.ownHousehold(content.household)
            })
            generalSocket.on("deleted", (data: SocketResponse) => {
                const content = data.content as {household: number}
                this.authStore.removeHousehold(content.household, "deleted")
            })

        },
        leave(){
          generalSocket.disconnect()
        },
        isUserNameTaken(username: string): Promise<boolean> {
            return new Promise((resolve, reject) => {
                generalSocket.emit(
                    'username',
                    { "username": username },
                    (data: SocketResponse) => {
                        switch (data.status) {
                            case "username_free":
                                resolve(false); // Username is not taken
                                break;
                            case "username_taken":
                                resolve(true); // Username is taken
                                break;
                            case "token_revoked":
                            case "expired_signature":
                                this.renewToken()
                                reject("token_expired")
                                return
                            default:
                                reject(new Error("Unexpected response from server"))
                        }
                    }
                );
            });
        },
        isEmailTaken(email: string): Promise<boolean>{
            return new Promise((resolve, reject) => {
                generalSocket.emit(
                    'email',
                    { "email": email },
                    (data: SocketResponse) => {
                        switch (data.status) {
                            case "email_free":
                                resolve(false); // Username is not taken
                                break;
                            case "email_taken":
                                resolve(true); // Username is taken
                                break;
                            case "token_revoked":
                            case "expired_signature":
                                this.renewToken()
                                reject("token_expired")
                                return
                            default:
                                reject(new Error("Unexpected response from server"))
                        }
                    }
                );
            });
        },
        updateHeaders(token?: string){
            generalSocket.io.opts.extraHeaders = {
                Authorization: `Bearer ${token}`
            }
            generalSocket.disconnect()
            if(token){
                generalSocket.connect()
                this.bindActions()
            }
        },
        renewToken(){
            const {axios} = useAxios<UserEndpoint>("user")
            axios.getUser().then(() => {
                getAccessToken().then((token) => {
                    this.updateHeaders(token)
                })
            })
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        socketErrorHandler(data: SocketResponse, callback: Callback){
            const userEndpoint = useNewAxios("user")
            const endpoint: UserEndpoint = userEndpoint.axios as UserEndpoint
            switch(data.status){
                case "token_revoked":
                case "expired_signature":
                    // DUMMY REQUEST TO REFRESH TOKEN
                    endpoint.getUser().then(() => {
                        getAccessToken().then((token) => {
                            this.updateHeaders(token)
                        })
                    })
                    return
                case "ok":
                    break
            }
        },
    }
})