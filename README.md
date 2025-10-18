# Reqyurement
# Project Dependencies

## Python Libraries
- psycopg2
- re
- fastapi
- uvicorn
- pandas
- numpy
- selenium
- json
- logging

## Browser/Driver
- chromedriver

## PostgreSQL Tools
- pgAdmin
- pg_dump
- psql


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
    model_name TEXT,
    release_date TEXT,
    display TEXT,
    battery TEXT,
    camera TEXT,
    ram TEXT,
    storage TEXT,
    price TEXT
);
```
## Install dependencies first:
```bash
pip install psycopg2-binary beautifulsoup4 requests
```
