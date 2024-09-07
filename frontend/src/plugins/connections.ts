import {getAccessToken, getBrowserLocalStorage, applyStorage} from "axios-jwt";
import {io} from "socket.io-client";


export const getStorage = getBrowserLocalStorage;
applyStorage(getStorage());
const socket = io("/household", {
    autoConnect: false
})
const generalSocket = io("/general", {
    autoConnect: false
})

export {
    socket,
    generalSocket
}