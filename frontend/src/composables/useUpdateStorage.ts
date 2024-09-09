import {ApiStorage} from "@/types";
import {StorageTypes} from "@/types";
import {ref, Ref, toValue} from 'vue';
import {notify} from "@kyvg/vue3-notification";


export default (maybeRefOrGetter: Ref<Array<ApiStorage>>, storage: ApiStorage|undefined = undefined, overlayStorage: Ref<ApiStorage|undefined> = ref(undefined)) =>
{
    if (storage === undefined)
    {
        return {storage: undefined, index: -1};
    }

    const content = toValue(maybeRefOrGetter)

    let i = 0
    for(; i < content.length; i++)
    {
        if(content[i]?.id !== storage.id)
        {
            continue
        }
        content[i].name = storage.name
        switch(storage.type)
        {
            case StorageTypes.Box:
                content[i].storageId = storage?.id
                content[i].storage = storage
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

