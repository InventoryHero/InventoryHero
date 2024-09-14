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


export enum StorageTypes {
    AllStorage = -1,
    NoStorage = 0,
    Box = 1,
    Location = 2
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


export type Permissions = {
    admin?: boolean
}

export interface User {
    id: number,
    username: string,
    email: string,
    password: string|undefined,
    isAdmin?: boolean,
    firstName: string,
    lastName: string,
    registrationDate: string,
    emailConfirmed: boolean
}

export interface ApiStorage{
    id: number,
    name: string,
    householdId: string,
    creationDate: string,
    productAmount: number,
    boxAmount?: number,
    storageId: number|undefined,
    storage?: ApiStorage,
    type: StorageTypes
}

export interface ApiProduct {
    id: number,
    name: string,
    householdId: number,
    starred: boolean,
    creationDate: string,
    totalAmount: number,
}

export interface ProductStorageMapping {
    id: number,
    productId: number,
    amount: number,
    updatedAt: string,
    storage?: ApiStorage,
    storageId?: number
}