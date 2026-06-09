"""
seed.py - Punjenje baze podataka s početnim podacima za Simke Tours
Pokretanje: python seed.py
"""

from app import app
from extensions import db
from models import Korisnik, Vodic, Put, Rezervacija


def seed():
    with app.app_context():
        print("Brišem stare podatke...")
        Rezervacija.query.delete()
        Put.query.delete()
        Vodic.query.delete()
        Korisnik.query.delete()
        db.session.commit()

        # Korisnici
        print("Dodajem korisnike...")

        admin = Korisnik(ime="Siniša", prezime="Kovačević", email="admin@simketours.ba", uloga="admin")
        admin.postavi_lozinku("admin123")

        turist1 = Korisnik(ime="Ana", prezime="Marić", email="ana@mail.com", uloga="turist")
        turist1.postavi_lozinku("lozinka123")

        turist2 = Korisnik(ime="Marko", prezime="Petrović", email="marko@mail.com", uloga="turist")
        turist2.postavi_lozinku("lozinka123")

        db.session.add_all([admin, turist1, turist2])
        db.session.commit()

        # Vodici
        print("Dodajem vodiče...")

        vodic1 = Vodic(
            ime="Mirko", prezime="Đurić",
            bio="Iskusni turistički vodič s 10 godina iskustva. Specijaliziran za mediteranska putovanja i kulturne ture po Italiji i Grčkoj.",
            ocjena=4.8,
            jezici="Hrvatski, Engleski, Talijanski",
            slika_url="https://i.pravatar.cc/150?img=11"
        )

        vodic2 = Vodic(
            ime="Jelena", prezime="Tomić",
            bio="Specijalizirana za avanturističke ture i planinarenje. Certifikovana planinska voditeljica s iskustvom u Alpima i Balkanu.",
            ocjena=4.9,
            jezici="Hrvatski, Engleski, Njemački",
            slika_url="https://i.pravatar.cc/150?img=47"
        )

        vodic3 = Vodic(
            ime="Ahmed", prezime="Hadžić",
            bio="Ekspert za Bliski Istok i Tursku. Studirao arabistiku u Sarajevu i Kairu. Vodi grupe kroz Istanbul i Kapadokiju već 8 godina.",
            ocjena=4.7,
            jezici="Hrvatski, Engleski, Turski",
            slika_url="https://i.pravatar.cc/150?img=15"
        )

        db.session.add_all([vodic1, vodic2, vodic3])
        db.session.commit()

        # Putovi
        print("Dodajem putove...")

        put1 = Put(
            naziv="Rim i Toskana",
            destinacija="Rim, Firenca",
            zemlja="Italija",
            opis="Posjetite Kolizej, Vatikan i Sikstinsku kapelu u Rimu, zatim se zaputite u bajkovitu Firencu. Proboravit ćemo noć u srcu Toskane gdje ćete kušati autentična talijanska vina i hranu.",
            cijena=1299.00,
            trajanje_dana=8,
            max_osoba=12,
            datum_polaska="15.07.2025",
            slika_url="https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=600",
            kategorija="kulturni",
            vodic_id=vodic1.id
        )

        put2 = Put(
            naziv="Santorini i Mykonos",
            destinacija="Santorini, Mykonos",
            zemlja="Grčka",
            opis="Bijele kuće s plavim kupolama i kristalno plavo more. Tri dana na Santoriniju, zatim premještaj na živahni Mykonos. Putovanje završava jednim danom u Ateni.",
            cijena=1599.00,
            trajanje_dana=9,
            max_osoba=10,
            datum_polaska="01.08.2025",
            slika_url="https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=600",
            kategorija="plažni",
            vodic_id=vodic1.id
        )

        put3 = Put(
            naziv="Švicarska i Austrija",
            destinacija="Interlaken, Beč, Salzburg",
            zemlja="Švicarska / Austrija",
            opis="Planinarit ćemo na Jungfrau, Vrhu Europe. Zatim elegantni Salzburg, rodni grad Mozarta, i na kraju bečki imperial sjaj.",
            cijena=1850.00,
            trajanje_dana=10,
            max_osoba=8,
            datum_polaska="10.07.2025",
            slika_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600",
            kategorija="avantura",
            vodic_id=vodic2.id
        )

        put4 = Put(
            naziv="Istanbul i Kapadokija",
            destinacija="Istanbul, Kapadokija",
            zemlja="Turska",
            opis="Plava džamija, Hagia Sophia, Grand Bazar i plovidba Bosporom. Nakon Istanbula, let u misterioznu Kapadokiju s legendarnim letom balonom u zoru!",
            cijena=999.00,
            trajanje_dana=7,
            max_osoba=14,
            datum_polaska="20.09.2025",
            slika_url="https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=600",
            kategorija="kulturni",
            vodic_id=vodic3.id
        )

        put5 = Put(
            naziv="Dubrovnik i otoci",
            destinacija="Dubrovnik, Hvar, Korčula",
            zemlja="Hrvatska",
            opis="Hodanje po drevnim zidinama Dubrovnika i posjet starom gradu. Brodom odlazimo na Hvar i Korčulu - rodni grad Marka Pola.",
            cijena=799.00,
            trajanje_dana=7,
            max_osoba=16,
            datum_polaska="01.07.2025",
            slika_url="https://images.unsplash.com/photo-1555990538-c4e539b5e671?w=600",
            kategorija="plažni",
            vodic_id=vodic1.id
        )

        put6 = Put(
            naziv="Maroko - zemlja boja",
            destinacija="Marrakech, Fes, Sahara",
            zemlja="Maroko",
            opis="Targ Djemaa el-Fna, labirintska medina Fesa i dvodnevni izlet u Saharu. Jahanje deve i noćenje u berberu šatoru pod zvijezdama.",
            cijena=1149.00,
            trajanje_dana=9,
            max_osoba=12,
            datum_polaska="12.10.2025",
            slika_url="https://images.unsplash.com/photo-1539020140153-e479b8c22e70?w=600",
            kategorija="kulturni",
            vodic_id=vodic3.id
        )

        db.session.add_all([put1, put2, put3, put4, put5, put6])
        db.session.commit()

        # Rezervacije
        print("Dodajem rezervacije...")

        rez1 = Rezervacija(
            korisnik_id=turist1.id, put_id=put1.id,
            broj_osoba=2, ukupna_cijena=put1.cijena * 2,
            status="potvrdjeno", napomena="Smještaj s pogledom ako je moguće.",
            datum_rezervacije="03.06.2025 10:30"
        )

        rez2 = Rezervacija(
            korisnik_id=turist2.id, put_id=put4.id,
            broj_osoba=1, ukupna_cijena=put4.cijena,
            status="na_cekanju", napomena="",
            datum_rezervacije="04.06.2025 14:15"
        )

        db.session.add_all([rez1, rez2])
        db.session.commit()

        print("\n✅ Baza uspješno popunjena!")
        print("\nPodaci za prijavu:")
        print("  Admin:   admin@simketours.ba  /  admin123")
        print("  Turist:  ana@mail.com          /  lozinka123")


if __name__ == "__main__":
    seed()
