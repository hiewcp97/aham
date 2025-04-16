-- Export funds table data to CSV
.mode csv
.headers on
.output ./db/scripts/output/funds_export.csv
SELECT 
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
FROM funds;
.output stdout