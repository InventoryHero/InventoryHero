import {getAccessToken, getBrowserLocalStorage} from "axios-jwt";
import {io} from "socket.io-client";
import {applyStorage} from 'axios-jwt/dist/src/applyStorage'


export const getStorage = getBrowserLocalStorage;
applyStorage(getStorage());
export const householdSocket =  io(`/household`, {
    extraHeaders: {
        "Authorization": `Bearer ${await getAccessToken()}`
    }
});

export const generalSocket = io("/general", {
    extraHeaders: {
        "Authorization": `Bearer ${await getAccessToken()}`
    }
})