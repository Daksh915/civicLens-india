USE civic_db;

CREATE TABLE IF NOT EXISTS dim_state (
    state_id    INT AUTO_INCREMENT PRIMARY KEY,
    state_name  VARCHAR(100) NOT NULL UNIQUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_years (
    year_id     INT AUTO_INCREMENT PRIMARY KEY,
    year        INT NOT NULL UNIQUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_crime (
    crime_id                   INT AUTO_INCREMENT PRIMARY KEY,
    state_id                   INT,
    year_id                    INT,
    total_crimes               INT,
    population_lakhs_2022      DECIMAL(10,2),
    crime_rate_per_lakh_2022   DECIMAL(10,2),
    chargesheeting_rate_2022   DECIMAL(10,2),
    literacy_rate              DECIMAL(5,2),
    literacy_year              INT,
    source_name                VARCHAR(100),
    ingested_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id)     REFERENCES dim_state(state_id),
    FOREIGN KEY (year_id)      REFERENCES dim_year(year_id),
    UNIQUE KEY uq_state_year   (state_id, year_id)
);


CREATE TABLE IF NOT EXISTS etl_log (
    log_id           INT AUTO_INCREMENT PRIMARY KEY,
    pipeline_name    VARCHAR(100),
    run_start        TIMESTAMP NULL,
    run_end          TIMESTAMP NULL,
    status           VARCHAR(20),
    rows_loaded      INT,
    error_message    TEXT
);

CREATE TABLE IF NOT EXISTS data_quality_log (
    dq_id           INT AUTO_INCREMENT PRIMARY KEY,
    table_name      VARCHAR(100),
    check_name      VARCHAR(100),
    check_result    VARCHAR(20),
    rows_affected   INT,
    checked_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);