-- Databricks notebook source
-- for manual testing from a particular version uncomment below lines and set version to start with
-- delete from habu_clean_room_common.clean_room.app_metadata where metadata_key = 'latest_version';
-- insert into habu_clean_room_common.clean_room.app_metadata select uuid(), 'latest_version', '11', current_timestamp, null;
-- select * from habu_clean_room_common.clean_room.app_metadata

-- COMMAND ----------

-- MAGIC %python
-- MAGIC org_id_sanitized = getArgument("org_id", "2a034d9c-db2b-4996-b219-138f31d172ee").replace("-", "")
-- MAGIC share_db = f'habu_org_{org_id_sanitized}_share_db'

-- COMMAND ----------

-- MAGIC %python
-- MAGIC last_processed_version = sqlContext.sql("SELECT metadata_value from habu_clean_room_common.clean_room.app_metadata where metadata_key = 'latest_version'").collect().pop()['metadata_value']
-- MAGIC 
-- MAGIC # this is because of a bug in databricks where selecting from table_changes fails if run initially
-- MAGIC sqlContext.sql(f"select * from {share_db}.clean_room.clean_room_requests")
-- MAGIC 
-- MAGIC records_to_process = sqlContext.sql(f"SELECT id, request_type, request_data, created_at, updated_at, request_status, _change_type, _commit_version FROM table_changes('{share_db}.clean_room.clean_room_requests', {last_processed_version}) where _change_type='insert'  order by _commit_timestamp").collect()
-- MAGIC 
-- MAGIC # delta tables error out if the query uses a version newer than latest. We pick up the last processed record and process only from second row onwards
-- MAGIC records_to_process = records_to_process[1:]
-- MAGIC 
-- MAGIC for record in records_to_process:
-- MAGIC     request_data = record['request_data']
-- MAGIC 
-- MAGIC     if record['request_type'] == 'NEW_CLEAN_ROOM' or record['request_type'] == 'NEW_CLEAN_ROOM_PARTNER':
-- MAGIC         sanitizedCRID = request_data['clean_room_id'].replace("-", "").upper()
-- MAGIC         dbutils.notebook.run("create-cleanroom.sql", 60, {"request_id": record['id'], "clean_room_id": sanitizedCRID, "habu_sharing_id": request_data['habu_sharing_id']})
-- MAGIC 
-- MAGIC     elif record['request_type'] == 'NEW_DATA_CONNECTION':
-- MAGIC         dbutils.notebook.run("new-data-connection.sql", 60, {"request_id": record['id'], "db_nm": request_data['database_name'], "schema_nm": request_data['schema_name'], "table_nm": request_data['table_name'], "data_connection_id": request_data['data_connection_id'], "dataset_type": request_data['dataset_type'], "org_id": request_data['organization_id']})
-- MAGIC 
-- MAGIC     elif record['request_type'] == 'NEW_DATASET':
-- MAGIC         sanitizedCRID = request_data['clean_room_id'].replace("-", "").upper()
-- MAGIC         dbutils.notebook.run("create-dataset.sql", 60, {"request_id": record['id'], "clean_room_id": sanitizedCRID, "catalog_name": request_data['catalog_name'], "schema_name": request_data['schema_name'], "table_name": request_data['table_name']})
-- MAGIC     
-- MAGIC     # update the last processed version
-- MAGIC     highest_processed_version = record['_commit_version']
-- MAGIC     sqlContext.sql(f"update habu_clean_room_common.clean_room.app_metadata set metadata_value = '{highest_processed_version}' where metadata_key = 'latest_version'")
-- MAGIC     
-- MAGIC     # insert into table shared back with habu so habu can monitor status of request
-- MAGIC     sqlContext.sql(f"insert into habu_clean_room_common.clean_room.clean_room_requests select \'{record['id']}\', \'{record['request_type']}\', (select request_data from {share_db}.clean_room.clean_room_requests where id = \'{record['id']}\'), \'{record['created_at']}\', current_timestamp, 'COMPLETE'")

-- COMMAND ----------

