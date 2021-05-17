Predmet: Sistem za rukovanje smenama u preduzeću.

Funkcionalne mogucnosti

Korisnički nalozi

KN1. Aplikacija zaštićena od neautorizovanog pristupa (na frontu i na backu). Pristup aplikaciji omogućen putem standardnog login ekrana (username, password).
KN2. Omogućeno dodavanje novih korisnika aplikacije od strane Administratora.
KN3. Korisnici se mogu sami registrovati za korišćenje aplikacije, pri čemu se potvrda registracije vrši preko korisnikovog email-a, a uz to Administrator mora da odobri svakog novog korisnika i dodeli mu ulogu.
KN4. Aplikacija podržava dve različite korisničke uloge (role):
Administrator: Ima dodeljene sve privilegije
Radnik: Ima pravo pristupa određenom podskupu funkcionalnosti aplikacije (opisano ispod).

Administracija plana smena

PS1. Plan smena se kreira za svaki dan i obuhvata:
- Definisanje početka i kraja svake smene
- Definisanje za koje radno mesto je vezana smena
- Definisanje broja potrebnih radnika za datu smenu.

Na primer, neka imamo preduzeće za dostavu sa radnim mestima: vozač i radnik u magacinu. Plan smene za neki dan bi mogao da izgleda ovako:
07:00-12:00 vozač x2
10:00-14:00 vozač x1
12:00-17:00 vozač x3
14:00-20:30 vozač x3
17:00-23:00 vozač x1
07:00-15:00 radnik u magacinu x2
15:00-23:00 radnik u magacinu x2

PS2. Omogućen pregled, izmena i brisanje smena od strane Administratora.
PS3. Ukoliko je ulogovan Radnik onemogućena izmena podataka o smeni (tj. mogu samo da pregledaju podatke o smenama).

Dodela smena radnicima

RS1. Administrator ima mogućnost da za svaku smenu odredi koji radnici će u njoj raditi.
RS2. Radnici imaju mogućnost da se sami prijave za smenu u kojoj još ima mesta, tj. gde je potreban broj radnika veći od dodeljenih.
RS3. Radnik ne može da vrši izmene već dodeljenih radnika (ne može da ih izbriše niti da dodeli smeni nekog drugog radnika, sem sebe).
RS3. Radnici koji su dodeljeni nekoj smeni mogu da traže od svojih kolega zamenu:
- Radnik obeležava smenu za koju traži zamenu.
- Drugi radnici vide smene za koje se traži zamena i mogu za njih da se prijave (tj. da je dodele sebi).
RS4. Radnik se može dodeliti samo smeni koja odgovara njegovom radnom mestu. Jednom radniku može da bude dodeljeno više radnih mesta (npr. može jedan dan da radi kao vozač, a sledeći dan u magacinu).

Evaluacija smena

ES1. Administrator ima mogućnost da upiše kada je radnik započeo smenu i kada je završio.
ES2. Administrator ima mogućnost da upiše da radnik nije došao na posao i razlog za to.
ES3. Radnici mogu da vide podatke o evaluaciji svojih smena (podatke koje je Administrator uneo), bez prava na izmenu.
ES4. Radnici imaju mogućnost da obeleže da neku smenu neće odraditi i razlog za to. Ova izmena je dozvoljena samo za sopstvenu smenu.
ES5. Sistem može da izračuna naknadu za radnika za datu smenu (potreban je podatak kolika je cena radnog sata za dato radno mesto).

Notifikacije

NT1. Stranica sa notifikacijama prikazuje sve notifikacije relevantne za ulogovanog korisnika, sortirane po datumu od najnovije ka najstarijoj.
NT2. Notifikacije obuhataju sledeće događaje:
- Administrator je dodelio smenu radniku. Notifikaciju vidi: Radnik.
- Administrator je obrisao dodeljenu smenu za radnika. Notifikaciju vidi: Radnik. 
- Radnik je sebi dodelio smenu. Notifikaciju vide: Administrator i Radnik.
- Radnik je obeležio da neće odraditi smenu. Notifikaciju vide: Administrator i Radnik. 
- Radnik je tražio zamenu za smenu. Notifikaciju vide: svi.
- Neko se prijavio za smenu za koju je tražena zamena. Notifikaciju vide: oba Radnika uključena u razmenu smene.

Live shifts

- stranica sa pregledom tekućih podataka o smenama (link u donjem desnom uglu ekrana):
1. Radnici koji sada imaju aktivnu smenu, sa oznakom da li su prisutni (ulogovani). 
 - Ako radnik kasni više od 5 minuta, oznacen crvenim satom.
2. Ako je radnik i dalje ulogovan, a smena mu je prošla, oznacen zelenim satom (overtime 1 sat).
3. Radnici kojima smena počinje u sledećih 2 sata.
Radnici koji su ulogovani, ali nemaju trenutno smenu.
