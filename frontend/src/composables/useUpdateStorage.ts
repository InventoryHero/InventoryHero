import {Box, Storage, Location} from "@/types";
import {StorageTypes} from "@/types";
import {ref, Ref, toValue} from 'vue';
import {notify} from "@kyvg/vue3-notification";


export default (maybeRefOrGetter: Ref<Array<Storage>>, storage: Storage|undefined = undefined, overlayStorage: Ref<Storage|undefined> = ref(undefined)) =>
{
    if (storage === undefined)
    {
        return {storage: undefined, index: -1};
    }

    const content = toValue(maybeRefOrGetter)

    let i = 0
    for(; i < content.length; i++)
    {
        if(content.at(i)?.id !== storage.id)
        {
            continue
        }
        content[i].name = storage.name
        switch(storage.type)
        {
            case StorageTypes.Box:
                let current: Box = content[i] as Box
                current.location = (storage as Box).location
                current.location_id = (storage as Box).location_id
                break
            case StorageTypes.Location:
                break
            default:
                i = content.length
                break
        }
        break
    }

    if(i >= content.length)
    {
        notify({
            title: 'box not found'
        })
        return {storage: undefined, index: -1};
    }

    const overlay = toValue(overlayStorage)
    if(overlay?.id === storage.id)
    {
        overlayStorage.value = content[i]
    }


    return {storage: content[i], index: i}
}

