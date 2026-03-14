import { AxiosInstance } from 'axios'
import {
  BoxResponseSchema,
  BoxUpdateSchema,
  RoomResponseSchema,
  RoomUpdateSchema,
  StorageCreateSchema,
  StorageType
} from '@/api/types/storage.ts'
import { ApiResponse } from '@/api/types/ApiResponse.ts'
import { ItemSummarySchema } from '@/api/types/items.ts'

type AnyStorageResponse = BoxResponseSchema | RoomResponseSchema
type AnyStorageUpdateSchema = BoxUpdateSchema | RoomUpdateSchema

export default (api: AxiosInstance) => {
  const getAllStorage = async (
    storage_type: StorageType | undefined = undefined
  ): Promise<ApiResponse<Array<AnyStorageResponse>>> => {
    const response = await api.get('/storage/all', {
      params: {
        storage_type: storage_type
      }
    })
    if (response.status === 200) {
      return {
        success: true,
        data: response.data as Array<AnyStorageResponse>
      }
    }
    return {
      success: false
    }
  }

  const getStorageItems = async (
    id?: string
  ): Promise<ApiResponse<Array<ItemSummarySchema>>> => {
    let url = `/storage/${id}/items`

    const response = await api.get(url)
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<Array<ItemSummarySchema>>
    }
    return {
      success: false
    }
  }

  const getStorageBoxes = async (
    id?: string
  ): Promise<ApiResponse<Array<BoxResponseSchema>>> => {
    let url = `/storage/${id}/boxes`
    const response = await api.get(url)
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<Array<BoxResponseSchema>>
    }
    return {
      success: false
    }
  }

  const getStorageDetail = async (
    id?: string
  ): Promise<ApiResponse<AnyStorageResponse>> => {
    let url = `/storage/${id}/detail`

    const response = await api.get(url)
    if (response.status === 200) {
      return {
        success: true,
        data: response.data
      } as ApiResponse<AnyStorageResponse>
    }
    return {
      success: false
    }
  }

  const createStorage = async (
    createSchema: StorageCreateSchema
  ): Promise<ApiResponse<AnyStorageResponse>> => {
    let url = `/storage/create`
    try {
      const response = await api.post(url, createSchema)
      if (response.status === 201) {
        return {
          success: true,
          data: response.data
        } as ApiResponse<AnyStorageResponse>
      }
    } catch (error) {
      return {
        success: false,
        error: error
      }
    }
    return {
      success: false
    }
  }
  const deleteStorage = async (id: string): Promise<ApiResponse<void>> => {
    let url = `/storage/${id}/`
    const response = await api.delete(url)
    const success = response.status === 204
    return {
      success: success,
      error: !success ? response.data : undefined
    }
  }

  const updateStorage = async (
    id: string,
    updateData: AnyStorageUpdateSchema
  ): Promise<ApiResponse<AnyStorageResponse>> => {
    const response = await api.put(`/storage/${id}/`, updateData)
    const success = response.status === 200
    return {
      success: success,
      data: success ? response.data : undefined,
      error: !success ? response.data : undefined
    }
  }

  return {
    getAllStorage,
    getStorageDetail,
    getStorageItems,
    getStorageBoxes,
    createStorage,
    deleteStorage,
    updateStorage
  }
}
