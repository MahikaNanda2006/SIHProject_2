CREATE TABLE batches (
    batch_id VARCHAR PRIMARY KEY,
    stakeholder VARCHAR,
    parent_batch_id VARCHAR,        -- new column for processors / hierarchy
    weight VARCHAR,
    latitude FLOAT,
    longitude FLOAT,
    image BYTEA,
    pdf BYTEA,
    extra_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hash_key VARCHAR
);
