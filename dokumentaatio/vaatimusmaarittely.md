
**Ohjelmointitekniikan harjoitustyö, 2024 P2, Desktop application: Sounds.py**

***Vaatimusmäärittely v.1***

**Sovelluksen yleiskuvaus**

Sovellus on tarkoitettu käytettäväksi bändin treenikämpällä tai kotona harjoiteltaessa sekä keikalla  laitteistoja 
asennettaessa ja testattaessa sekä äänitysstudiolla demobiisien soundeja valittaessa ja muokattaessa samplerille 
kelpaaviksi standardeiksi soundfonteiksi. Tämä viimeisin digitaalisella äänityöasemalla tapahtuva soundfont-vaihe 
on jatkokehitysvaihe, jossa analogiset, usein ns. vintage- soittimet ja laitteet yhdistetään jouhevasti digitaaliseen 
tuotantoketjuun.

Pääpaino on ratkaista sovelluksen avulla keskeisiä bänditoiminnassa havaittuja käytännön ongelmia. Muusikoilla on 
taipumusta hankkia ajan myötä useampia instrumentteja, esim. kitaroita ja niiden ääntä muokkaavia ns. kitarapedaaleja, 
joita löytyy useita per muusikko. Tosimuusikko ei käytä halpoja, digitaaliseen emulaatioon perustuvia multiefektipedaaleja 
vaan niiden pitää olla aitoja analogisia useimmiten vintage-taustaisia ja huipputason ääntä tuottavia yhden päätarkoituksen 
effektejä (esim. distorsion, delay,  reverb, chorus, preamp, compression jne.  pedals). Usein keikalla ja treeneissä 
tarvitaankin erillistä tarrakiinnitykseen perustavaa pedaalilautaa, jotta laitteita pystyy järkevästi käyttämään. 
Ongelmana ei ole pelkästään näiden pedaalien lukumäärä vaan myös mihin järjestykseen ne on parasta sijoittaa signaalitiellä 
ja minkä-laiset asetukset niille pitää säätää, jotta saataisiin aikaan kitaristin lempisoundit keikallakin. Ongelmana 
ei ole pelkästään soundien asettelu lukuisilla potikoilla ja kytkimillä. Lisäksi pitää ottaa keikalle oikeanlaiset 
pedaalin virtalähteet ja tuoreet paristot ja nippu erilaisia piuhoja.  Yleensä vain pedaalien omistaja pystyy suoriutumaan 
tästä, mutta ei hänkään keikalla kaikkea muista. Ongelma on siis kipeä etenkin roudarin kannalta, joka kytkee, säätää ja 
testaa bändin soundin usein vain noin vartin ennenkuin soitto alkaa. Soundcheck alkaa sitten kun kaikki muusikot ovat 
suvainneet saapua kitaroineen keikkapaikalle.

**Sovelluksen käyttäjät eli actorit:**

- artist: esim. kitaristi tai keyboardin soittaja
- manager: roadmanager, stagemanager, producer
- admin: järjestelmän asennus ja ylläpito sekä valvonta

**Sovelluksen käyttötavat eli use caset:**

***1. Artistin käyttötapaukset***

Artisti valitsee laitekomponentit, kytkee sekä säätää ja testaa oman signaalitiensä effektilaudalle ja ottaa siitä 
lopuksi kännykällä valokuvia aiheina sekä koko signaalitien konfiguraatio sekä yksittäisten laitekomponenttien säätönupisto. 
Lopuksi artisti lähettää kuvat ja mahdollisesti äänittämänsä soundinäytteet esim. emailitse administraattorille. 
Artisti myös nimeää omat signature-soundinsa lähetyksen yhteydessä ja antaa ohjeita niiden käyttötarkoituksesta.
Ennen esim. keikkaa tms. soittotilannetta artisti valitsee soittolistan mukaiset soundit biisikohtaisesti ja merkitsee 
niiden nimet tilaisuuden soittolistaan sekä lähettää listan managerille.Samalla artisti sitoutuu tuomaan keikalla 
tarvittavat henkilökohtaiset soittimensa ja pedaalinsa.
Soittotilanteen koittaessa esim. keikalla, artisti vilkaisee biisilistaa ja valitsee soitettavan biisin perusteella 
sopivan soundin ja saa Sounds-sovelluksesta näytöllle valokuvan pedaaliasetelmastaan  sekä tarvittaessa myös detaljoidummat 
valokuvat yksityisen pedaalin nuppien ja kytkimien  asetuksista ko. asetelmassa (analog gear bundle presettings). 
Jos asetelma ei ole enää kovin tuttu voi mahdollisesti myös kuunnella esim. kuulokkeilla Sound sovelluksesta 
vihje-samplen valitusta soundista.

***2. Managerin käyttötapaukset***

Manuaalinen taustatyö: Jos manageri on roadmanager tai stage manager roolissa hän tekee yhteenvedon artisteilta 
saamistaan biisilistoista soundivalintoineen. Mikäli listoja ei kuulu ajoissa artisteilta, käyttää hän ennalta 
sovittua artistin oletussoundivalikoimaa. Yhteenvetolistan manageri sitten lähettää asianosaisille esim. sosiaalisessa 
mediassa (esim. WhatsUp) olevan bändiryhmän kautta, jossa listaa voi helposti kommentoida. Kun soundivalinnat on 
hyväksytty, artistit ovat sitoutuneet tuomaan henkilökohtaiset laitteet ja varusteet keikkapaikalle sekä asentamaan 
ja säätämään ne.
Manageri voi nyt keskittyä bändin yhteisiin asioihin, laitteisiin ja niiden kuljetukseen sekä asennukseen. 
Apuna hänellä on tässä työssä Sounds sovellus, josta hän näkee muusikkojen instrumentit ja laitteet soittolistan perusteella. 
Hän alkaa suunnitella ensimmäiseksi laitteiden sijoittelua esiintymislavalle sekä tarvittavaa mikrofonien asettelua. 
Hän ottaa  avukseen Sound-sovelluksen ja hakee sieltä  sopivalla mikrofoni ja monitorimäärällä (esim. laulajat ja 
rumpali/rummut) varustetun PA-laitteiden ja niihin liittyvän miksauspöydän mallikonfiguraatiot ja säätönuppien sekä 
kytkinten oletusasetusten valokuvat sekä tarvittaessa myös  käyttöohjeen (user guide). Sounds-sovelluksen avulla manageri 
pystyy myös tarkistamaan, että koko järjestelmä on saatavissa toimintakykyiseksi toivotuilla soundeilla ja artistien 
lukumäärällä. Tarkistuksen jälkeen manageri merkitsee manuaalisesti soittolistaan käytettävän PA-laiteasetelman ja mikserin nimet.
Manageri käyttää sovellusta myös täydentävänä apuna laatiessan keikan laitteiston keräilylistaa kuljetusta varten. 
Samoin Sounds-sovellusta käytetään keikan paluukuljetuksen osalta varmistamaan, että kaikki olennaiset äänilaitekomponentit 
ovat paluukuormassa mukana.

***3. Administraattorin käyttötapaukset***

Admin myöntää järjestelmään manager-tason käyttöoikeuksia perustaa järjestelmän tietokannan sekä vastaanottaa laiteasetelmien 
ja säätöjen valokuvia (sekä skaalaa ne sopiviksi) sekä soundien nimi ja käyttötarkoitustietoja sekä muita laitteisto-ohjeita. 
Admin myös huolehtii sovelluksen asennus ja konfigurointiohjeista sekä jakelusta.

**Sounds sovelluksen rakenne:**

Sounds-sovelluksen rakenne perustuu ns. kerrosarkkitehtuuriin:

Sovelluksen *käyttöliittymä* on selkeästi erotettu sovelluslogiikasta.
Koska sovellus perustuu pääasiassa kuvallisen ja audio-informaation käsittelyyn ad-hoc kenttäolosuhteissa on käyttöliittymän 
perustaksi valittu PyGame. Tämä tarjoaa myös hyvät edellytykset eventien käsittelyyn ja nuppianimaatioiden lisäämiseen 
sovelluksen mahdollisissa jatkokehityshankkeissa.

*Sovelluksen logiikka* on erotettu kerrosarkkitehtuuria noudattaen käyttöliittymästä ja tietokannasta. Tietokantapalvelut 
saadaan ORM-rajapinnan avulla korkealla abstraktiotasolla sovelluslogiikan käyttöön.  Sovelluslogiikan toteutus noudattaa 
“keep it simple”-periaatetta ja  funktiot tehdään toteuttamaan vain yhtä asiaa kerrallaan. Luokat ja moduulit toteuttavat 
loogisia kokonaisuuuksia mahdollisimman riippumattomasti.

*Tietokanta*
Tietokantana käytetään PostgreSQL-relaatiotietokantaa ja sen palveluita tarjoillaan sopivan ORM-rajapinnan avulla 
Python-sovellukselle. Silloin kuin sovelluslogiikka on helppo toteuttaa tietokantamekanismien avulla (esim. sql view-
tekniikalla) näin voidaan menetellä. Perustellusti myös suoraa tietokannan käyttöä voidaan joissain tapauksissa 
harkita (sql execute-komento).

**Tietokannan käsiteanalyysi:**

Sovelluksesta on tunnistettu seuraavat entiteetit, joita tietokantataulut kuvaavat:
	-  band
	-  artist
	-  gearbundle
	-  gearbundlesound
	-  gear

Näiden monesta-moneen relaatioita tuetaan lisäksi seuraavilla liitostauluilla:
	-  bandgearbundle
	-  artistgearbundle
	
**Sovelluksen käsitteet eli entiteetit**

Sound-tietokannan käsitekaavio (entity diagram) erillisessä db-diagram.pdf tiedostossa.
