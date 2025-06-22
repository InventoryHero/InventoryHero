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
