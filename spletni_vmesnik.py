import json
import random
import bottle
from model import Tekmovalka, Skakalnica, Drzava


@bottle.get('/')
def zacetna_stran():
    return bottle.template(
        'zacetna_stran.html',
    )

@bottle.get('/sezone/')
def sezone():
    return bottle.template(
        'sezone.html',
    )

@bottle.get('/najboljsih-10-tekmovalk/')
def najboljsih_10_tekmovalk():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    tekmovalke = Tekmovalka.najboljse_v_sezoni(iskalni_niz)
    return bottle.template(
        'rezultati_iskanja_sezone.html',
        iskalni_niz=iskalni_niz,
        tekmovalke=tekmovalke
    )

@bottle.get('/najboljsih-10-drzav/')
def najboljsih_10_drzav():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    drzave = Tekmovalka.najboljse_drzave_v_sezoni(iskalni_niz)
    return bottle.template(
        'rezultati_iskanja_sezone1.html',
        iskalni_niz=iskalni_niz,
        drzave=drzave
    )

@bottle.get('/tekmovalke/')
def tekmovalke():
    return bottle.template(
        'tekmovalke.html',
    )
@bottle.get('/isci-tekmovalko/')
def isci_tekmovalko():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    ime_priimek = Tekmovalka.poisci1(iskalni_niz)
    return bottle.template(
        'iskanje_tekmovalke.html',
        iskalni_niz=iskalni_niz,
        ime_priimek=ime_priimek,
    )

@bottle.get('/isci-tekmovalko/<ime_priimek>/')
def podatki_o_izbrani_tekmovalki(ime_priimek):
    return bottle.template(
        'iskanje_tekmovalke1.html',
        ime_priimek=ime_priimek,
        a=Tekmovalka.poisci2(ime_priimek),
        b=Tekmovalka.stevilo_stopnick1(ime_priimek),
    )

@bottle.get('/razvrstitev-stevilo-zmag/')
def razvrstitev_stevilo_zmag():
    return bottle.template(
        'razvrstitev_stevilo_zmag.html',
        a = Tekmovalka.po_zmagah()
    )

@bottle.get('/razvrstitev-stevilo-stopnick/')
def razvrstitev_stevilo_stopnick():
    return bottle.template(
        'razvrstitev_stevilo_stopnick.html',
        a = Tekmovalka.po_stopnickah()
    )

@bottle.get('/razvrstitev-stevilo-top-deset/')
def razvrstitev_stevilo_top_deset():
    return bottle.template(
        'razvrstitev_stevilo_top_deset.html',
        a = Tekmovalka.po_top_deset()
    )

@bottle.get('/razvrstitev-tocke/')
def razvrstitev_tocke():
    return bottle.template(
        'razvrstitev_tocke.html',
        a = Tekmovalka.po_tockah()
    )

@bottle.get('/razvrstitev-stevilo-ol-medalj/')
def razvrstitev_stevilo_ol_medalj():
    return bottle.template(
        'razvrstitev_stevilo_ol_medalj.html',
        a = Tekmovalka.po_medaljah_ol()
    )

@bottle.get('/razvrstitev-stevilo-sp-medalj/')
def razvrstitev_stevilo_sp_medalj():
    return bottle.template(
        'razvrstitev_stevilo_sp_medalj.html',
        a = Tekmovalka.po_medaljah_sp()
    )

@bottle.get('/drzave/')
def drzave():
    return bottle.template(
        'drzave.html',
    )

@bottle.get('/drzave-razvrstitev-stevilo-zmag/')
def drzave_razvrstitev_stevilo_zmag():
    return bottle.template(
        'drzave_razvrstitev_stevilo_zmag.html',
        a = Drzava.po_zmagah()
    )

@bottle.get('/drzave-razvrstitev-stevilo-stopnick/')
def drzave_razvrstitev_stevilo_stopnick():
    return bottle.template(
        'drzave_razvrstitev_stevilo_stopnick.html',
        a = Drzava.po_stopnickah()
    )

@bottle.get('/drzave-razvrstitev-stevilo-top-deset/')
def drzave_razvrstitev_stevilo_top_deset():
    return bottle.template(
        'drzave_razvrstitev_stevilo_top_deset.html',
        a = Drzava.po_top_deset()
    )

@bottle.get('/drzave-razvrstitev-tocke/')
def drzave_razvrstitev_tocke():
    return bottle.template(
        'drzave_razvrstitev_tocke.html',
        a = Drzava.po_tockah()
    )

@bottle.get('/drzave-razvrstitev-stevilo-ol-medalj/')
def drzave_razvrstitev_stevilo_ol_medalj():
    return bottle.template(
        'drzave_razvrstitev_stevilo_ol_medalj.html',
        a = Drzava.po_medaljah_ol()
    )

@bottle.get('/drzave-razvrstitev-stevilo-sp-medalj/')
def drzave_razvrstitev_stevilo_sp_medalj():
    return bottle.template(
        'drzave_razvrstitev_stevilo_sp_medalj.html',
        a = Drzava.po_medaljah_sp()
    )

@bottle.get('/drzave-razvrstitev-na-milijon/')
def drzave_razvrstitev_na_milijon():
    return bottle.template(
        'drzave_razvrstitev_na_milijon.html',
        a = Drzava.tocke_na_milijon_preb()
    )

@bottle.get('/drzave-razvrstitev-na-milijardo-bdp/')
def drzave_razvrstitev_na_milijardo_bdp():
    return bottle.template(
        'drzave_razvrstitev_na_milijardo_bdp.html',
        a = Drzava.tocke_na_miljardo_bdp()
    )

@bottle.get('/skakalnice/')
def skakalnice():
    return bottle.template(
        'skakalnice.html',
    )

@bottle.get('/isci-skakalnico/')
def isci_skakalnico():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    kraj = Skakalnica.poisci1(iskalni_niz)
    return bottle.template(
        'iskanje_skakalnice.html',
        iskalni_niz=iskalni_niz,
        kraj=kraj,
    )

@bottle.get('/isci-skakalnico/<kraj>/<tip_skakalnice>/')
def podatki_o_izbrani_skakalnici(kraj, tip_skakalnice):
    return bottle.template(
        'iskanje_skakalnice1.html',
        kraj=kraj,
        tip_skakalnice=tip_skakalnice,
        a=Skakalnica.poisci2(kraj, tip_skakalnice)
    )

@bottle.get('/najveckrat-prirediteljice/')
def najveckrat_prirediteljice():
    return bottle.template(
        'najveckrat_prirediteljice.html',
        a=Skakalnica.najveckrat_prirediteljice()
    )
    
@bottle.get('/stevilo-tekem/')
def stevilo_tekem_tip():
    return bottle.template(
        'stevilo_tekem_tip.html',
        a=Skakalnica.stevilo_tekem_na_srednjih_skakalnicah(),
        b=Skakalnica.stevilo_tekem_na_velikih_skakalnicah(),
    )
bottle.run(debug=True, reloader=True)
