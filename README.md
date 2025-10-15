# Samsung phones 
## Requirements
```bash
pip install psycopg2-binary
```

```bash
pip install pandas psycopg2-binary beautifulsoup4 requests
```
## Database setup
```bash
CREATE DATABASE phonesdb;
```
```bash
CREATE TABLE samsung_phones (
  id SERIAL PRIMARY KEY,
  model_name TEXT NOT NULL,
  codename TEXT,
  release_date DATE,
  display TEXT,
  battery TEXT,
  camera JSONB,
  ram_gb INTEGER,
  storage_gb INTEGER,
  price_currency TEXT,
  price_amount NUMERIC,
  specs_raw JSONB,
  source_url TEXT UNIQUE,
  scraped_at TIMESTAMP DEFAULT now()
);
```
## Install dependencies first:
```bash
pip install psycopg2-binary beautifulsoup4 requests
```
