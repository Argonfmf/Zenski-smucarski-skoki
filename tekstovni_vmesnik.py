from model import Tekmovalka, Skakalnica
from pomozne_funkcije import Meni, JaNe, prekinitev

def vnesi_izbiro(moznosti):
    '''
    Uporabniku da na izbiro podane možnosti.
    '''
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")

def izpisi_podatke_tekmovalka(tekmovalka): 
    '''
    Izpiše podatke o tekmovalki.
    '''
    print(tekmovalka.ime_priimek, tekmovalka.letnica_rojstva, tekmovalka.drzava)

def izpisi_podatke_skakalnica(skakalnica):
    '''
    Izpiše podatke o skakalnici.
    '''
    print(skakalnica.kraj, skakalnica.velikost, skakalnica.drzava, skakalnica.tip_skakalnice)

def izpise_stevilo_tekem_skakalnica(skakalnica):
    '''
    Izpiše število tekem na skakalnici.
    '''
    for stevilo in skakalnica.stevilo_tekem():
        print(stevilo)
        
def izpise_stevilo_zmag(tekmovalka):
    '''
    Izpiše število zmag dane tekmovalke.
    '''
    for stevilo in tekmovalka.stevilo_zmag():
        print(stevilo)
        
def izpise_stevilo_stopnick(tekmovalka):
    '''
    Izpiše število stopničk dane tekmovalke.
    '''
    for stevilo in tekmovalka.stevilo_stopnick():
        print(stevilo)

def izpise_stevilo_olimpijskih_medalj(tekmovalka):
    '''
    Izpiše število olimpijskih medalj dane tekmovalke.
    '''
    for stevilo in tekmovalka.stevilo_medalj_olimpijske():
        print(stevilo)

def izpise_stevilo_medalj_svetovnega_prvenstva(tekmovalka):
    '''
    Izpiše število medalj s svetovnega prvenstva dane tekmovalke.
    '''
    for stevilo in tekmovalka.stevilo_medalj_svetovno_prvenstvo():
        print(stevilo)
        
def izpisi_podatke_sezone(sezona):
    '''
    Izpiše prvih deset tekmovalk dane sezone.
    '''
    for i, elt in enumerate(sezona, 1):
        print(f'{i}) {elt[0]}, {elt[1]} točk')

def poisci_tekmovalko():
    '''
    Poišče tekmovalko, ki jo vnese uporabnik.
    '''
    while True:
        ime_tekmovalke = input('Katera tekmovalka te zanima? ')
        tekmovalke = list(Tekmovalka.poisci(ime_tekmovalke))
        if len(tekmovalke) == 1:
            return tekmovalke[0]
        elif len(tekmovalke) == 0:
            print('Te tekmovalke ne najdem. Poskusi znova.')
        else:
            print('Našel sem več tekmovalk, katera od teh te zanima?')
            return vnesi_izbiro(tekmovalke)

def poisci_skakalnico():
    '''
    Poišče skakalnico, ki jo vnese uporabnik.
    '''
    while True:
        ime_skakalnice = input('Katera skakalnica te zanima? ')
        skakalnice = list(Skakalnica.poisci(ime_skakalnice))
        if len(skakalnice) == 1:
            return skakalnice[0]
        elif len(skakalnice) == 0:
            print('Te skakalnice ne najdem. Poskusi znova.')
        else:
            print('Našel sem več skakalnic, kateri od teh te zanima?')
            return vnesi_izbiro(skakalnice)

def poisci_sezono():
    '''
    Poišče sezono, ki jo vnese uporabnik.
    '''
    while True:
        sezona = input('Katera sezona te zanima? ')
        sezona1 = list(Tekmovalka.najboljse_v_sezoni(sezona))
        if len(sezona1) == 0:
            print('Te sezone ne najdem. Poskusi znova.')
        else:
            return sezona1

@prekinitev
def iskanje_tekmovalke():
    '''
    Izpiše podatke od tekmovalke, ki jo vnese uporabnik.
    '''
    tekmovalka = poisci_tekmovalko()
    izpisi_podatke_tekmovalka(tekmovalka)
    while True:
        print('Te zanima še kaj o tekmovalki?')
        dodaj = vnesi_izbiro(JaNe)
        if dodaj == JaNe.NE:
            break
        dodaj = vnesi_izbiro(('Število zmag', 'Število stopničk', 'Število olimpijskih medalj', 'Število medalj s svetovnega prvenstva'))
        if dodaj == 'Število zmag':
            izpise_stevilo_zmag(tekmovalka)
        elif dodaj == 'Število stopničk':
            izpise_stevilo_stopnick(tekmovalka)
        elif dodaj == 'Število olimpijskih medalj':
            izpise_stevilo_olimpijskih_medalj(tekmovalka)
        elif dodaj == 'Število medalj s svetovnega prvenstva':
            izpise_stevilo_medalj_svetovnega_prvenstva(tekmovalka)
            
@prekinitev
def vrstni_red_sezone():
    '''
    Izpiše vrstni red prvih desetih tekmovalk sezone, ki jo vnese uporabnik.
    '''
    sezona = poisci_sezono()
    izpisi_podatke_sezone(sezona)

@prekinitev
def iskanje_skakalnice():
    '''
    Izpiše podatke od skakalnice, ki jo vnese uporabnik.
    '''
    skakalnica = poisci_skakalnico()
    izpisi_podatke_skakalnica(skakalnica)
    while True:
        print('Te zanima še število prirejenih tekem na skakalnici?')
        dodaj = vnesi_izbiro(JaNe)
        if dodaj == JaNe.NE:
            break
        izpise_stevilo_tekem_skakalnica(skakalnica)
        break

@prekinitev
def dodajanje_tekmovalke():
    """
    Doda tekmovalko z imenom, letnico rojstva in kratico države iz katere prihaja, ki ga vnese uporabnik.
    """
    ime_priimek = input('Napiši ime in priimek tekmovalke, ki jo želiš dodati: ')
    letnica_rojstva = None
    while letnica_rojstva is None:
        try:
            letnica_rojstva = int(input('Napiši katerega leta se je tekmovalka rodila: '))
        except ValueError:
            print("Leto mora biti celo število!")
    drzava = input('Dodaj mednarodno kratico države iz katere prihaja tekmovalka: ')
    tekmovalka = Tekmovalka(ime_priimek, letnica_rojstva, drzava)
    id_tekmovalke = tekmovalka.dodaj_v_bazo()
    print(f'Tekmovalka {ime_priimek} dodana z ID-jem {id_tekmovalke}.')

@prekinitev
def dodajanje_skakalnice():
    """
    Doda skakalnico z imenom kraja, tipom, velikostjo skakalnice in kratico države v kateri se nahaja, ki ga vnese uporabnik.
    """
    kraj = input('Napiši kraj skakalnice, ki jo želiš dodati: ')
    velikost = None
    while velikost is None:
        try:
            velikost = int(input('Napiši velikost skakalnice: '))
        except ValueError:
            print("Velikost mora biti celo število!")
    drzava = input('Dodaj mednarodno kratico države iz katere je skakalnca: ')
    tip_skakalnice = input('Napiši ali je skakalnica "srednja" ali "velika": ')
    skakalnica = Skakalnica(kraj, velikost, drzava, tip_skakalnice)
    id_skakalnice = skakalnica.dodaj_v_bazo()
    print(f'Skakalnica {kraj}, ki ima velikost {velikost} m, dodana z ID-jem {id_skakalnice}.')

def koncal():
    """
    Pozdravi pred izhodom.
    """
    print('Adijo!')

class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    ISKAL_TEKMOVALKO = ('Iskal tekmovalko', iskanje_tekmovalke)
    ISKAL_SKAKALNICO = ('Iskal skakalnico', iskanje_skakalnice)
    POGLEDA_VRSTNI_RED_SEZONE = ('Pogledal vrstni red sezone', vrstni_red_sezone)
    DODAL_TEKMOVALKO = ('Dodal tekmovalko', dodajanje_tekmovalke)
    DODAL_SKAKALNICO = ('Dodal skakalnico', dodajanje_skakalnice)
    KONCAL_POIZVEDBO = ('Končal poizvedbo', koncal)

@prekinitev
def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi ženskih smačarskih skokov!')
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.KONCAL_POIZVEDBO:
            return


glavni_meni()