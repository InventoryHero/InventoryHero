/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface AppConfig {
  smtp_enabled: boolean;
  registration_allowed: boolean;
  app_version: string;
  base_url: string;
  base_url_default: boolean;
  database_type: string | null;
  database_connection: string | null;
  deployment: string;
}
export interface ConfigPublic {
  smtp_enabled: boolean;
  registration_allowed: boolean;
}
