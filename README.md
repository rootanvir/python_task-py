# Requirement
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


# Setting Up PostgreSQL Server and Importing Database

## 1. Install PostgreSQL

### Windows:
1. Download the installer from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/).
2. Run the installer and follow the setup wizard.
3. Choose a password for the default `postgres` user.
4. Select default port `5432` (or change if needed).


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
