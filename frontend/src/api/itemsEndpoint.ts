import {AxiosInstance} from "axios";
import {CategoryReadSchema, ItemDetailReadSchema, ItemSummarySchema} from "@/api/types/items.ts";
import {ApiResponse} from "@/api/types/ApiResponse.ts";
import {HouseholdPublic} from "@/api/types/households.ts";

export default (api: AxiosInstance) => {

    const getAllItemsSummary = async (): Promise<ApiResponse<Array<ItemSummarySchema>>> => {
        let url = "/items/overview"
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

    const getAllCategories = async (): Promise<ApiResponse<Array<CategoryReadSchema>>> => {
        const response = await api.get("/categories/all")
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<Array<CategoryReadSchema>>
        }
        return {
            success: false
        }
    }

    const getItemDetails = async (id: string, fromStorage: string|undefined): Promise<ApiResponse<ItemDetailReadSchema>> => {
        const response = await api.get(`/items/${id}/`, {
            params: {
                from_storage: fromStorage
            }
        })
        if(response.status === 200){
            return {
                success: true,
                data: response.data
            } as ApiResponse<ItemDetailReadSchema>
        }
        return {
            success: false
        }
    }

    const consumeItemInstance = async (itemId: string, instanceId: string): Promise<ApiResponse<void>> => {
        const response = await api.post(`/items/${itemId}/${instanceId}/consume`)
        return {
            success: response.status == 204,
            error: response.data
        }
    }

    return {
        getAllItemsSummary,
        getAllCategories,
        getItemDetails,
        consumeItemInstance
    }

}