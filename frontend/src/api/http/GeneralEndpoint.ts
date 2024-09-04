import {Endpoint} from "./Endpoint";

export class GeneralEndpoint extends Endpoint {
    constructor() {
        super(false, "")
    }

    public async checkSmtp(){
        const response = await this.internalAxios.get("/smtp-enabled")
        return response.data["smtp_configured"] ?? false
    }
}