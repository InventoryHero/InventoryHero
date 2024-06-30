
import {useAuthStore} from "./auth";
import {createPinia} from "pinia";
import {useConfigStore} from "@/store/config";
import {useSocketStore} from "./householdSocket";
import {useGeneralSocketStore} from "./generalSocket"


const pinia = createPinia()

export default  pinia
export {useAuthStore, useConfigStore, useSocketStore, useGeneralSocketStore}