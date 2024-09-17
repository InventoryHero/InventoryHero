import {Endpoint} from "./Endpoint.ts";
import {Household, HouseholdMember} from "@/types";

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

    public async createHousehold(name: string): Promise<{success: boolean, household?: Household}> {
        const body = {
            name: name
        }
        const response = await this.internalAxios.post("/create", body)
        if(response.status === 200)
        {
            return {
                success: true,
                household: response.data?.household as Household
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false,
        }
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
            return {
                success: true,
                household: response.data?.household as Household
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false
        }
    }

    public async leaveHousehold(id: number){
        const response = await this.internalAxios.post(`/leave/${id}`)
        if(response.status === 204){
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async getMembers(id: number){
        const response = await this.internalAxios.get(`/members/${id}`)
        if(response.status === 200){
            return {
                success: true,
                members: response.data?.members as Array<HouseholdMember>
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false
        }
    }

    public async deleteHousehold(id: number){
        const response = await this.internalAxios.delete(`/${id}`)
        if(response.status === 204){
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async kickFromHousehold(householdId: number, id: number){
        const response = await this.internalAxios.post(`/kick/${householdId}/${id}`)
        if(response.status === 204){
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

    public async updateHousehold(householdId: number, updateData: Partial<Household>){
        const response = await this.internalAxios.post(`/update/${householdId}`, {
            household: updateData
        })
        if(response.status === 200){
            return {
                success: true,
                household: response.data?.household as Household
            }
        }
        this.handleNonErrorNotifications(response)
        return {
            success: false
        }
    }

    public async transferHousehold(householdId: number, username: string){
        const response = await this.internalAxios.post(`/transfer/${householdId}/${username}`)
        if(response.status === 204){
            return true
        }
        this.handleNonErrorNotifications(response)
        return false
    }

}