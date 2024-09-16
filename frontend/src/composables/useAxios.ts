import {
    UserEndpoint,
    Endpoint,
    HouseholdEndpoint,
    LocationEndpoint,
    StorageEndpoint,
    BoxEndpoint,
    ProductEndpoint,
    AdministrationEndpoint, GeneralEndpoint
} from "@/api/http";

import {useAuthStore} from "@/store";


type SpecificEndpoint = UserEndpoint | HouseholdEndpoint | LocationEndpoint | StorageEndpoint | BoxEndpoint | ProductEndpoint | AdministrationEndpoint | GeneralEndpoint;

export type AxiosContext<T extends Endpoint> = {
    axios: T
};

export default function useAxios<T extends SpecificEndpoint>(endpoint: string): AxiosContext<T> {
    //const authStore = useAuthStore()
    let axios = null;
    switch(endpoint){
        case "user":
            axios = new UserEndpoint() as T
            break
        case "household":
            axios = new HouseholdEndpoint() as T
            break;
        case "storage":
            axios = new StorageEndpoint() as T
            break
        case "location":
            axios = new LocationEndpoint() as T
            break
        case "box":
            axios = new BoxEndpoint() as T
            break
        case "product":
            axios = new ProductEndpoint() as T
            break
        case "administration":
            //if(authStore.isAdmin){
            axios = new AdministrationEndpoint() as T
            //}
            break
        case "general":
            axios = new GeneralEndpoint() as T
            break

        default:
            console.error("INVALID ENDPOINT")

    }

    if(axios === null){
        axios = new Endpoint() as T
    }

    return {
        axios: axios ,
    }

}