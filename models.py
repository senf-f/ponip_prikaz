from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    nadlezno_tijelo = db.Column(db.String, nullable=False)
    poslovni_broj = db.Column(db.String, nullable=False)
    opis = db.Column(db.String, nullable=False)
    vrsta_predmeta = db.Column(db.String, nullable=False)
    opseg_imovine = db.Column(db.String, nullable=False)
    utvrdjena_vrijednost = db.Column(db.Float, nullable=False)
    napomena_uz_detalje = db.Column(db.String)
    broj_drazbe = db.Column(db.String, nullable=False)
    datum_odluke = db.Column(db.DateTime, nullable=False)
    datum_pocetka = db.Column(db.DateTime, nullable=False)
    datum_pocetka_nadmetanja = db.Column(db.DateTime, nullable=False)
    datum_zavrsetka_nadmetanja = db.Column(db.DateTime, nullable=False)
    ostali_uvjeti_prodaje = db.Column(db.String, nullable=False)
    min_cijena = db.Column(db.Float, nullable=False)
    pocetna_cijena = db.Column(db.Float, nullable=False)
    iznos_drazbenog_koraka = db.Column(db.Float, nullable=False)
    jamcevina = db.Column(db.Float, nullable=False)
    ostali_uvjeti_za_jamcevinu = db.Column(db.String)
    razgledavanje = db.Column(db.String)
    napomena_uz_uvjete_prodaje = db.Column(db.String)

    sales_info = db.relationship("SalesInfo", backref="property", lazy=True, uselist=False)

class SalesInfo(db.Model):
    __tablename__ = "sales_info"

    id = db.Column(db.Integer, db.ForeignKey("properties.id"), primary_key=True)
    iznos_najvise_ponude = db.Column(db.Float)
    status_nadmetanja = db.Column(db.String)
    broj_uplatitelja = db.Column(db.Integer)
