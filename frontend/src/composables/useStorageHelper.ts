import {StorageTypes} from "@/types";
import {StorageType} from "@/api/types/items.ts";

export default () => {

    const router = useRouter()
    const getStorageIcon = (type: StorageType) => {
        switch(type){
            case "box":
                return "mdi-package-variant"
            case "room":
                return "mdi-door"
        }
    }

    const getStoragePath = (id: string, type: StorageType) => {
        switch(type){
            case "box":
                return router.resolve({
                    name: 'BoxContentView',
                    params: {
                        id: id,
                    },
                })
            case "room":
                return router.resolve({
                    name: 'RoomContentView',
                    params: {
                        id: id,
                    },
                })
        }
    }

    return {
        getStorageIcon,
        getStoragePath
    }
}