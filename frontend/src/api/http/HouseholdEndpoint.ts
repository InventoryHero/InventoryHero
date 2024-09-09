import {Endpoint} from "./Endpoint.ts";
import {Household} from "@/types";

export class HouseholdEndpoint extends Endpoint{

    constructor(){
        super(false, "/household")
    }

    public async getHouseholds(): Promise<Array<Household>> {
        const response = await this.internalAxios.get("/all")
        if(response.status === 200)
        {
            return response.data as Array<Household>
        }
        this.handleNonErrorNotifications(response)
        return []
    }

    public async createHousehold(name: string): Promise<boolean> {
        const body = {
            name: name
        }
        const response = await this.internalAxios.post("/create", body)
        if(response.status === 200)
        {
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async createInviteCode(id: number){
        const response = await this.internalAxios.get(`/code/${id}`)
        if(response.status === 200)
        {
            return {
                success: true,
                code: response.data.code
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            code: ""
        }
    }

    public async getHouseholdMeta(invite: string){
        const response = await this.internalAxios.get(`/meta/${invite}`)
        if(response.status === 200)
        {
            return {
                success: true,
                owner: response.data.owner,
                name: response.data.name
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
            owner: "",
            name: ""
        }
    }

    public async joinHousehold(invite: string)
    {
        const response = await this.internalAxios.get(`/join/${invite}`)
        if(response.status === 200)
        {
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

}