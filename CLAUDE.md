# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask web application that displays Croatian property auction data ("dražba") in a sortable/filterable table. It reads from a database populated by a separate scraper project (`ponip_scraper_v2`).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Production (gunicorn)
gunicorn wsgi:app
```

## Architecture

- **app.py** — Flask app with a single route (`/`) that joins `Property` and `SalesInfo` tables and renders the template.
- **models.py** — SQLAlchemy models for `properties` and `sales_info` tables. `SalesInfo` is linked to `Property` via a one-to-one relationship.
- **wsgi.py** — Gunicorn entry point.
- **templates/index.html** — Jinja2 template with client-side JS for table sorting and status filtering.
- **static/style.css** — Dark-theme CSS.

## Environment

- Development uses a SQLite database from the sibling `ponip_scraper_v2` project (`../ponip_scraper_v2/test_database.db`).
- Production expects `ENVIRONMENT=production` and `SQLALCHEMY_DATABASE_URI` set in `.env` (PostgreSQL via psycopg2).

## Data Model Notes

- `SalesInfo.id` is stored as a string in the DB but is cast to Integer when joining with `Property.id`.
- The query in `app.py` uses an outer join — properties may not have corresponding sales info.
