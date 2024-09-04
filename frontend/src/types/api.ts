export type Household = {
    id: number,
    creator: number,
    name: string,
    members: Array<HouseholdMember>
}

export type HouseholdMember = {
    id: number,
    member: number
}

export type ProductOnly = {
    creation_date: string,
    household_id: number,
    id: number,
    name: string,
    starred: boolean,
    total_amount: number,
}

export type Product = ProductOnly & {
    storage_locations: Array<ProductLocations>
}

export type ProductLocations = {
    id: number
    amount: number,
    name: string,
    product_id: number,
    updated_at: string,
    storage: Storage|undefined,
    storage_type: number
}

export enum StorageTypes {
    AllStorage = -1,
    NoStorage = 0,
    Box = 1,
    Location = 2
}

export interface Storage {
    id: number,
    name: string,
    household_id: string,
    creation_date: string,
    type: StorageTypes
}

export interface Location extends Storage {

}

export interface Box extends Storage {
    location_id: number | null
    location: Location | null,
    products?: number,
    product_mappings?: Array<Product>
}

export function isInstanceOfStorage(object: any): object is Storage{
    return 'type' in object;
}


export interface ILoginRequest{
    username: string,
    password: string
}

export interface ILoginResponse{
    access_token: string,
    refresh_token: string
}
export interface IRegisterRequest{
    username: string,
    password: string,
    email: string
}

export interface IReqisterResponse{
    user?: string,
    status: string
}

export interface IUser {
    username: string,
    email: string,
    household?:  number,
    authorized?: boolean
}

export type LocationContent = {
    type: "box"|"product"
    id: string,
    content: Box | ProductOnly & ProductLocations

}


export type Permissions = {
    admin?: boolean
}

export interface User {
    id: number,
    username: string,
    email: string,
    password: string|undefined,
    is_admin: boolean,
    first_name: string,
    last_name: string,
    registration_date: string,
    email_confirmed: boolean
}