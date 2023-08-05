-- COMMAND ----------

create catalog if not exists habu_org_${org_id_sanitized}_share_db USING SHARE ${orchestrator_name}.habu_org_${org_id_sanitized}_share;

-- COMMAND ----------

create catalog if not exists HABU_CLEAN_ROOM_COMMON;
create schema if not exists HABU_CLEAN_ROOM_COMMON.clean_room;
create schema if not exists HABU_CLEAN_ROOM_COMMON.DATA_CONNECTIONS;
create table if not exists HABU_CLEAN_ROOM_COMMON.clean_room.app_metadata(id string, metadata_key string, metadata_value string, created_at timestamp, updated_at timestamp);

CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS (ID STRING NOT NULL, REQUEST_TYPE STRING NOT NULL, REQUEST_DATA MAP<STRING, STRING>, CREATED_AT TIMESTAMP,  UPDATED_AT TIMESTAMP, REQUEST_STATUS STRING);

CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.DATA_CONNECTIONS.DATA_CONNECTIONS ( 
            ID STRING NOT NULL, 
            ORGANIZATION_ID STRING NOT NULL, 
            DATABASE_NAME STRING NOT NULL, 
            DB_SCHEMA_NAME STRING NOT NULL, 
            DB_TABLE_NAME STRING NOT NULL, 
            DATASET_TYPE STRING);
            
CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS ( 
            ID STRING NOT NULL, 
            ORGANIZATION_ID STRING NOT NULL, 
            DATA_CONNECTION_ID STRING NOT NULL, 
            COLUMN_NAME STRING NOT NULL, 
            COLUMN_POSITION INT NOT NULL, 
            DATA_TYPE STRING, 
            NUMERIC_PRECISION INT, 
            NUMERIC_SCALE INT);
            
CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_ERRORS (
            CODE INT,
            STATE STRING,
            MESSAGE STRING,
            STACK_TRACE STRING,
            CREATED_AT TIMESTAMP,
            REQUEST_ID STRING,
            PROC_NAME STRING)

-- COMMAND ----------

CREATE SHARE if not exists habu_clean_room_common_share_${org_id_sanitized};

-- COMMAND ----------

CREATE RECIPIENT IF NOT EXISTS habu_orchestrator USING ID '${habu_sharing_id}';

-- COMMAND ----------

ALTER SHARE habu_clean_room_common_share_${org_id_sanitized} ADD TABLE HABU_CLEAN_ROOM_COMMON.DATA_CONNECTIONS.DATA_CONNECTIONS;

ALTER SHARE habu_clean_room_common_share_${org_id_sanitized} ADD TABLE HABU_CLEAN_ROOM_COMMON.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS;

ALTER SHARE habu_clean_room_common_share_${org_id_sanitized} ADD TABLE HABU_CLEAN_ROOM_COMMON.clean_room.CLEAN_ROOM_ERRORS;

ALTER TABLE HABU_CLEAN_ROOM_COMMON.clean_room.app_metadata  SET tblproperties(delta.enableChangeDataFeed = true);
ALTER SHARE habu_clean_room_common_share_${org_id_sanitized} ADD TABLE HABU_CLEAN_ROOM_COMMON.clean_room.app_metadata WITH CHANGE DATA FEED;

ALTER TABLE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS  SET tblproperties(delta.enableChangeDataFeed = true);
ALTER SHARE habu_clean_room_common_share_${org_id_sanitized} ADD TABLE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS WITH CHANGE DATA FEED;

-- COMMAND ----------

GRANT SELECT ON SHARE habu_clean_room_common_share_${org_id_sanitized} TO RECIPIENT habu_orchestrator;

-- COMMAND ----------

insert into habu_clean_room_common.clean_room.app_metadata select uuid(), 'latest_version', '1', current_timestamp, null;