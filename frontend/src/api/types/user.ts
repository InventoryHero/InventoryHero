/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type AuthenticationProvider = "local" | "oidc";
export type AuthenticationProvider1 = "local" | "oidc";
export type AuthenticationProvider2 = "local" | "oidc";
export type AuthenticationProvider3 = "local" | "oidc";
export type AuthenticationProvider4 = "local" | "oidc";

export interface AdminUserCreate {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  auth_provider?: AuthenticationProvider;
  password: string;
  admin?: boolean;
}
export interface UserBase {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  auth_provider?: AuthenticationProvider1;
}
export interface UserCreate {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  auth_provider?: AuthenticationProvider2;
  password: string;
  password_confirmation: string;
}
export interface UserPublic {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  auth_provider: AuthenticationProvider3;
  id: string;
  admin: boolean;
  registered_on: string;
  confirmed: boolean;
}
export interface AdminUserUpdate {
  username?: string | null;
  email?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  admin?: boolean | null;
}
export interface ChangePasswordForm {
  new_password: string;
  new_password_confirmation: string;
  current_password: string;
}
export interface ChangePasswordFormBase {
  new_password: string;
  new_password_confirmation: string;
}
export interface ResetPasswordForm {
  email: string;
}
export interface ResetPasswordResponse {
  valid: boolean;
  reason: string | null;
}
export interface TokenValidationResponse {
  valid: boolean;
  reason: string | null;
}
export interface UserCreateBase {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  auth_provider?: AuthenticationProvider4;
  password: string;
}
export interface UserUpdate {
  username?: string | null;
  email?: string | null;
  first_name?: string | null;
  last_name?: string | null;
}
