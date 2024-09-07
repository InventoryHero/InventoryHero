import {Endpoint} from "./Endpoint.ts";
import {Household, Product, ProductLocations, ProductOnly} from "@/types";
import {ApiProduct, ProductStorageMapping} from "@/types/api.ts";

export class ProductEndpoint extends Endpoint{

    constructor(){
        super(true, "/products")
    }

    public async getProducts({
        id = undefined as (undefined|string)
    } = {}): Promise<Array<ApiProduct>>{

        let url = ""
        if(id !== undefined){
            url += `/${id}`
        }
        let response = await this.internalAxios.get(url)

        if(response.status === 200){
            return response.data as Array<ApiProduct>
        }
        this.handleNonErrorNotifications(response)
        return [] as Array<ApiProduct>
    }

    public async getProductStorage(product_id: number, container: number|undefined = undefined): Promise<Array<ProductStorageMapping>> {
        let url = `/stored/${product_id}`


        let response = await this.internalAxios.get(url, {
            params: {
                storage: container
            }
        })

        if(response.status === 200){
            return response.data as Array<ProductStorageMapping>
        }
        this.handleNonErrorNotifications(response)
        return [] as Array<ProductStorageMapping>
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

    public async updateProduct(id: number|null, update: Partial<ApiProduct>): Promise<{success: boolean, updatedProduct: ApiProduct|undefined}>{
        if(id === null)
        {
            console.error("TRYING TO DELETE NULL")
            return {
                success: false,
                updatedProduct: undefined
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
                updatedProduct: response.data.updated as ApiProduct
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            updatedProduct: undefined
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

    public async updateProductAt(id: number|null, update: Partial<ProductStorageMapping>){
        if(id === null)
        {
            console.error("TRYING TO DELETE NULL")
            return {
                success: false,
                updated: undefined as ProductStorageMapping|undefined,
                deleted: undefined as ProductStorageMapping|undefined
            }
        }
        let response = await this.internalAxios.post(`/stored/${id}`, {
            amount: update.amount,
            storage: update.storage?.id,
        })
        if(response.status === 200)
        {
            return {
                success: true,
                updated: response.data.updated as ProductStorageMapping|undefined,
                deleted: (response.data.deleted ?? undefined) as ProductStorageMapping|undefined
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            updated: undefined as ProductStorageMapping|undefined,
            deleted: undefined as ProductStorageMapping|undefined
        }
    }

    public async addExistingProduct(data: Partial<ProductStorageMapping>, updateStarred: boolean, starred?: boolean){
        let url = `/create/${data.productId}`
        const response = await this.internalAxios.post(url, {
            ...data,
            productId: undefined,
            starred: updateStarred ? starred : undefined
        })
        if(response.status === 200){
            return {
                success: true
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false
        }
    }


    public async createProduct(name: string, amount: number, starred: boolean, storageId?: number){
        let url = "/create"
        let response = await this.internalAxios.post(url, {
            name, amount, starred, storageId
        })
        if(response.status === 200){
            return {
                success: true,
                product: response.data as ApiProduct
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            product: undefined
        }
    }


}