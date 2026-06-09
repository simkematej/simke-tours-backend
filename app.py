from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import or_
from extensions import db, migrate
from models import Korisnik, Vodic, Put, Rezervacija
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/simke_tours"
app.config["SECRET_KEY"] = "simke-tours-tajni-kljuc-2024"

db.init_app(app)
migrate.init_app(app, db)




@app.route('/')
def index():
    return "Simke Tours API"




@app.route('/api/prijava', methods=['POST'])
def prijava():
    data = request.get_json()
    email = data.get('email')
    lozinka = data.get('lozinka')

    korisnik = Korisnik.query.filter_by(email=email).first()

    if not korisnik or not korisnik.provjeri_lozinku(lozinka):
        return jsonify({"greska": "Pogrešan email ili lozinka"}), 401

    return jsonify({
        "poruka": "Prijava uspješna",
        "korisnik": korisnik.to_dict()
    })


@app.route('/api/registracija', methods=['POST'])
def registracija():
    data = request.get_json()

    postoji = Korisnik.query.filter_by(email=data.get('email')).first()
    if postoji:
        return jsonify({"greska": "Email već postoji"}), 400

    korisnik = Korisnik(
        ime=data.get('ime'),
        prezime=data.get('prezime'),
        email=data.get('email'),
        uloga="turist"
    )
    korisnik.postavi_lozinku(data.get('lozinka'))
    db.session.add(korisnik)
    db.session.commit()

    return jsonify({"poruka": "Registracija uspješna", "korisnik": korisnik.to_dict()})




@app.route('/api/vodici', methods=['GET'])
def vodici():
    svi = Vodic.query.all()
    return jsonify([v.to_dict() for v in svi])


@app.route('/api/vodici/<int:id>', methods=['GET'])
def vodic(id):
    v = Vodic.query.get_or_404(id)
    return jsonify(v.to_dict())


@app.route('/api/vodici', methods=['POST'])
def novi_vodic():
    data = request.get_json()
    v = Vodic(
        ime=data.get('ime'),
        prezime=data.get('prezime'),
        bio=data.get('bio'),
        ocjena=data.get('ocjena', 0.0),
        jezici=data.get('jezici'),
        slika_url=data.get('slika_url')
    )
    db.session.add(v)
    db.session.commit()
    return jsonify({"poruka": "Vodič dodan", "vodic": v.to_dict()})


@app.route('/api/vodici/<int:id>', methods=['PUT'])
def uredi_vodica(id):
    v = Vodic.query.get_or_404(id)
    data = request.get_json()
    v.ime = data.get('ime', v.ime)
    v.prezime = data.get('prezime', v.prezime)
    v.bio = data.get('bio', v.bio)
    v.ocjena = data.get('ocjena', v.ocjena)
    v.jezici = data.get('jezici', v.jezici)
    v.slika_url = data.get('slika_url', v.slika_url)
    db.session.commit()
    return jsonify({"poruka": "Vodič ažuriran", "vodic": v.to_dict()})


@app.route('/api/vodici/<int:id>', methods=['DELETE'])
def izbrisi_vodica(id):
    v = Vodic.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({"poruka": "Vodič izbrisan"})




@app.route('/api/putovi', methods=['GET'])
def putovi():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)
    q = request.args.get('q', '', type=str)
    kategorija = request.args.get('kategorija', '', type=str)

    upit = Put.query.outerjoin(Vodic, Put.vodic_id == Vodic.id)

    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Put.naziv.ilike(pojam),
            Put.destinacija.ilike(pojam),
            Put.zemlja.ilike(pojam),
            Put.opis.ilike(pojam)
        ))

    if kategorija:
        upit = upit.filter(Put.kategorija == kategorija)

    upit = upit.order_by(Put.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [p.to_dict() for p in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })


@app.route('/api/putovi/<int:id>', methods=['GET'])
def put_detalj(id):
    p = Put.query.get_or_404(id)
    return jsonify(p.to_dict())


@app.route('/api/putovi', methods=['POST'])
def novi_put():
    data = request.get_json()
    p = Put(
        naziv=data.get('naziv'),
        destinacija=data.get('destinacija'),
        zemlja=data.get('zemlja'),
        opis=data.get('opis'),
        cijena=data.get('cijena'),
        trajanje_dana=data.get('trajanje_dana'),
        max_osoba=data.get('max_osoba', 15),
        datum_polaska=data.get('datum_polaska'),
        slika_url=data.get('slika_url'),
        kategorija=data.get('kategorija'),
        vodic_id=data.get('vodic_id')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"poruka": "Put dodan", "put": p.to_dict()})


@app.route('/api/putovi/<int:id>', methods=['PUT'])
def uredi_put(id):
    p = Put.query.get_or_404(id)
    data = request.get_json()
    p.naziv = data.get('naziv', p.naziv)
    p.destinacija = data.get('destinacija', p.destinacija)
    p.zemlja = data.get('zemlja', p.zemlja)
    p.opis = data.get('opis', p.opis)
    p.cijena = data.get('cijena', p.cijena)
    p.trajanje_dana = data.get('trajanje_dana', p.trajanje_dana)
    p.max_osoba = data.get('max_osoba', p.max_osoba)
    p.datum_polaska = data.get('datum_polaska', p.datum_polaska)
    p.slika_url = data.get('slika_url', p.slika_url)
    p.kategorija = data.get('kategorija', p.kategorija)
    p.vodic_id = data.get('vodic_id', p.vodic_id)
    db.session.commit()
    return jsonify({"poruka": "Put ažuriran", "put": p.to_dict()})


@app.route('/api/putovi/<int:id>', methods=['DELETE'])
def izbrisi_put(id):
    p = Put.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"poruka": "Put izbrisan"})




@app.route('/api/rezervacije', methods=['GET'])
def rezervacije():
    korisnik_id = request.args.get('korisnik_id', type=int)
    if korisnik_id:
        lista = Rezervacija.query.filter_by(korisnik_id=korisnik_id).all()
    else:
        lista = Rezervacija.query.all()
    return jsonify([r.to_dict() for r in lista])


@app.route('/api/rezervacije/<int:id>', methods=['GET'])
def rezervacija(id):
    r = Rezervacija.query.get_or_404(id)
    return jsonify(r.to_dict())


@app.route('/api/rezervacije', methods=['POST'])
def nova_rezervacija():
    data = request.get_json()
    put = Put.query.get(data.get('put_id'))
    if not put:
        return jsonify({"greska": "Put nije pronađen"}), 404

    broj_osoba = data.get('broj_osoba', 1)
    ukupna_cijena = put.cijena * broj_osoba

    r = Rezervacija(
        korisnik_id=data.get('korisnik_id'),
        put_id=data.get('put_id'),
        broj_osoba=broj_osoba,
        ukupna_cijena=ukupna_cijena,
        status="na_cekanju",
        napomena=data.get('napomena', ''),
        datum_rezervacije=datetime.now().strftime("%d.%m.%Y %H:%M")
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"poruka": "Rezervacija uspješna", "rezervacija": r.to_dict()})


@app.route('/api/rezervacije/<int:id>', methods=['PUT'])
def uredi_rezervaciju(id):
    r = Rezervacija.query.get_or_404(id)
    data = request.get_json()
    r.status = data.get('status', r.status)
    r.napomena = data.get('napomena', r.napomena)
    db.session.commit()
    return jsonify({"poruka": "Rezervacija ažurirana", "rezervacija": r.to_dict()})


@app.route('/api/rezervacije/<int:id>', methods=['DELETE'])
def izbrisi_rezervaciju(id):
    r = Rezervacija.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"poruka": "Rezervacija izbrisana"})



@app.route('/api/korisnici', methods=['GET'])
def korisnici():
    svi = Korisnik.query.all()
    return jsonify([k.to_dict() for k in svi])


@app.route('/api/korisnici/<int:id>', methods=['DELETE'])
def izbrisi_korisnika(id):
    k = Korisnik.query.get_or_404(id)
    db.session.delete(k)
    db.session.commit()
    return jsonify({"poruka": "Korisnik izbrisan"})




@app.route('/api/statistike', methods=['GET'])
def statistike():
    return jsonify({
        "ukupno_putova": Put.query.count(),
        "ukupno_vodica": Vodic.query.count(),
        "ukupno_korisnika": Korisnik.query.filter_by(uloga="turist").count(),
        "ukupno_rezervacija": Rezervacija.query.count(),
        "potvrdjene_rezervacije": Rezervacija.query.filter_by(status="potvrdjeno").count(),
        "na_cekanju": Rezervacija.query.filter_by(status="na_cekanju").count(),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
