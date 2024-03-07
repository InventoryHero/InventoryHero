
import {useAuthStore} from "./auth";
import {createPinia} from "pinia";
import {useConfigStore} from "@/store/config";
import {useSocketStore} from "@/store/socket";


const pinia = createPinia()

export default  pinia
export {useAuthStore, useConfigStore, useSocketStore}