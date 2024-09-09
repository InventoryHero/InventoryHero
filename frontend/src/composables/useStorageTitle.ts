import {ApiStorage, StorageTypes} from "@/types";


export default (storage: Ref<ApiStorage|undefined|null>) => {


    const icon = computed(() => {
        switch (storage.value?.type ?? -1) {
            case StorageTypes.Location:
                return "mdi-archive-marker"
            case StorageTypes.Box:
                return "mdi-package-variant"
            default:
                return "mdi-archive-off"
        }
    });

    const name = computed(() => storage.value?.name ?? '');

    return {
        name,
        icon
    }
}