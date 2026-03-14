import {useEventBus} from "@vueuse/core";



export default useEventBus<string|undefined>("item-added")