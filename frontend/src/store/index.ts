
import {useAuthStore} from "./auth";
import {createPinia} from "pinia";
import {useConfigStore} from "@/store/config";
import {useHouseholdSocket} from "./householdSocket";
import {useGeneralSocketStore} from "./generalSocket"
import productStore from "./productStore"
import storageStore from "./storageStore"


const pinia = createPinia()

export default  pinia
export {
    useAuthStore,
    useConfigStore,
    useHouseholdSocket,
    useGeneralSocketStore,
    productStore as useProducts,
    storageStore as useStorage
}