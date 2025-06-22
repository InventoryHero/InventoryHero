import {AxiosInstance} from "axios";
import {BoxResponseSchema, RoomResponseSchema, StorageType} from "@/api/types/storage.ts";
import {ApiResponse} from "@/api/types/ApiResponse.ts";
import {ItemDetailReadSchema, ItemSummarySchema} from "@/api/types/items.ts";

type test = BoxResponseSchema | RoomResponseSchema

export default (api: AxiosInstance) => {

    const getAllStorage = async (storage_type: StorageType|undefined): Promise<ApiResponse<Array<test>>> => {
        const response = await api.get("/storage/all", {
            params: {
                storage_type:storage_type
            }
        });
        if(response.status === 200){
            return {
                success: true,
                data: response.data as Array<test>
            }
        }
        return {
            success: false
        }
    }

    const getStorageItems = async (id?: string): Promise<ApiResponse<Array<ItemSummarySchema>>> => {
        let url = `/storage/${id}/items`

        const response = await api.get(url)
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<Array<ItemSummarySchema>>
        }
        return {
            success: false
        }
    }

    const getStorageBoxes = async(id?: string): Promise<ApiResponse<Array<BoxResponseSchema>>> => {
        let url = `/storage/${id}/boxes`
        const response = await api.get(url)
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<Array<BoxResponseSchema>>
        }
        return {
            success: false
        }
    }

    const getStorageDetail = async (id?: string): Promise<ApiResponse<test>> => {
        let url = `/storage/${id}/detail`

        const response = await api.get(url)
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<test>
        }
        return {
            success: false
        }
    }

    return {
        getAllStorage,
        getStorageDetail,
        getStorageItems,
        getStorageBoxes,
    }

}