import {Endpoint} from "./Endpoint.ts";
import {Household, Product, ProductLocations, ProductOnly} from "@/types";

export class ProductEndpoint extends Endpoint{

    constructor(){
        super(true, "/products")
    }

    public async getProducts({
        id = undefined as (undefined|string),
        getStoredAt = false
    } = {}){

        let url = ""
        if(id !== undefined){
            url += `${id}/`
        }
        let response = await this.internalAxios.get(url,
        {
            params: {
                storedAt: getStoredAt ? true : undefined

            }
        })

        if(response.status === 200){
            return response.data as Array<Product>
        }
        this.handleNonErrorNotifications(response)
        return [] as Array<Product>
    }

    public async deleteProduct(id: number|null){
        if(id === null)
        {
            console.error("TRYING TO DELETE NULL")
            return false
        }
        let response = await this.internalAxios.delete(`/${id}`)
        if(response.status === 204)
        {
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async updateProduct(id: number|null, update: Partial<Product>){
        if(id === null)
        {
            console.error("TRYING TO DELETE NULL")
            return {
                success: false,
                product: undefined as Product|undefined
            }
        }
        let data = {
            product: update
        }
        let response = await this.internalAxios.post(`/update/${id}`, data)
        if(response.status === 200)
        {
            return {
                success: true,
                product: response.data.updated as Product|undefined
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            product: undefined as Product|undefined
        }
    }

    public async deleteProductAt(id: number|null){
        if(id === null)
        {
            console.error("TRYING TO DELETE NULL")
            return false
        }

        let response = await this.internalAxios.delete(`/stored/${id}`)
        if(response.status === 200)
        {
            return true
        }
        this.handleNonErrorNotifications(response)
        return false

    }

    public async updateProductAt(id: number|null, update: Partial<ProductLocations>){
        if(id === null)
        {
            console.error("TRYING TO DELETE NULL")
            return {
                success: false,
                updated: undefined as ProductLocations|undefined,
                deleted: undefined as ProductLocations|undefined
            }
        }
        let response = await this.internalAxios.post(`/stored/${id}`, {
            amount: update.amount,
            storage: update.storage?.id ?? undefined,
            storage_type: update.storage_type
        })
        if(response.status === 200)
        {
            return {
                success: true,
                updated: response.data.updated as ProductLocations|undefined,
                deleted: (response.data.deleted ?? undefined) as ProductLocations|undefined
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            updated: undefined as ProductLocations|undefined,
            deleted: undefined as ProductLocations|undefined
        }
    }

    public async createProduct(data: Partial<ProductOnly & ProductLocations>){
        let url = "/create"
        if(data.id !== undefined && data.id !== null)
        {
            url += `/${data.id}`
        }
        let response = await this.internalAxios.post(url, {
            ...data,
            id: undefined
        })
        if(response.status === 200){
            return {
                success: true,
                product: response.data as Product
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            product: undefined
        }
    }


}