import {useEventBus} from "@vueuse/core";
import {CategoryReadSchema} from "@/api/types/items.ts";



export default useEventBus<CategoryReadSchema>("category-added")