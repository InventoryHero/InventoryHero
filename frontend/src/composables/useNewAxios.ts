import {
    UserEndpoint,
    Endpoint,
    HouseholdEndpoint,
    LocationEndpoint,
    StorageEndpoint,
    BoxEndpoint,
    ProductEndpoint
} from "@/api/http";
import {StorageTypes} from "@/types";


export type AxiosContext = {
    axios: Endpoint
}



export default (endpoint = "") : AxiosContext => {

    switch(endpoint){
        case "user":
            return {
                axios: new UserEndpoint()
            }
        case "household": {
            return {
                axios: new HouseholdEndpoint()
            }
        }
        case "storage": {
            return {
                axios: new StorageEndpoint()
            }
        }
        case "location":{
            return {
                axios: new LocationEndpoint()
            }
        }
        case "box": {
            return {
                axios: new BoxEndpoint()
            }
        }
        case "product":{
            return {
                axios: new ProductEndpoint()
            }
        }
        default:
            console.error("INVALID ENDPOINT")

    }

    return {
        axios: new Endpoint(),
    }

}