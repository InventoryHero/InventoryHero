/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface AdminUserCreate {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  password: string;
  admin?: boolean;
}
export interface UserBase {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
}
export interface UserCreate {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  password: string;
}
export interface UserPublic {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  id: string;
  admin: boolean;
  registered_on: string;
  confirmed: boolean;
}
export interface UserUpdate {
  username?: string | null;
  email?: string | null;
  first_name?: string | null;
  last_name?: string | null;
}
