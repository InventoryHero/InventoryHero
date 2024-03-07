import {Storage} from "@/types";
import { Ref, toValue} from 'vue';

export default (currentStorage: Ref<Storage|undefined|null>, newStorage: Ref<Storage|undefined|null>) => {
    const current = toValue(currentStorage)
    const newS = toValue(newStorage)

    if(current === undefined || newS === undefined || current === null || newS === null)
    {
        return {
            same: current === newS
        }
    }

    if(current.type !== newS.type){
        return {
            same: false
        }
    }

    if(current.id !== newS.id)
    {
        return {
            same: false
        }
    }

    return {
        same: true
    }
}