-- Enable timing to track performance
\timing on

-- Create temporary table for staging
CREATE TEMPORARY TABLE temp_funds (LIKE funds INCLUDING ALL);

-- Copy data from CSV file
\copy temp_funds FROM 'db/scripts/output/funds_export.csv' WITH (FORMAT csv, HEADER true)

-- Create function for batch processing
CREATE OR REPLACE FUNCTION migrate_funds_in_batches(batch_size INT)
RETURNS void AS $$
DECLARE
    last_id INT := 0;
    batch_count INT := 0;
    total_migrated INT := 0;
BEGIN
    LOOP
        -- Insert batch of records
        INSERT INTO funds (
            id,
            fund_id,
            fund_name,
            fund_manager_name,
            fund_description,
            fund_nav,
            fund_creation_date,
            fund_performance,
            created_at,
            updated_at
        )
        SELECT 
            id,
            fund_id::uuid,
            fund_name,
            fund_manager_name,
            fund_description,
            fund_nav::numeric(20,2),
            fund_creation_date::date,
            fund_performance::numeric(10,2),
            created_at::timestamp with time zone,
            updated_at::timestamp with time zone
        FROM temp_funds
        WHERE id > last_id
        ORDER BY id
        LIMIT batch_size;

        GET DIAGNOSTICS batch_count = ROW_COUNT;
        
        EXIT WHEN batch_count = 0;
        
        total_migrated := total_migrated + batch_count;
        
        -- Update last processed ID
        SELECT id INTO last_id
        FROM funds
        ORDER BY id DESC
        LIMIT 1;
        
        RAISE NOTICE 'Migrated batch: % records. Total: %', batch_count, total_migrated;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Execute migration in batches of 1000 records
SELECT migrate_funds_in_batches(1000);

-- Cleanup
DROP FUNCTION migrate_funds_in_batches(INT);
DROP TABLE temp_funds;