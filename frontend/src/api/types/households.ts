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
  id: string;
  created_at: string;
  expires_at: string;
}
export interface HouseholdInvitePublic {
  id: string;
  created_at: string;
  expires_at: string;
  code: string;
}
export interface HouseholdInviteWithMeta {
  id: string;
  created_at: string;
  expires_at: string;
  inviter_name: string;
  household_name: string;
}
export interface HouseholdMemberBase {
  id: string;
  user_id: string;
  joined: string;
  role: Role;
}
export interface HouseholdMemberPublic {
  id: string;
  user_id: string;
  joined: string;
  role: Role;
  user: UserPublic;
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
export interface HouseholdMemberUpdate {
  id: string;
  user_id: string;
  joined: string;
  role: Role;
}
export interface HouseholdMemberUpdateRole {
  role?: Role | null;
}
export interface HouseholdPublic {
  name: string;
  id: string;
  created: string;
}
export interface HouseholdSelection {
  id: string;
}
export interface HouseholdUpdate {
  name?: string | null;
}
export interface HouseholdWithMemberPublic {
  name: string;
  id: string;
  created: string;
  member: HouseholdMemberPublic;
}
export interface HouseholdWithMembersPublic {
  name: string;
  id: string;
  created: string;
  members: HouseholdMemberPublic[];
}
