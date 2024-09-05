
import {useAuthStore} from "./auth";
import {createPinia} from "pinia";
import {useConfigStore} from "@/store/config";
import {useHouseholdSocket} from "./householdSocket";
import {useGeneralSocketStore} from "./generalSocket"
import {useProducts} from "./products"


const pinia = createPinia()

export default  pinia
export {useAuthStore, useConfigStore, useHouseholdSocket, useGeneralSocketStore, useProducts}