import {Endpoint} from "./Endpoint";
import {User} from "@/types/api.ts";

export class AdministrationEndpoint extends Endpoint {
    constructor() {
        super(false, "/administration")
    }

    public async loadUsers(){
        const response = await this.internalAxios.get("/users")
        if(response.status === 200){
            return response.data.users as Array<User>
        }
        this.handleNonErrorNotifications(response)
        return [] as Array<User>
    }

    public async resendConfirmationEmail(user: number){
        const response = await this.internalAxios.get(`/resend/${user}`)
        if(response.status === 200){
            return true;
        }
        this.handleNonErrorNotifications(response)
        return false
    }
}