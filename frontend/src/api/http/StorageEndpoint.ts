import {Endpoint} from "./Endpoint";
import {
    ApiProduct,
    ApiStorage,
    StorageTypes
} from "@/types";
import {Api} from "@vitejs/plugin-vue";


type GetStorageParams = {
    id?: undefined|string,
    contained: boolean
}


export class StorageEndpoint extends Endpoint{
    protected subroute: string = ""
    protected type: StorageTypes = StorageTypes.NoStorage
    constructor(type: StorageTypes = StorageTypes.AllStorage){
        super(true, `/storage`)
        this.type = type

        switch(type){
            case StorageTypes.Location:
                this.subroute = "/location"
                break
            case StorageTypes.Box:
                this.subroute = '/box'
                break
            case StorageTypes.AllStorage:
                this.subroute = '/all'
                break
            default:
                console.error("UNSUPPORTED TYPE")

        }
    }


    public async getStorageType({
        id = undefined as undefined|string,
        contained = true
    } = {}){
        let url = this.subroute
        if(id !== undefined){
            url += `/${id}`
        }
        let params = {
            params: {
                contained: contained
            }
        }

        let response = await this.internalAxios.get(url, params)
        if(response.status === 200)
        {
            return response.data
        }
        this.handleNonErrorNotifications(response);
        return []
    }

    protected async getStorageContent(id: string = ""){
        if(this.type <= StorageTypes.NoStorage || this.type > StorageTypes.Location)
        {
            console.error("INVALID CALL FOR GET STORAGE CONTENT")
            return
        }
        let url = `${this.subroute}/content/${id}`
        let response = await this.internalAxios.get(url)
        if(response.status === 200)
        {
            return response.data?.content ?? {}
        }
        this.handleNonErrorNotifications(response)
        return {}
    }

    public async deleteStorage(id: number|null){
        if(this.type <= StorageTypes.NoStorage || this.type > StorageTypes.Location)
        {
            console.error("INVALID CALL FOR DELETE")
            return
        }
        if(id === null)
        {
            // TODO NOTIFY
            console.error("DELETING NULL")
            return false;
        }
        let url = `${this.subroute}/${id}`
        let response = await this.internalAxios.delete(url)
        if(response.status === 204)
        {
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    protected async createStorage(data: Partial<Storage>){
        if(this.type <= StorageTypes.NoStorage || this.type > StorageTypes.Location)
        {
            console.error("INVALID CALL FOR CREATE")
            return {
                success: false,
                newStorage: undefined
            }
        }

        let url = `${this.subroute}/add`
        let response = await this.internalAxios.post(url, data)
        if(response.status === 201)
        {
            return {
                success: true,
                newStorage: response.data
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            newStorage: undefined
        }
    }


    protected async getName(id: number){
        if(this.type <= StorageTypes.NoStorage || this.type > StorageTypes.Location)
        {
            console.error("INVALID CALL FOR DELETE")
            return
        }


        let url = `${this.subroute}/${id}/name`
        let response = await this.internalAxios.get(url)
        if(response.status === 200)
        {
            return response.data.name ?? ""
        }
        this.handleNonErrorNotifications(response)
        return ""
    }
}




// TODO LOCALIZATION FOR ERRORS
export class LocationEndpoint extends StorageEndpoint{
    constructor(){
        super(StorageTypes.Location)
    }
    public async getLocations(params :Partial<GetStorageParams> =  {
        id: undefined,
        contained: true
    }){
        let data = await this.getStorageType(params)
        return data as Array<ApiStorage>
    }

    public async getContent(id: number){
        let data = await this.getStorageContent(id.toString())
        return {
            boxes: data.boxes,
            products: data.products
        }
    }

    public async updateLocation(id: number|null, updatedData: Partial<ApiStorage>)
    {
        if(id === null)
        {
            // TODO NOTIFY
            return {
                updated: undefined
            }
        }

        let data = {
            storage: updatedData
        }

        let url = `${this.subroute}/${id}`
        let response = await this.internalAxios.post(url, data)
        if(response.status === 200)
        {
            return {
                updated: response.data.updated as ApiStorage
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            updated: undefined
        }
    }

    public async createLocation(data: Partial<ApiStorage>){
        const {success, newStorage} = await this.createStorage(data)

        return {
            success,
            newLocation: newStorage as ApiStorage
        }
    }

    public async getLocationName(id: number|null){
        if(id === null)
        {
            // TODO NOTIFY
            console.error("GETTING NAME OF NULL")
            return ""
        }
        return await this.getName(id)
    }
}

export class BoxEndpoint extends StorageEndpoint{
    constructor(){
        super(StorageTypes.Box)
    }
    public async getBoxes(params:Partial<GetStorageParams>){
        let data = await this.getStorageType(params)
        return data as Array<ApiStorage>
    }

    public async getContent(id: number|null){
        if(id === null){
            console.error("TRYING TO GET NULL CONTENT")
            return {
                products: [] as Array<ApiProduct>
            }
        }

        let data = await this.getStorageContent(id.toString())
        return {
            products: (data?.products ?? []) as Array<ApiProduct>
        }
    }

    public async updateBox(id: number|null, updatedData: Partial<ApiStorage>): Promise<{updated: ApiStorage|undefined}>
    {
        if(id === null)
        {
            // TODO NOTIFY
            return {
                updated: undefined
            }
        }

        let data = {
            storage: updatedData
        }

        let url = `${this.subroute}/${id}`
        let response = await this.internalAxios.post(url, data)
        if(response.status === 200)
        {
            return {
                updated: response.data.updated as ApiStorage
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            updated: undefined
        }
    }

    public async createBox(data: Partial<ApiStorage>){
        const {success, newStorage} = await this.createStorage(data)

        return {
            success,
            newBox: newStorage as ApiStorage
        }
    }

    public async getBoxName(id: number|null){
        if(id === null)
        {
            // TODO NOTIFY
            console.error("GETTING NAME OF NULL")
            return ""
        }
        return await this.getName(id)
    }
}
