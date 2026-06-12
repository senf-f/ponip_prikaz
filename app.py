import os
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template
from sqlalchemy import Integer, cast

from models import db, Property, SalesInfo

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = Flask(__name__)

if ENVIRONMENT == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
else:
    db_path = Path(__file__).resolve().parent.parent / "ponip_scraper_v2" / "test_database.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    combined_data = db.session.query(
        Property.id,
        Property.opis,
        Property.utvrdjena_vrijednost,
        Property.pocetna_cijena,
        Property.datum_zavrsetka_nadmetanja,
        SalesInfo.broj_uplatitelja,
        SalesInfo.iznos_najvise_ponude,
        SalesInfo.status_nadmetanja,
        SalesInfo.url,
    ).outerjoin(SalesInfo, Property.id == cast(SalesInfo.id, Integer)).all()

    today = datetime.now().date()
    one_week_from_now = today + timedelta(weeks=1)

    app.logger.info(f"Fetched {len(combined_data)} rows from the database.")
    return render_template("index.html", data=combined_data, today=today, one_week_from_now=one_week_from_now)


if __name__ == "__main__":
    app.run(debug=True)
