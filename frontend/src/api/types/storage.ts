/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type StorageType = "room" | "box";

export interface BoxResponseSchema {
  name: string;
  storage_type: "box";
  parent_id?: string | null;
  id: string;
  num_items?: number | null;
  parent?: StorageResponseSchema | null;
}
export interface StorageResponseSchema {
  name: string;
  storage_type: StorageType;
  parent_id?: string | null;
  id: string;
}
export interface RoomResponseSchema {
  name: string;
  storage_type: "room";
  parent_id?: string | null;
  id: string;
  num_boxes?: number | null;
  num_items?: number | null;
}
export interface StorageBaseSchema {
  name: string;
  storage_type: StorageType;
  parent_id?: string | null;
}
export interface StorageCreateSchema {
  name: string;
  storage_type: StorageType;
  parent_id?: string | null;
}
