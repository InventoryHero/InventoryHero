import {Storage, StorageTypes} from "@/types";
import { Ref, toValue} from 'vue';

export default (storage: Ref<Storage|undefined|null>) => {
    const s = toValue(storage)

    let icon = ""
    switch(s?.type ?? -1)
    {
        case StorageTypes.Location:
            icon = 'fa:fas fa-location-dot'
            break
        case StorageTypes.Box:
            icon =  'fa:fas fa-boxes'
            break
        default:
            icon = 'fa:fas fa-ban'
    }

    return {
        name: s?.name ?? '',
        icon: icon
    }
}