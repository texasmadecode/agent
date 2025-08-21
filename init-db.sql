-- Initial database setup script
-- This script runs when the PostgreSQL container starts for the first time

-- Create the marketing_agent database if it doesn't exist
SELECT 'CREATE DATABASE marketing_agent'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'marketing_agent')\gexec

-- Create extensions we might need
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance (will be created by migrations but good to have as backup)
-- These will only apply if tables exist
DO $$
BEGIN
    -- Add any initial database setup here
    RAISE NOTICE 'Database initialization script completed';
END
$$;
