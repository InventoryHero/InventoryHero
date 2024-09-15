import { StorageTypes} from "@/types";


export default (type: StorageTypes) => {

    return computed(() => {
        switch (type) {
            case StorageTypes.Location:
                return "mdi-archive-marker"
            case StorageTypes.Box:
                return "mdi-package-variant"
            default:
                return "mdi-archive-off"
        }
    });

}