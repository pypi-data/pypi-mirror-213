-- Databricks notebook source
drop SHARE if exists HABU_CR_${clean_room_id}_SHARE;



-- COMMAND ----------

create share if not exists HABU_CR_${clean_room_id}_SHARE;


-- COMMAND ----------

GRANT SELECT ON SHARE HABU_CR_${clean_room_id}_SHARE TO RECIPIENT habu_orchestrator;