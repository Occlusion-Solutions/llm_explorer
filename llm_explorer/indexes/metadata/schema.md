# Databricks SQL Metadata

**Table 1: system.information_schema.metastores (This table stores the metastore information)
This table stores metadata about a metastore, which is a centralized repository of metadata for a data system. The schema includes the names and data types of each column in the table.

metastore_id: string
metastore_name: string
metastore_owner: string
storage_root: string
storage_root_credential_id: string
storage_root_credential_name: string
delta_sharing_scope: string
delta_sharing_recipient_token_lifetime: long
delta_sharing_organization_name: string
privilege_model_version: string
region: string
cloud: string
created: timestamp
created_by: string
last_altered: timestamp
last_altered_by: string
global_metastore_id: string


**Table 2: default.snow_vw_en_padalloc_daily_summary_out (This table stores the daily summary of padalloc)
This table stores the information of the padalloc view, which includes the production values for all the wells for a given day.

ZONE_CODE string
ZONE_NAME string
ZONE_HID decimal(38,0)
WELL_HID decimal(15,0)
WELL_CODE string
PROD_DATE timestamp
PROD_GAS_VOLUME_MCF decimal(38,4)
PROD_OIL_VOLUME_BBL decimal(38,4)
PROD_WATER_VOLUME_BBL decimal(38,4)
ALLOCATED_FLAG string
SALE_GAS_VOLUME_MCF decimal(38,4)
SALE_OIL_VOLUME_BBL decimal(38,4)
LGL_VOLUME_MCF decimal(38,4)
OTHER_USES_GAS_MCF decimal(38,4)