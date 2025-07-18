/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type StorageType = "room" | "box";

/**
 * Represents a single link in the breadcrumb trail.
 */
export interface BreadcrumbSchema {
  name: string;
  type: StorageType;
  id: string;
}
export interface CategoryBaseSchema {
  name: string;
}
export interface CategoryCreateSchema {
  name: string;
}
export interface CategoryReadSchema {
  name: string;
  id: string;
}
export interface ItemAttributes {
  id?: string;
  item_id: string;
  expiration_date?: string | null;
  serial_number?: string | null;
  batch_code?: string | null;
  notes?: string | null;
}
export interface ItemAttributesBaseSchema {
  expiration_date?: string | null;
  serial_number?: string | null;
  batch_code?: string | null;
  notes?: string | null;
}
export interface ItemAttributesCreateSchema {
  expiration_date?: string | null;
  serial_number?: string | null;
  batch_code?: string | null;
  notes?: string | null;
}
export interface ItemAttributesReadBaseSchema {
  expiration_date?: string | null;
  serial_number?: string | null;
  batch_code?: string | null;
  notes?: string | null;
  id: string;
  item_id: string;
}
export interface ItemAttributesReadSchema {
  expiration_date?: string | null;
  serial_number?: string | null;
  batch_code?: string | null;
  notes?: string | null;
  id: string;
  item_id: string;
  storage: ItemStorageReadSchema[];
  /**
   * Calculates the total quantity of this attribute instance by summing the
   * quantities from all its storage locations.
   */
  total_quantity: number;
}
export interface ItemStorageReadSchema {
  storage_id: string;
  quantity: number;
  id: string;
  product_attribute_id: string;
}
export interface ItemAttributesUpdateSchema {
  expiration_date?: string | null;
  serial_number?: string | null;
  batch_code?: string | null;
  notes?: string | null;
}
export interface ItemBaseSchema {
  name: string;
  description?: string | null;
}
export interface ItemCreateSchema {
  name: string;
  description?: string | null;
  categories?: string[];
  attributes: ItemAttributesBaseSchema;
  storage: ItemStorageBaseSchema;
}
export interface ItemStorageBaseSchema {
  storage_id: string;
  quantity?: number;
}
export interface ItemDetailReadSchema {
  name: string;
  description?: string | null;
  id: string;
  categories: CategoryReadSchema[];
  items: {
    [k: string]: ItemStorageReadSchema[];
  };
  storage: StorageResponseSchema[];
  attributes: {
    [k: string]: ItemAttributesReadBaseSchema;
  };
  breadcrumbs?: BreadcrumbSchema[] | null;
}
export interface StorageResponseSchema {
  name: string;
  storage_type: StorageType;
  parent_id?: string | null;
  id: string;
}
export interface ItemInstanceCreate {
  attributes?: ItemAttributesCreateSchema | null;
  storage?: ItemStorageCreateSchema | null;
}
export interface ItemStorageCreateSchema {
  storage_id: string;
  quantity?: number;
}
export interface ItemInstanceReadSchema {
  name: string;
  description?: string | null;
  id: string;
  categories: CategoryReadSchema[];
  storage: ItemStorageWithAttributesReadSchema;
}
export interface ItemStorageWithAttributesReadSchema {
  storage_id: string;
  quantity: number;
  id: string;
  product_attribute_id: string;
  attributes: ItemAttributes;
}
export interface ItemInstanceUpdateSchema {
  stock?: ItemStorageUpdateSchema | null;
  attributes?: ItemAttributesUpdateSchema | null;
}
export interface ItemStorageUpdateSchema {
  quantity?: number | null;
}
export interface ItemReadSchema {
  name: string;
  description?: string | null;
  id: string;
  categories: CategoryReadSchema[];
}
export interface ItemSummarySchema {
  name: string;
  description?: string | null;
  id: string;
  total_quantity: number;
  categories?: CategoryReadSchema[] | null;
}
export interface ItemUpdateSchema {
  name?: string | null;
  description?: string | null;
  categories_to_add: string[] | null;
  categories_to_remove: string[] | null;
}
