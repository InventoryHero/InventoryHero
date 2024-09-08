import {ApiStorage, StorageTypes} from "@/types";
import {computed, Ref, toValue} from 'vue';

export default (storage: Ref<ApiStorage|undefined|null>) => {


    const icon = computed(() => {
        switch (storage.value?.type ?? -1) {
            case StorageTypes.Location:
                return 'fa:fas fa-location-dot';
            case StorageTypes.Box:
                return 'fa:fas fa-boxes';
            default:
                return 'fa:fas fa-ban';
        }
    });

    const name = computed(() => storage.value?.name ?? '');

    return {
        name,
        icon
    }
}