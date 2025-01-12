import os
from flask import Flask, render_template
from models import db, Property, SalesInfo
from dotenv import load_dotenv


load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


app = Flask(__name__)
if ENVIRONMENT == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/../ponip_scraper_v2/test_database.db" # Default to SQLite for development

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    combined_data = db.session.query(
        Property.id,
        Property.nadlezno_tijelo,
        Property.opis,
        SalesInfo.iznos_najvise_ponude,
        SalesInfo.status_nadmetanja,
    ).join(SalesInfo, Property.id == SalesInfo.id).all()

    return render_template("index.html", data=combined_data)

if __name__ == "__main__":
    app.run()