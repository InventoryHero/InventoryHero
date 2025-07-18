import {AxiosInstance} from "axios";
import {
    CategoryReadSchema,
    ItemCreateSchema,
    ItemDetailReadSchema, ItemInstanceCreate,
    ItemReadSchema,
    ItemSummarySchema, ItemUpdateSchema,
    ItemInstanceUpdateData
} from "@/api/types/items.ts";

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

    const createNewItem = async (item: ItemCreateSchema): Promise<ApiResponse<ItemReadSchema>> => {
        const response = await api.post("/items/create", item)
        if(response.status === 201){
            return {
                success: true,
                data: response.data,
            }
        }
        return {
            success: false,
            error: response.data
        }
    }

    const createItemInstance = async (item_id: string, item: ItemInstanceCreate): Promise<ApiResponse<ItemReadSchema>> => {
        const response = await api.post(`/items/${item_id}/create`, item)
        if(response.status === 201){
            return {
                success: true,
                data: response.data,
            }
        }
        return {
            success: false,
            error: response.data
        }
    }

    const deleteItem = async (item_id: string): Promise<ApiResponse<void>> => {
        const response = await api.delete(`/items/${item_id}/`)
        return {
            success: response.status == 204,
            error: response.data
        }
    }

    const updateItem = async(item_id: string, updateData: ItemUpdateSchema): Promise<ApiResponse<ItemReadSchema>> => {
        const response = await api.patch(`/items/${item_id}/`, updateData)
        if(response.status === 200){
            return {
                success: true,
                data: response.data as ItemReadSchema
            }
        }
        return {
            success: false,
            error: response.data
        }
    }

    const updateItemInstance = async(itemId: string, instanceId: string, updateData: ItemInstanceUpdateData): Promise<ApiResponse> => {
        const response = await api.patch(`/items/${itemId}/${instanceId}`, updateData)
        return {
            success: response.status == 204,
            error: response.data
        }
    }

    const deleteInstances = async(itemId: string, instanceId: string): Promise<ApiResponse> => {
        const response = await api.delete(`/items/${itemId}/${instanceId}`)
        return {
            success: response.status == 204,
            error: response.data
        }
    }

    const addItemInstance = async (itemId: string, instanceId: string): Promise<ApiResponse<void>> => {
        const response = await api.post(`/items/${itemId}/${instanceId}/add`)
        return {
            success: response.status == 204,
            error: response.data
        }
    }

    return {
        getAllItemsSummary,
        getAllCategories,
        getItemDetails,
        consumeItemInstance,
        createNewItem,
        createItemInstance,
        deleteItem,
        updateItem,
        updateItemInstance,
        deleteInstances,
        addItemInstance
    }

}