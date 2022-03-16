import csv
import json
import sqlite3


PARAM_FMT = ":{}"

class Tabela:
    '''
    Razred, ki predstavlja tabelo v bazi.

    Polja razreda:
    - ime: ime tabele
    - podatki: ime datoteke s podatki ali None
    '''
    ime = None
    podatki = None

    def __init__(self, conn):
        '''
        konstruktor razreda
        '''
        self.conn = conn

    def ustvari(self):
        '''
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        '''
        raise NotImplementedError

    def izbrisi(self):
        '''
        Metoda za brisanje tabele.
        '''
        self.conn.execute(f"DROP TABLE IF EXISTS {self.ime};")

    def uvozi(self, encoding = "UTF-8"):
        '''
        Metoda za uvoz podatkov.
        '''
        if self.podatki is None:
            return
        with open(self.podatki, encoding=encoding) as datoteka:
            if self.podatki.split('.')[1] == 'csv':
                podatki = csv.reader(datoteka)
                stolpci = next(podatki) #uvodna vrstica
                for vrstica in podatki:
                    vrstica = {k: None if v == '' else v for k, v in zip(stolpci, vrstica)}
                    self.dodaj_vrstico(**vrstica)
            else:
                podatki = json.load(datoteka)
                prvi_kljuc = list(podatki.keys())[0]
                prva_vrednost = podatki[prvi_kljuc]
                novi_slovar = podatki.copy()
                novi_slovar.pop(prvi_kljuc)
                prvi_kljuc = [prvi_kljuc]
                for kljuc, vrednost in novi_slovar.items():
                    vrstica = {k: None if v == '' else v for k, v in zip(prvi_kljuc, {kljuc})}
                    vrstica1 = {k: None if v == '' else v for k, v in zip(prva_vrednost, vrednost)}
                    vrstica.update(vrstica1)
                    self.dodaj_vrstico(**vrstica)
    
    def izprazni(self):
        '''
        Metoda za praznenje tabel.
        '''
        self.conn.execute(f"DELETE FROM {self.ime};")

    def dodajanje(self, stolpci=None):
        '''
        Metoda za gradnjo poizvedbe

        Argumenti:
        - stoplci: seznam stolpcev
        '''
        return f"""
            INSERT INTO {self.ime} ({",".join(stolpci)})
            VALUES ({",".join(PARAM_FMT.format(s) for s in stolpci)});
        """

    def dodaj_vrstico(self, **podatki):
        '''
        Metoda za dodajanje vrstice.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stoplcih
        '''
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items() if vrednost is not None}
        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid

class Drzava(Tabela):
    '''
    Tabela za države.
    '''
    ime = 'drzava'
    podatki = 'drzave.csv'

    def ustvari(self):
        '''
        Ustvari tabelo drzava.
        '''
        self.conn.execute("""
            CREATE TABLE drzava (
                kratica     TEXT PRIMARY KEY UNIQUE,
                ime_drzave  TEXT,
                populacija  INTEGER NOT NULL,
                bdp         INTEGER NOT NULL
            );
        """)
#                id_drzave   INTEGER PRIMARY KEY AUTOINCREMENT,
class Tekmovalka(Tabela):
    '''
    Tabela za tekmovalke.
    '''
    ime = 'tekmovalka'
    podatki = 'tekmovalke2.json'

    def ustvari(self):
        '''
        Ustvari tabelo tekmovalka.
        '''
        self.conn.execute("""
            CREATE TABLE tekmovalka (
                id_tekmovalke     INTEGER PRIMARY KEY,
                ime_priimek       TEXT    NOT NULL,
                letnica_rojstva   INTEGER NOT NULL,
                drzava            TEXT NOT NULL REFERENCES drzava (kratica),
                UNIQUE (id_tekmovalke, drzava)
            );
        """)
# drzava            INTEGER NOT NULL REFERENCES drzava (id_drzave),
class Skakalnica(Tabela):
    '''
    Tabela za skakalnice.
    '''
    ime = 'skakalnica'
    podatki = 'skakalnice2.csv'

    def ustvari(self):
        '''
        Ustvari tabelo skakalnica.
        '''
        self.conn.execute("""
            CREATE TABLE skakalnica (
                id_skakalnice   INTEGER PRIMARY KEY,
                kraj            TEXT    NOT NULL,
                velikost        INTEGER NOT NULL,
                drzava          TEXT    NOT NULL REFERENCES drzava (kratica),
                tip_skakalnice  TEXT    NOT NULL CHECK (tip_skakalnice IN ('srednja', 'velika'))
            );
        """)
#drzava          INTEGER NOT NULL REFERENCES drzava (id_drzave)
#drzava          INTEGER NOT NULL

class Tekma(Tabela):
    '''
    Tabela za tekme.
    '''
    ime = 'tekma'
    podatki = 'tekme2.json'

    def ustvari(self):
        '''
        Ustvari tabelo tekma.
        '''
        self.conn.execute("""
            CREATE TABLE tekma (
                id_tekme    INTEGER PRIMARY KEY,
                datum       DATE NOT NULL,
                tekmovanje  TEXT NOT NULL CHECK (tekmovanje IN ('svetovni pokal', 'svetovno prvenstvo', 'olimpijske igre')),
                skakalnica  INTEGER NOT NULL REFERENCES skakalnica (id_skakalnice),
                sezona      TEXT
            );
        """)
#                kraj        TEXT    NOT NULL,
#                velikost    INTEGER NOT NULL,
#sezona      TEXT CHECK (sezona LIKE '____/__')
class Rezultat(Tabela):
    '''
    Tabela za rezultate.
    '''
    ime = 'rezultat'
    podatki = 'rezultati2.csv'

    def ustvari(self):
        '''
        Ustvari tabelo rezultat.
        '''
        self.conn.execute("""
            CREATE TABLE rezultat (
                mesto       INTEGER,
                tekmovalka  INTEGER NOT NULL REFERENCES tekmovalka (id_tekmovalke),
                tekma       INTEGER NOT NULL REFERENCES tekma (id_tekme),
                PRIMARY KEY (tekmovalka, tekma)
            );
        """)

class Tockovanje(Tabela):
    '''
    Tabela za rezultate.
    '''
    ime = 'tockovanje'
    podatki = 'tockovanje.csv'

    def ustvari(self):
        '''
        Ustvari tabelo rezultat.
        '''
        self.conn.execute("""
            CREATE TABLE tockovanje (
                mesto       INTEGER UNIQUE,
                tocke       INTEGER UNIQUE
            );
        """)

def ustvari_tabele(tabele):
    '''
    Ustvari podane tabele.
    '''
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    '''
    Izbriši podane tabele.
    '''
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    '''
    Uvozi podatke v podane tabele.
    '''
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    '''
    Izprazni podane tabele.
    '''
    for t in tabele:
        t.izprazni()

def ustvari_bazo(conn):
    '''
    Izvede ustvarjanje baze.
    '''
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)

def pripravi_tabele(conn):
    '''
    Pripravi objekte za tabele.
    '''
    drzava = Drzava(conn)
    tekmovalka = Tekmovalka(conn)
    skakalnica = Skakalnica(conn)
    tekma = Tekma(conn)
    rezultat = Rezultat(conn)
    tockovanje = Tockovanje(conn)
    return [drzava, tekmovalka, skakalnica, tekma, rezultat, tockovanje]
#    return [drzava, tekmovalka, skakalnica, tekma]


def ustvari_bazo_ce_ne_obstaja(conn):
    '''
    Ustvari bazo, če ta še ne obstaja.
    '''
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)
            
# conn = dbapi.connect("zenski_smucarski_skoki.pb")
# cur = conn.cursor()
# ustvari_bazo_ce_ne_obstaja(cur)