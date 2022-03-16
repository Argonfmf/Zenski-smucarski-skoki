import baza
import sqlite3


conn = sqlite3.connect('zenski_smucarski_skoki.pb')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

drzava, tekmovalka, skakalnica, tekma, rezultat, tockovanje = baza.pripravi_tabele(conn)

class Tekmovalka:
    '''
    Razred za tekmovalke.
    '''

    def __init__(self, ime_priimek, letnica_rojstva, drzava, id_tekmovalke=None):
        self.id_tekmovalke = id_tekmovalke
        self.ime_priimek = ime_priimek
        self.letnica_rojstva = letnica_rojstva
        self.drzava = drzava

    def __str__(self):
        return self.ime_priimek
    
    def po_zmagah():
        '''
        Razporedi tekmovalke po številu zmag v pokalu.
        '''
        sql = """ 
            SELECT ime_priimek, drzava, COUNT(mesto)
            FROM tekmovalka JOIN rezultat ON id_tekmovalke = tekmovalka
            WHERE mesto = 1
            GROUP BY ime_priimek
            ORDER BY COUNT(mesto) DESC
        """
        for ime, drzava, stevilo in conn.execute(sql):
            yield [ime, drzava, stevilo]

    def po_stopnickah():
        '''
        Razporedi tekmovalke po številu stopničk v pokalu.
        '''
        sql = """ 
            SELECT ime_priimek, drzava, COUNT(mesto)
            FROM tekmovalka JOIN rezultat ON id_tekmovalke = tekmovalka
            WHERE mesto BETWEEN 1 AND 3
            GROUP BY ime_priimek
            ORDER BY COUNT(mesto) DESC
        """
        for ime, drzava, stevilo in conn.execute(sql):
            yield [ime, drzava, stevilo]

    def po_top_deset():
        '''
        Razporedi tekmovalke po številu uvrstitev med najboljših 10 v pokalu.
        '''
        sql = """ 
            SELECT ime_priimek, drzava, COUNT(mesto)
            FROM tekmovalka JOIN rezultat ON id_tekmovalke = tekmovalka
            WHERE mesto BETWEEN 1 AND 10
            GROUP BY ime_priimek
            ORDER BY COUNT(mesto) DESC
        """
        for ime, drzava, stevilo in conn.execute(sql):
            yield [ime, drzava, stevilo]

    def po_tockah():
        '''
        Razporedi tekmovalke po številu osvojenih točk v pokalu.
        '''
        sql = """ 
            SELECT ime_priimek, drzava, SUM(tocke) 
            FROM tekmovalka JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON tekma = id_tekme
            JOIN tockovanje ON rezultat.mesto = tockovanje.mesto
            WHERE tekmovanje = 'svetovni pokal'
            GROUP BY ime_priimek
            ORDER BY SUM(tocke) DESC
        """
        for ime, drzava, tocke in conn.execute(sql):
            yield [ime, drzava, tocke]

    def po_medaljah_ol():
        '''
        Razporedi tekmovalke po številu osvojenih medalj na olimpjskih igrah.
        '''
        sql = """ 
            SELECT ime_priimek, drzava,
            COUNT(CASE WHEN mesto = 1 THEN 1 END) AS zlate,
            COUNT(CASE WHEN mesto = 2 THEN 1 END) AS srebrne,
            COUNT(CASE WHEN mesto = 3 THEN 1 END) AS bronaste
            FROM tekmovalka JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON id_tekme = tekma
            WHERE tekmovanje = 'olimpijske igre'
            GROUP BY ime_priimek
            ORDER BY zlate DESC, srebrne DESC, bronaste DESC
            LIMIT 8;
        """
        for ime, drzava, zlate, srebrne, bronaste in conn.execute(sql):
            yield [ime, drzava, zlate, srebrne, bronaste]

    def po_medaljah_sp():
        '''
        Razporedi tekmovalke po številu osvojenih medalj na svetovnih prvenstvih.
        '''
        sql = """ 
            SELECT ime_priimek, drzava,
            COUNT(CASE WHEN mesto = 1 THEN 1 END) AS zlate,
            COUNT(CASE WHEN mesto = 2 THEN 1 END) AS srebrne,
            COUNT(CASE WHEN mesto = 3 THEN 1 END) AS bronaste
            FROM tekmovalka JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON id_tekme = tekma
            WHERE tekmovanje = 'svetovno prvenstvo'
            GROUP BY ime_priimek
            ORDER BY zlate DESC, srebrne DESC, bronaste DESC
            LIMIT 15;
        """
        for ime, drzava, zlate, srebrne, bronaste in conn.execute(sql):
            yield [ime, drzava, zlate, srebrne, bronaste]

    def stevilo_zmag(self):
        '''
        Vrne število zmag tekmovalke.
        '''
        sql = """
            SELECT COUNT(mesto)
            FROM rezultat JOIN tekmovalka ON tekmovalka=id_tekmovalke
            JOIN tekma ON tekma = id_tekme
            WHERE mesto = 1 AND ime_priimek = ? AND tekmovanje = 'svetovni pokal'
        """
        for stevilo in conn.execute(sql, [self.ime_priimek]):
            return stevilo
        
    def stevilo_stopnick(self):
        '''
        Vrne število stopnick tekmovalke.
        '''
        sql = """
            SELECT COUNT(mesto)
            FROM rezultat JOIN tekmovalka ON tekmovalka=id_tekmovalke
            JOIN tekma ON tekma = id_tekme
            WHERE mesto BETWEEN 1 AND 3 AND ime_priimek = ? AND tekmovanje = 'svetovni pokal'
        """
        for stevilo in conn.execute(sql, [self.ime_priimek]):
            return stevilo
        
    def stevilo_medalj_olimpijske(self):
        '''
        Vrne število olimpijskih medalj tekmovalke.
        '''
        sql = """
            SELECT COUNT(mesto)
            FROM rezultat JOIN tekmovalka ON tekmovalka=id_tekmovalke
            JOIN tekma ON tekma = id_tekme
            WHERE mesto BETWEEN 1 AND 3 AND ime_priimek = ? AND tekmovanje = 'olimpijske igre'
        """
        for stevilo in conn.execute(sql, [self.ime_priimek]):
            return stevilo
    
    def stevilo_medalj_svetovno_prvenstvo(self):
        '''
        Vrne število medalj s svetovnega prvenstva za dano tekmovalko.
        '''
        sql = """
            SELECT COUNT(mesto)
            FROM rezultat JOIN tekmovalka ON tekmovalka=id_tekmovalke
            JOIN tekma ON tekma = id_tekme
            WHERE mesto BETWEEN 1 AND 3 AND ime_priimek = ? AND tekmovanje = 'svetovno prvenstvo'
        """
        for stevilo in conn.execute(sql, [self.ime_priimek]):
            return stevilo
        
    @staticmethod
    def najboljse_v_sezoni(sezona):
        """
        Vrne najboljših 10 tekmovalk v dani sezoni.
        """
        sql = """ 
            SELECT ime_priimek, SUM(tocke)
            FROM rezultat JOIN tekmovalka ON tekmovalka = id_tekmovalke
            JOIN tockovanje ON tockovanje.mesto = rezultat.mesto
            JOIN tekma ON tekma = id_tekme
            WHERE sezona = ? AND tekmovanje = 'svetovni pokal'
            GROUP BY ime_priimek
            ORDER BY SUM(tocke) DESC
            LIMIT 10
        """
        for ime_priimek, tocke in conn.execute(sql, [sezona]):
            yield [ime_priimek, tocke]
    
    @staticmethod
    def najboljse_drzave_v_sezoni(sezona):
        """
        Vrne najboljših 10 držav v dani sezoni.
        """
        sql = """ 
            SELECT ime_drzave, SUM(tocke)
            FROM rezultat JOIN tekmovalka ON tekmovalka = id_tekmovalke
            JOIN tockovanje ON rezultat.mesto = tockovanje.mesto
            JOIN tekma ON tekma = id_tekme
            JOIN drzava ON drzava = kratica
            WHERE sezona = ? AND tekmovanje = 'svetovni pokal'
            GROUP BY ime_drzave
            ORDER BY SUM(tocke) DESC
            LIMIT 10
        """
        for ime_drzave, tocke in conn.execute(sql, [sezona]):
            yield [ime_drzave, tocke]

    @staticmethod
    def poisci(niz):
        """
        Vrne vse tekmovalke, ki v imenu in priimku vsebujejo dani niz.
        """
        sql = "SELECT ime_priimek, letnica_rojstva, drzava FROM tekmovalka WHERE ime_priimek LIKE ?"
        for ime_priimek, letnica_rojstva, drzava in conn.execute(sql, [f'%{niz}%']):
            yield Tekmovalka(ime_priimek=ime_priimek, letnica_rojstva=letnica_rojstva, drzava=drzava)
    
    @staticmethod
    def poisci1(niz):
        """
        Vrne vse tekmovalke, ki v imenu in priimku vsebujejo dani niz.
        """
        sql = "SELECT ime_priimek FROM tekmovalka WHERE ime_priimek LIKE ? "
        for ime_priimek in conn.execute(sql, [f'%{niz}%']):
            yield [ime_priimek]
            
    @staticmethod
    def stevilo_stopnick1(niz):
        '''
        Vrne število stopnick tekmovalke.
        '''
        sql = """
            SELECT COUNT(mesto)
            FROM rezultat JOIN tekmovalka ON tekmovalka=id_tekmovalke
            JOIN tekma ON tekma = id_tekme
            WHERE mesto BETWEEN 1 AND 3 AND ime_priimek LIKE ? AND tekmovanje = 'svetovni pokal'
        """
        for stevilo in conn.execute(sql, [f'%{niz}%']):
            return stevilo
    
    @staticmethod
    def poisci2(niz):
        """
        Vrne vse tekmovalke, ki v imenu in priimku vsebujejo dani niz.
        """
        sql = """
                SELECT ime_priimek, letnica_rojstva, drzava, COUNT(CASE WHEN mesto = 1 THEN 1 END) FROM tekmovalka
                JOIN rezultat ON id_tekmovalke = tekmovalka JOIN tekma ON tekma = id_tekme
                WHERE ime_priimek LIKE ? AND tekmovanje = 'svetovni pokal'
            """
        
        for ime_priimek, letnica_rojstva, drzava, st_zmag in conn.execute(sql, [f'%{niz}%']):
            yield [ime_priimek, letnica_rojstva, drzava, st_zmag]
    
    def dodaj_v_bazo(self):
        assert self.id_tekmovalke is None
        with conn:
            self.id_tekmovalke = tekmovalka.dodaj_vrstico(ime_priimek=self.ime_priimek, letnica_rojstva=self.letnica_rojstva, drzava=self.drzava)
            return self.id_tekmovalke


class Skakalnica:
    '''
    Razred za skakalnice.
    '''

    def __init__(self, kraj, velikost, drzava, tip_skakalnice, id_skakalnice=None):
        self.id_skakalnice = id_skakalnice
        self.kraj = kraj
        self.velikost = velikost
        self.drzava = drzava
        self.tip_skakalnice = tip_skakalnice

    def __str__(self):
        return f'{self.kraj} {self.tip_skakalnice}'

    def podatki(self):
        '''
        Vrne podatke skakalnice.
        '''
        sql = """
            SELECT kraj, velikost, drzava, tip_skakalnice 
            FROM skakalnica
            WHERE id_skakalnice = ?
        """
        for kraj, velikost, drzava, tip_skakalnice in conn.execute(sql, [self.id_skakalnice]):
            return kraj, velikost, drzava, tip_skakalnice
    
    def stevilo_tekem(self):
        '''
        Vrne število tekem skakalnice.
        '''
        sql = """
            SELECT COUNT(skakalnica)
            FROM tekma JOIN skakalnica ON skakalnica=id_skakalnice
            WHERE kraj = ? AND tip_skakalnice = ?
        """
        for stevilo in conn.execute(sql, [self.kraj, self.tip_skakalnice]):
            return stevilo

    def stevilo_tekem_na_srednjih_skakalnicah():
        '''
        Vrne število tekem na srednjih skakalnicah.
        '''
        sql = """
            SELECT COUNT(id_skakalnice)
            FROM tekma JOIN skakalnica ON skakalnica=id_skakalnice
            WHERE tip_skakalnice = 'srednja' AND tekmovanje = 'svetovni pokal'
        """
        for stevilo in conn.execute(sql):
            return stevilo
    
    def stevilo_tekem_na_velikih_skakalnicah():
        '''
        Vrne število tekem na velikih skakalnicah.
        '''
        sql = """
            SELECT COUNT(id_skakalnice)
            FROM tekma JOIN skakalnica ON skakalnica=id_skakalnice
            WHERE tip_skakalnice = 'velika' AND tekmovanje = 'svetovni pokal'
        """
        for stevilo in conn.execute(sql):
            return stevilo
    

    @staticmethod
    def poisci(niz):
        """
        Vrne vse skakalnice, ki v imenu kraja vsebujejo dani niz.
        """
        sql = "SELECT kraj, velikost, drzava, tip_skakalnice FROM skakalnica WHERE kraj LIKE ?"
        for kraj, velikost, drzava, tip_skakalnice in conn.execute(sql, [f'%{niz}%']):
            yield Skakalnica(kraj=kraj, velikost=velikost, drzava=drzava, tip_skakalnice=tip_skakalnice)
            
    @staticmethod
    def poisci1(niz):
        """
        Vrne vse skakalnice, ki v imenu kraja vsebujejo dani niz.
        """
        sql = "SELECT kraj, tip_skakalnice FROM skakalnica WHERE kraj LIKE ?"
        for kraj, tip_skakalnice in conn.execute(sql, [f'%{niz}%']):
            yield [kraj, tip_skakalnice]
            
    @staticmethod
    def poisci2(niz1, niz2):
        """
        Vrne vse skakalnice, ki v imenu kraja vsebujejo dani niz1 in v tip_skakalnice vsebujejo dani niz2.
        """
        sql = "SELECT kraj, velikost, ime_drzave, tip_skakalnice FROM skakalnica JOIN drzava ON drzava = kratica WHERE kraj LIKE ? AND tip_skakalnice LIKE ?"
        for kraj, velikost, ime_drzave, tip_skakalnice in conn.execute(sql, [f'%{niz1}%', f'%{niz2}%']):
            yield [kraj, velikost, ime_drzave, tip_skakalnice]


    def najveckrat_prirediteljice():
        """
        Vrne vse skakalnice, ki po številu prirejenih tekem.
        """
        sql =   """ SELECT kraj, drzava, velikost, COUNT(skakalnica)
                    FROM tekma JOIN skakalnica ON skakalnica = id_skakalnice
                    WHERE tekmovanje = 'svetovni pokal'
                    GROUP BY skakalnica
                    ORDER BY COUNT(skakalnica) DESC
                """
        for kraj, drzava, velikost, stevilo in conn.execute(sql):
            yield [kraj, drzava, velikost, stevilo]
        
        
    def dodaj_v_bazo(self):
        '''
        Doda skakalnico v bazo.
        '''
        assert self.id_skakalnice is None
        with conn:
            self.id_skakalnice = skakalnica.dodaj_vrstico(kraj=self.kraj, velikost=self.velikost, drzava=self.drzava, tip_skakalnice=self.tip_skakalnice)
            return self.id_skakalnice

class Drzava():
    '''
    Razred za države.
    '''
    def __init__(self, kratica, ime_drzave, populacija, bdp):
        self.kratica = kratica
        self.ime_drzave = ime_drzave
        self.populacija = populacija
        self.bdp = bdp

    def __str__(self):
        return f'{self.ime_drzave}'
    
    def po_zmagah():
        '''
        Razporedi države po številu zmag v pokalu.
        '''
        sql = """ 
            SELECT ime_drzave, COUNT(mesto) 
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON tekma = id_tekme
            WHERE mesto = 1 AND tekmovanje = 'svetovni pokal'
            GROUP BY drzava
            ORDER BY COUNT(mesto) DESC
        """
        for drzava, stevilo in conn.execute(sql):
            yield [drzava, stevilo]

    def po_stopnickah():
        '''
        Razporedi države po številu stopničk v pokalu.
        '''
        sql = """ 
            SELECT ime_drzave, COUNT(mesto) 
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON tekma = id_tekme
            WHERE mesto BETWEEN 1 AND 3 AND tekmovanje = 'svetovni pokal'
            GROUP BY drzava
            ORDER BY COUNT(mesto) DESC
        """
        for drzava, stevilo in conn.execute(sql):
            yield [drzava, stevilo]

    def po_top_deset():
        '''
        Razporedi tekmovalke po številu uvrstitev med najboljših 10 v pokalu.
        '''
        sql = """ 
            SELECT ime_drzave, COUNT(mesto) 
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON tekma = id_tekme
            WHERE mesto BETWEEN 1 AND 10 AND tekmovanje = 'svetovni pokal'
            GROUP BY drzava
            ORDER BY COUNT(mesto) DESC
        """
        for drzava, stevilo in conn.execute(sql):
            yield [drzava, stevilo]

    def po_tockah():
        '''
        Razporedi države po številu osvojenih točk v pokalu.
        '''
        sql = """ 
            SELECT ime_drzave, SUM(tocke) 
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tockovanje ON rezultat.mesto = tockovanje.mesto
            JOIN tekma ON tekma = id_tekme
            WHERE tekmovanje = 'svetovni pokal'
            GROUP BY ime_drzave
            ORDER BY SUM(tocke) DESC
        """
        for drzava, tocke in conn.execute(sql):
            yield [drzava, tocke]

    def po_medaljah_ol():
        '''
        Razporedi države po številu osvojenih medalj na olimpjskih igrah.
        '''
        sql = """ 
            SELECT ime_drzave,
            COUNT(CASE WHEN mesto = 1 THEN 1 END) AS zlate,
            COUNT(CASE WHEN mesto = 2 THEN 1 END) AS srebrne,
            COUNT(CASE WHEN mesto = 3 THEN 1 END) AS bronaste
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON tekma = id_tekme
            WHERE tekmovanje = 'olimpijske igre'
            GROUP BY ime_drzave
            ORDER BY zlate DESC, srebrne DESC, bronaste DESC
            LIMIT 6
        """
        for drzava, zlate, srebrne, bronaste in conn.execute(sql):
            yield [drzava, zlate, srebrne, bronaste]

    def po_medaljah_sp():
        '''
        Razporedi države po številu osvojenih medalj na svetovnih prvenstvih.
        '''
        sql = """ 
            SELECT ime_drzave,
            COUNT(CASE WHEN mesto = 1 THEN 1 END) AS zlate,
            COUNT(CASE WHEN mesto = 2 THEN 1 END) AS srebrne,
            COUNT(CASE WHEN mesto = 3 THEN 1 END) AS bronaste
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tekma ON tekma = id_tekme
            WHERE tekmovanje = 'svetovno prvenstvo'
            GROUP BY ime_drzave
            ORDER BY zlate DESC, srebrne DESC, bronaste DESC
            LIMIT 8
        """
        for drzava, zlate, srebrne, bronaste in conn.execute(sql):
            yield [drzava, zlate, srebrne, bronaste]

    def tocke_na_milijon_preb():
        '''
        Razporedi države po osvojenih točkah na 1.000.000 prebivalcev.
        '''
        sql = """
            SELECT ime_drzave, SUM(tocke) / (populacija / 1000000) 
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tockovanje ON rezultat.mesto = tockovanje.mesto
            JOIN tekma ON tekma = id_tekme
            WHERE tekmovanje = 'svetovni pokal'
            GROUP BY ime_drzave
            ORDER BY SUM(tocke) / (populacija / 1000000) DESC
        """
        for drzava, na_populacijo in conn.execute(sql):
            yield [drzava, na_populacijo]

    def tocke_na_miljardo_bdp():
        '''
        Razporedi države po osvojenih točkah glede na miljarde bdp-ja.
        '''
        sql = """
            SELECT ime_drzave, ROUND(SUM(tocke) / bdp, 2) 
            FROM drzava JOIN tekmovalka ON drzava = kratica
            JOIN rezultat ON id_tekmovalke = tekmovalka
            JOIN tockovanje ON rezultat.mesto = tockovanje.mesto
            JOIN tekma ON tekma = id_tekme
            WHERE tekmovanje = 'svetovni pokal'
            GROUP BY ime_drzave
            ORDER BY ROUND(SUM(tocke) / bdp, 2) DESC
        """
        for drzava, na_bdp in conn.execute(sql):
            yield [drzava, na_bdp]

    