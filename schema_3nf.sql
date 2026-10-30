-- ==========================================================
-- ARCHIVO: schema_3nf.sql
-- Descripción: Definición del esquema relacional en 3ª Forma Normal (3NF)
-- Capa: Silver / Estructurada
-- Motor: PostgreSQL
-- ==========================================================

-- 1. Crear el esquema estructurado (Silver)
CREATE SCHEMA IF NOT EXISTS silver;

-- ==========================================================
-- 2. TABLAS DIMENSIONALES (Catálogos y entidades normalizadas)
-- ==========================================================

-- Tabla de Empresas
CREATE TABLE IF NOT EXISTS silver.dim_companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla de Ubicaciones (Ciudad, País, etc.)
CREATE TABLE IF NOT EXISTS silver.dim_locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(150),
    country VARCHAR(150)
);

-- Tabla de Categorías o Roles de Empleo
CREATE TABLE IF NOT EXISTS silver.dim_job_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(150) UNIQUE NOT NULL
);

-- ==========================================================
-- 3. TABLA DE HECHOS (Fact Table - Ofertas de Empleo)
-- ==========================================================

CREATE TABLE IF NOT EXISTS silver.fact_jobs (
    job_id SERIAL PRIMARY KEY,
    external_job_id VARCHAR(100), -- ID original si el CSV lo trae
    job_title VARCHAR(255) NOT NULL,
    company_id INT REFERENCES silver.dim_companies(company_id),
    location_id INT REFERENCES silver.dim_locations(location_id),
    category_id INT REFERENCES silver.dim_job_categories(category_id),
    salary_min NUMERIC(12, 2),
    salary_max NUMERIC(12, 2),
    salary_avg NUMERIC(12, 2),
    posted_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- 4. ÍNDICES PARA OPTIMIZACIÓN DE CONSULTAS
-- ==========================================================
CREATE INDEX IF NOT EXISTS idx_fact_jobs_company ON silver.fact_jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_fact_jobs_location ON silver.fact_jobs(location_id);
CREATE INDEX IF NOT EXISTS idx_fact_jobs_category ON silver.fact_jobs(category_id);