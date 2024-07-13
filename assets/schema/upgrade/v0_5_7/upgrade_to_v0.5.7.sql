USE gptdb;
ALTER TABLE  gptdb_serve_flow
    ADD COLUMN `define_type` varchar(32) null comment 'Flow define type(json or python)' after `version`;
