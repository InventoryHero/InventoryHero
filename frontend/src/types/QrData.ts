import {StorageTypes} from "@/types/api.ts";

interface StorageQrData{
    id: number,
    household_id: number,
    storage_type: StorageTypes,
    name?: string
}

export type {StorageQrData}