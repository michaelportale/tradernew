-- Create TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create hypertable function for easier table creation
CREATE OR REPLACE FUNCTION create_market_data_hypertable(
  schema_name TEXT, 
  table_name TEXT
) 
RETURNS VOID AS $
BEGIN
  EXECUTE format('SELECT create_hypertable(%L, %L, chunk_time_interval => interval %L)',
            schema_name || '.' || table_name, 'timestamp', '1 day');
END;
$ LANGUAGE plpgsql;
