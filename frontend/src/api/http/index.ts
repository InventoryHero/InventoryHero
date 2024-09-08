import {UserEndpoint} from "./UserEndpoint";
import {Endpoint} from "./Endpoint";
import {HouseholdEndpoint} from "./HouseholdEndpoint";
import {LocationEndpoint, StorageEndpoint, BoxEndpoint} from "./StorageEndpoint.ts";
import {ProductEndpoint} from "./ProductEndpoint.ts";
import {AdministrationEndpoint} from "@/api/http/AdministrationEndpoint.ts";
import {GeneralEndpoint} from "@/api/http/GeneralEndpoint.ts";
import {io} from "socket.io-client";

export {
    UserEndpoint,
    Endpoint,
    HouseholdEndpoint,
    LocationEndpoint,
    StorageEndpoint,
    BoxEndpoint,
    ProductEndpoint,
    AdministrationEndpoint,
    GeneralEndpoint
}
