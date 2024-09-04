import {getAccessToken, getBrowserLocalStorage, applyStorage} from "axios-jwt";
import {io} from "socket.io-client";


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