
import {useAuthStore} from "./auth";
import {createPinia} from "pinia";
import {useConfigStore} from "@/store/config";
import {useHouseholdSocketStore} from "./sockets/householdSocketStore.ts";
import {useGeneralSocketStore} from "./sockets/generalSocketStore.ts"
import productStore from "./productStore"
import storageStore from "./storageStore"
import printSettings from "@/store/printSettings";
import notifications from "@/store/notifications";
import scroll from "@/store/scroll"


const pinia = createPinia()

export default  pinia
export {
    useAuthStore,
    useConfigStore,
    useHouseholdSocketStore,
    useGeneralSocketStore,
    productStore as useProducts,
    storageStore as useStorage,
    printSettings as usePrintSettings,
    notifications as useNotificationStore,
    scroll as useScrollPositionStore
}