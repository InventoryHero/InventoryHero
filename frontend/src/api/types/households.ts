/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type Role = "owner" | "admin" | "member";

export interface HouseholdBase {
  name: string;
}
export interface HouseholdCreate {
  name: string;
}
export interface HouseholdInviteBase {
  id: number;
  created_at: string;
  expires_at: string;
}
export interface HouseholdInvitePublic {
  id: number;
  created_at: string;
  expires_at: string;
  code: string;
}
export interface HouseholdInviteWithMeta {
  id: number;
  created_at: string;
  expires_at: string;
  inviter_name: string;
  household_name: string;
}
export interface HouseholdMemberBase {
  id: number;
  user_id: number;
  joined: string;
  role: Role;
}
export interface HouseholdMemberPublic {
  id: number;
  user_id: number;
  joined: string;
  role: Role;
  user: UserPublic;
}
export interface UserPublic {
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  id: number;
  admin: boolean;
  registered_on: string;
  confirmed: boolean;
}
export interface HouseholdMemberUpdate {
  id: number;
  user_id: number;
  joined: string;
  role: Role;
}
export interface HouseholdMemberUpdateRole {
  role?: Role | null;
}
export interface HouseholdPublic {
  name: string;
  id: number;
  created: string;
  creator: number;
}
export interface HouseholdSelection {
  id: number;
}
export interface HouseholdUpdate {
  name?: string | null;
}
export interface HouseholdWithMemberPublic {
  name: string;
  id: number;
  created: string;
  creator: number;
  member: HouseholdMemberPublic;
}
export interface HouseholdWithMembersPublic {
  name: string;
  id: number;
  created: string;
  creator: number;
  members: HouseholdMemberPublic[];
}
