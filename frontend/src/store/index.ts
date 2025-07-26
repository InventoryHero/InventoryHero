
import {createPinia} from "pinia";
import {useHouseholdSocketStore} from "./sockets/householdSocketStore.ts";
import {useGeneralSocketStore} from "./sockets/generalSocketStore.ts"



const pinia = createPinia()

export default  pinia
export {
    useHouseholdSocketStore,
    useGeneralSocketStore,
}