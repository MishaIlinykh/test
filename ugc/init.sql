CREATE DATABASE IF NOT EXISTS UGC_database;

CREATE TABLE IF NOT EXISTS UGC_database.UGC_table (
    user_id UUID,
    event_type LowCardinality(String),
    timestamp DateTime,
    content Map(String, String)
) ENGINE = MergeTree
ORDER BY tuple();
