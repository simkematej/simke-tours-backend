from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Korisnik(db.Model):
    __tablename__ = "korisnici"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    lozinka_hash = db.Column(db.String(256), nullable=False)
    uloga = db.Column(db.String(10), nullable=False, default="turist")  # "turist" ili "admin"

    rezervacije = db.relationship("Rezervacija", backref="korisnik", lazy=True)

    def postavi_lozinku(self, lozinka):
        self.lozinka_hash = generate_password_hash(lozinka)

    def provjeri_lozinku(self, lozinka):
        return check_password_hash(self.lozinka_hash, lozinka)

    def to_dict(self):
        return {
            "id": self.id,
            "ime": self.ime,
            "prezime": self.prezime,
            "email": self.email,
            "uloga": self.uloga
        }


class Vodic(db.Model):
    __tablename__ = "vodici"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    ocjena = db.Column(db.Float, nullable=True, default=0.0)
    jezici = db.Column(db.String(200), nullable=True)
    slika_url = db.Column(db.String(300), nullable=True)

    putovi = db.relationship("Put", backref="vodic", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ime": self.ime,
            "prezime": self.prezime,
            "bio": self.bio,
            "ocjena": self.ocjena,
            "jezici": self.jezici,
            "slika_url": self.slika_url
        }


class Put(db.Model):
    __tablename__ = "putovi"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    destinacija = db.Column(db.String(100), nullable=False)
    zemlja = db.Column(db.String(60), nullable=False)
    opis = db.Column(db.Text, nullable=True)
    cijena = db.Column(db.Float, nullable=False)
    trajanje_dana = db.Column(db.Integer, nullable=False)
    max_osoba = db.Column(db.Integer, nullable=False, default=15)
    datum_polaska = db.Column(db.String(20), nullable=True)
    slika_url = db.Column(db.String(300), nullable=True)
    kategorija = db.Column(db.String(50), nullable=True)
    vodic_id = db.Column(db.Integer, db.ForeignKey("vodici.id"), nullable=True)

    rezervacije = db.relationship("Rezervacija", backref="put", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "naziv": self.naziv,
            "destinacija": self.destinacija,
            "zemlja": self.zemlja,
            "opis": self.opis,
            "cijena": self.cijena,
            "trajanje_dana": self.trajanje_dana,
            "max_osoba": self.max_osoba,
            "datum_polaska": self.datum_polaska,
            "slika_url": self.slika_url,
            "kategorija": self.kategorija,
            "vodic_id": self.vodic_id,
            "vodic_ime_prezime": f"{self.vodic.ime} {self.vodic.prezime}" if self.vodic else "",
            "vodic_ocjena": self.vodic.ocjena if self.vodic else None
        }


class Rezervacija(db.Model):
    __tablename__ = "rezervacije"

    id = db.Column(db.Integer, primary_key=True)
    korisnik_id = db.Column(db.Integer, db.ForeignKey("korisnici.id"), nullable=False)
    put_id = db.Column(db.Integer, db.ForeignKey("putovi.id"), nullable=False)
    broj_osoba = db.Column(db.Integer, nullable=False, default=1)
    ukupna_cijena = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="na_cekanju")  # na_cekanju, potvrdjeno, otkazano
    napomena = db.Column(db.Text, nullable=True)
    datum_rezervacije = db.Column(db.String(30), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "korisnik_id": self.korisnik_id,
            "put_id": self.put_id,
            "broj_osoba": self.broj_osoba,
            "ukupna_cijena": self.ukupna_cijena,
            "status": self.status,
            "napomena": self.napomena,
            "datum_rezervacije": self.datum_rezervacije,
            "korisnik_ime": f"{self.korisnik.ime} {self.korisnik.prezime}" if self.korisnik else "",
            "put_naziv": self.put.naziv if self.put else "",
            "put_destinacija": self.put.destinacija if self.put else ""
        }
