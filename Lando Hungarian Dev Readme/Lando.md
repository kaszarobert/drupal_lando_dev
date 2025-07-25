# Lando dev environment

Docker-alapú fejlesztői környezet Drupal oldalhoz egy paranccsal indítva. A memóriahasználat miatt javasolt egyszerre csak 1 vagy 2 site-ot futtatni.

- [Lando dev environment](#lando-dev-environment)
  - [Parancsok áttekintése](#parancsok-áttekintése)
  - [Landofile írása](#landofile-írása)
    - [Magyarázat](#magyarázat)
    - [Hová tegyem őket](#hová-tegyem-őket)
    - [Alap Lando config](#alap-lando-config)
    - [Szükséges port felszabadítása](#szükséges-port-felszabadítása)
    - [Alap környezet](#alap-környezet)
    - [Egyéni PHP beállítások az appserverhez](#egyéni-php-beállítások-az-appserverhez)
    - [Másik fajta adatbázis-szerver beállítása](#másik-fajta-adatbázis-szerver-beállítása)
    - [Adatbázis-mentés](#adatbázis-mentés)
    - [MySQL/MariaDB slow query log bekapcsolása](#mysqlmariadb-slow-query-log-bekapcsolása)
    - [phpMyAdmin hozzáadása](#phpmyadmin-hozzáadása)
    - [MailPit hozzáadása](#mailpit-hozzáadása)
      - [Ha SMTP-t használ az oldal](#ha-smtp-t-használ-az-oldal)
        - [a) Symfony Mailer](#a-symfony-mailer)
        - [b) Swiftmailer](#b-swiftmailer)
      - [Ha natív PHP sendmailt használ az oldal](#ha-natív-php-sendmailt-használ-az-oldal)
    - [Drush útvonalának manuális megadása](#drush-útvonalának-manuális-megadása)
    - [NodeJS 10 Gulppal hozzáadása](#nodejs-10-gulppal-hozzáadása)
    - [Apache Solr hozzáadása](#apache-solr-hozzáadása)
      - [Ha csak most adod hozzá](#ha-csak-most-adod-hozzá)
      - [Ha már vannak solr core fájlok (amit a + Get config.zip gombbal töltöttél le a Drupalban a Solr Server beállításakor)](#ha-már-vannak-solr-core-fájlok-amit-a--get-configzip-gombbal-töltöttél-le-a-drupalban-a-solr-server-beállításakor)
    - [Varnish hozzáadása](#varnish-hozzáadása)
    - [Redis hozzáadása](#redis-hozzáadása)
    - [Webpack NodeJS 16 Vue CLI-vel](#webpack-nodejs-16-vue-cli-vel)
    - [xdebug PHP extension hozzáadása az appserverhez](#xdebug-php-extension-hozzáadása-az-appserverhez)
      - [1. Alap beállítás](#1-alap-beállítás)
      - [2. Egyéb phpStorm beállítások Windows esetén](#2-egyéb-phpstorm-beállítások-windows-esetén)
        - [2.1 Windows-on futtatott phpStorm esetén további szükséges beállítás](#21-windows-on-futtatott-phpstorm-esetén-további-szükséges-beállítás)
        - [2.2 WSL2 alatt futtatjuk a phpStormot](#22-wsl2-alatt-futtatjuk-a-phpstormot)
      - [3. phpStorm beállítása debugolásra](#3-phpstorm-beállítása-debugolásra)
      - [4. Visual Studio Code beállítása debugolásra](#4-visual-studio-code-beállítása-debugolásra)
      - [5. Használat](#5-használat)
        - [5.1 Használat phpStormban](#51-használat-phpstormban)
        - [5.2 Használat Visual Studio Code-ban](#52-használat-visual-studio-code-ban)
    - [Új PHP extension hozzáadása az appserverhez](#új-php-extension-hozzáadása-az-appserverhez)
    - [wkhtmltopdf telepítése az appserverbe](#wkhtmltopdf-telepítése-az-appserverbe)
    - [Headless Chrome telepítése az appserverbe](#headless-chrome-telepítése-az-appserverbe)
    - [Portok megnyitása a konténerben futtatott szerverekre](#portok-megnyitása-a-konténerben-futtatott-szerverekre)
    - [PHP codestyle check hozzáadása](#php-codestyle-check-hozzáadása)
    - [Lokális szerverek elérése másik gépről vagy mobilról](#lokális-szerverek-elérése-másik-gépről-vagy-mobilról)
      - [Beállítás](#beállítás)
      - [Használat](#használat)
    - [Nginx átirányítások](#nginx-átirányítások)
    - [Hibás konténerek újraépítése](#hibás-konténerek-újraépítése)
      - [Lando frissítési értesítő kikapcsolása](#lando-frissítési-értesítő-kikapcsolása)
      - [Composer nem éri el a packagist.org oldalat IPv6-ról](#composer-nem-éri-el-a-packagistorg-oldalat-ipv6-ról)
    - [Drupal PHPUnit tesztek futtatása](#drupal-phpunit-tesztek-futtatása)
      - [Beállítás](#beállítás-1)
      - [Használat](#használat-1)
      - [Már feltelepített oldalhoz UI tesztek írása](#már-feltelepített-oldalhoz-ui-tesztek-írása)
      - [Tesztek indítása phpStormból](#tesztek-indítása-phpstormból)
    - [PHPStan futtatása](#phpstan-futtatása)
    - [Google Cloud SDK Landoval](#google-cloud-sdk-landoval)
      - [Beállítás](#beállítás-2)
      - [Használat](#használat-2)
    - [Amazon Web Services CLI Landoval](#amazon-web-services-cli-landoval)
      - [Beállítás](#beállítás-3)
      - [Használat](#használat-3)
  
## Parancsok áttekintése

| Név | Parancs |
| ------ | ------ |
| Indítás | `lando start` |
| Leállítás | `lando stop` |
| Információk az URL-ekről | `lando info` |
| Újraindítás (nem változik meg a konténer konfiguráció) | `lando restart` |
| Újraépítés (megváltozik a konténer konfiguráció) | `lando rebuild -y` |
| Egy konténer újraépítése (csak így lehet egyesével szolgáltatásokat újraindítani: https://github.com/lando/lando/issues/1333) | `lando rebuild -s varnish -y` |
| Minden site lekapcsolása | `lando poweroff` |
| Lando-s pluginok frissítése | `lando update && lando setup` |
| SSH az appserver konténerbe | `lando ssh` |
| SSH a solr konténerbe | `lando ssh -s solr` |
| SSH a solr konténerbe root felhasználóval | `lando ssh -s solr --user root` |
| Composer futtatása konténerből | `lando composer` |
| Drush futtatása konténerből | `lando drush` |
| NPM/Gulp futtatása konténerből | `lando npm` |
| NodeJS futtatása konténerből | `lando node` |
| Gulp futtatása konténerből | `lando gulp` |
| Naplók | `lando logs` |
| Apache naplók | `lando logs -s appserver` |
| Apache naplók élőben jelezve folyamatosan | `lando logs -s appserver -f` |
| Legutóbbi 50 naplóbejegyzés | `lando logs \| tail -n 50` |

## Landofile írása

### Magyarázat

| Plugin | README |
| ------ | ------ |
| name | projekt neve |
| recipe | Milyen sablon konfigurációból induljon a build |
| config | A sablon konfigurációban lévő extra beállítások |
| proxy | Az egyes konténereket milyen URL-el érjük el (mindig a 80-as porton, a belső portokat a Landohoz csatolt Traefik átfordítja mindig a 80-asra. Ezért ezeknek külön URL-t kell megadni) |
| tooling | Saját parancsok definiálása, és hogy azok melyik konténerben legyenek futtatva. Ezek így futtathatók majd konzolablakban: `lando parancsnev` |
| services | A sablon konfiguráción kívül megadott extra konténerek. |

### Hová tegyem őket

Javasolt gyűjtőhely a Lando-alapú projekteknek a gépen a `/home/<felhasznalonev>/lando-projects/` mappa.
Ezen belül minden projekt saját almappába kerüljön. Így biztosított, hogy nem lesz jogosultság-probléma a fájlokkal és a mappákkal. Lando-ban futó szerverek a jelenlegi felhasználóval futtatnak parancsokat, olvasnak/írnak fájlokat.

Ha már volt a gépre Apache szerver telepítve, és a `/var/www/html` is használva volt, akkor se javasolt oda tenni a Lando-alapon futtatott oldalakat. Az oka: az a mappa alapból az Apache saját `www-data` felhasználójához tartozik, nem a jelenlegi felhasználónkhoz. Külön állítgatás nélkül ott a jelenlegi felhasználónkkal csak `sudo chmod -R <fajlutvonal> 777` jogosultságokat állítva tudunk majd a fájlokhoz hozzáférni, ami felesleges bonyodalmat okoz csak.

WSL2-t használva se tegyük a Lando-oldalakat a bemountolt Windows-os NTFS/FAT32 fájlrendszer mappáiba, mert így a fájlműveletek (és ezáltal minden más is) nagyon lassúak lesznek.

### Szükséges port felszabadítása

Lando-val tudunk akármennyi és akármilyen URL-t rendelni a szerverekhez, de szigorúan csak a 80 és 443-as porton. Lando-t használva minden kérés egy proxy-n megy át, ami ezt a két portot figyeli. Tehát ha pl.
- konténerben futó Solr localhost:8983-ra hallgat, azt a Lando proxy-ja a gépünkön a solr.drupal1.localhost:80-on teszi elérhetővé.
- konténerben futó BrowserSync localhost:3000-en hallgat, azt a Lando proxy-ja a gépünkön a bs.drupal1.localhost:80-on teszi elérhetővé stb.

Ennek további előnye, hogy semmi körülmény között nem lesz port ütközés más programokkal és szerverekkel a gépen. Így párhuzamosan futhat:
- akármennyi BrowserSync egyszerre (mivel azok tudnak futni a bs.drupal1.localhost, bs.drupal2.localhost, stb. címen egymástól függetlenül).
- több különböző verziójú NodeJS egyszerre, akár párhuzamosan több Lando-alapú oldalból is.
- párhuzamosan futhat 2 oldal, ami teljesen más PHP/Redis/Solr verziókat használ stb.

*Az esetleges működési hibák elkerülése végett ne futtassunk semmit a gépen a 80-as és a 443-as porton! Ha használnánk Apache-szervert és a vhostokat lokálisan, azt kapcsoljuk ki vagy konfiguráljuk át, hogy pl. a 8080-as porton fussanak!*

Ez nem kötelező, de a kevesebb hibalehetőség végett javasolt. Ugyan a Lando keres másik portot ha a 80-as épp foglalt (8080, 8081 stb.), de nem biztos, hogy a futtatott segédprogramjaink és a kódbázisunk minden része ennyire flexibilisen tudja kezelni a portokat. Későbbi bonyodalmak elkerülése végett döntsük el, hogy natívan telepített szerverekkel akarunk fejleszteni, vagy konténerizálva Lando segítségét használva. Ha nem muszáj, ne keverjük a kettőt!

### Alap Lando config

Mielőtt `lando start` paranccsal indítanál oldalat első alkalommal, tedd ezt be a `/home/FELHASZNALONEVED/.lando/config.yml` fájlba (ha nem lenne ilyen, hozd létre):

```
bindAddress: 0.0.0.0
channel: none
maxKeyWarning: 50
setup:
  buildEngine: false

```


### Alap környezet

Pl. drupal1.localhost URL-re, PHP 8.1, MariaDb 10.3, Composer 2-es környezet kialakítása:

A gyökér mappában hozzunk létre egy `.lando.yml` nevű fájlt ezzel a tartalommal (vigyázzunk, hogy a bekezdések ne Tab karaketerrel, hanem szóközzel legyenek):

```
name: drupal1
recipe: drupal9
config:
  webroot: web
  php: '8.1'
  database: mariadb:10.3
  composer_version: '2.3.5'

services:
  database:
    creds:
      user: drupal1
      password: drupal1
      database: drupal1
    config:
      database: .lando/my_custom.cnf

proxy:
  appserver:
    - drupal1.localhost

```

**A name kulcsú elem minden projekt esetén legyen egyedi!**

Database ütköző collation elkerülése végett állítsuk be "utf8mb4_general_ci" alapnak az adatbázishoz. Ehhez hozzuk létre a `.lando` mappában a `my_custom.cnf` fájlt ezzel a tartalommal:

```
[mysqld]
character-set-server  = utf8mb4
collation-server      = utf8mb4_general_ci
```

Adatbázis-szerver beállításai nagyon fontosak a legelején, mert ezt könnyen módosítani nem tudjuk, ha már fel lett telepítve az oldal. (konkrétan: dumpot kell készíteni, majd törölni database konténert és volume-ot, majd újraépíteni, és visszaimportálni a dumpot)

Elindítása: `lando start`

### Egyéni PHP beállítások az appserverhez

A `config:` alatt váltható PHP-verzió. Pl.:
```
  php: '5.5'
  php: '7.0'
  php: '7.2'
  php: '7.4'
  php: '8.0'
  php: '8.1'
  php: '8.2'
```

A `config:` alá ez kerüljön: (igen, az eddigi `config:` alatt lesz még egy `config:`, ez nem elírás)

```
  config:
    php: .lando/php.ini
```

A főmappában hozzunk létre egy `.lando` mappát és abban hozzunk létre egy `php.ini` nevű fájlt az egyéni beállításokkal. Pl. memória limit beállítása:

```
memory_limit = 256M
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

### Másik fajta adatbázis-szerver beállítása

A `config:` alatti `database:` sorban adható meg a szükséges adatbázis és verziója.

Pl.
```
database: mariadb:10.3
database: mariadb:10.5
database: mysql:5.7
database: mysql:8.0
```

Az előbbiekben említett collation beállítása nagyon fontos. Régi mariadb-k `latin1_swedish_ci`-t használnak, az újabb MySQL pedig `utf8mb4_0900_ai_ci`-t. Ezért feltétlenül legyen beállítva a közös, `utf8mb4_general_ci`.

Ha már létező adatbázis-szervert akarunk cserélni, akkor dumpot kell készíteni az eddigiről, és újrabuildelni a projektet (`lando rebuild -y`), majd visszaimportálni a dumpot.

### Adatbázis-mentés

Ez a módszer gyorsabb, mint Drush vagy egyéb PHP-folyamaton keresztül használva, mert a mysqldump és a mysql CLI alkalmazásokat használja.

Tömörített dump készítés a Landofile-ban definiált adatbázisból:

```
lando db-export adatbazisdump.sql
```

Dump importálása a Landofile-ban definiált adatbázisba: (itt .gz vagy .tar.gz tömörített dumpot is importálhatunk)

```
lando db-import adatbazisdump.sql
```

Dump importálása a Landofile-ban nem az alapértelmezetten definiált nevű "drupal2" adatbázisba: (itt nem importálhatunk tömörített dumpot, csak .sql fájlt)

```
lando mysql --user=drupal1 --password=drupal1 --database=drupal2 --host=database < adatbazisdump.sql
```

### MySQL/MariaDB slow query log bekapcsolása

Annyi a teendő, hogy adatbázis-konfigurációs fájlba (előbbiekben ez volt a my_custom.cnf) ezeket beletesszük:

```
slow_query_log = 1
slow_query_log_file = /app/web/sites/default/files/slow-query.log
long_query_time = 1
```

A long_query_time adja meg a küszöbértéket, hogy hány másodperc felettieket logolja. Erről bővebben: https://dev.mysql.com/doc/refman/8.0/en/slow-query-log.html

Megj.
A database konténerben más user van, mint az appserver konténerben. Ezért alapból nem fogja tudni az adatbázis-szerver írni a /app/web/sites/default/files/slow-query.log fájlt, és hibával leáll. Ezért előtte hozzuk létre üresen a fájlt, és adjunk 777-es jogosultságot rá (vagy akár az egész files mappára):

```
> web/sites/default/files/slow-query.log
sudo chmod 777 web/sites/default/files/slow-query.log
```

Csak az adatbázis-szerver újrakonfigurálását így lehet hívni:

```
lando rebuild -s database -y
```

### phpMyAdmin hozzáadása

A `services:` alá ez kerüljön:

```
  phpmyadmin:
    type: phpmyadmin:5.0
    hosts:
      - database
```

A `proxy:` alá ez kerüljön:

```
  phpmyadmin:
    - pma.drupal1.localhost
```

### MailPit hozzáadása

Localhoston e-mail küldő szervert helyettesít. Megnézheted, milyen leveleket küldene ki a szerver anélkül, hogy valódi e-mail küldés történne.

Megj. a MailHog ugyan elterjedtebb hasonló megoldás erre, ám 2020 óta nincs támogatva, egyes HTML maileket nem jelenít meg HTML formájában, ezért nem javasolt többé a használata, lásd a fejlesztő bejelentését: https://github.com/mailhog/MailHog/issues/442#issuecomment-1493415258 Helyette ezt a MailPit megoldást javasolják.

A helyettesítő szerver az `smtp://OLDALNEV_mailpit_1:1025` címen lesz (avagy ha úgy nem menne, akkor próbáld az `smtp://mailpit:1025` címen), ahol `OLDALNEV` a `name` elem a `.lando.yml`-ből. Az ezzel "küldött" e-maileket a http://mail.OLDALNEV.localhost oldalon listázza ki.

A `services:` alá ez kerüljön:

```
  mailpit:
    scanner: false
    api: 3
    type: lando
    services:
      image: axllent/mailpit:v1.13.3
      volumes:
        - mailpit:/data
      ports:
        - 8025 # Web UI.
        - 1025 # SMTP.
      environment:
        MP_MAX_MESSAGES: 5000
        MP_DATA_FILE: /data/mailpit.db
        MP_SMTP_AUTH_ACCEPT_ANY: 1
        MP_SMTP_AUTH_ALLOW_INSECURE: 1
      command: '/mailpit'
    volumes:
      mailpit:

```

A `proxy:` alá ez kerüljön:

```
  mailpit:
    - mail.OLDALNEV.localhost:8025
```


Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Majd attól függően, az oldalon milyen e-mail küldés van megvalósítva, másképp kell beállítani a Drupalt.

#### Ha SMTP-t használ az oldal

##### a) Symfony Mailer

A fent leírtak után a Drupal Symfony Mailert így tudjuk rákötni a settings.php-ben (ez igazából a felületen is beállítható, csak felületen az éles hozzáférést javasolt becommitolni, amit localhoston felülírsz a settings.php-vel):

**Fontos, hogy a Symfony Mailer felületén a /admin/config/system/mailer/transport oldalon adjunk hozzá egy SMTP transportot előbb, aminek az ID-je a configban "smtp" legyen!**

```
$config['symfony_mailer.settings']['default_transport'] = 'smtp';
$config['symfony_mailer.mailer_transport.smtp']['status'] = TRUE;
$config['symfony_mailer.mailer_transport.smtp']['configuration']['host'] = 'OLDALNEV_mailpit_1';
$config['symfony_mailer.mailer_transport.smtp']['configuration']['port'] = 1025;
```

Ezután cache ürítés és a http://mail.OLDALNEV.localhost oldalon fogod látni a kimenő e-maileket.

##### b) Swiftmailer

Drupal Swiftmailer modult így tudjuk rákötni a settings.php-ben:

```
$config['swiftmailer.transport']['transport'] = 'smtp';
$config['swiftmailer.transport']['smtp_host'] = 'OLDALNEV_mailpit_1';
$config['swiftmailer.transport']['smtp_port'] = '1025';
$config['swiftmailer.transport']['smtp_encryption'] = '0';
```

Ezután cache ürítés és a http://mail.OLDALNEV.localhost oldalon fogod látni a kimenő e-maileket.

#### Ha natív PHP sendmailt használ az oldal

Ebben az esetben a sendmail binárist fogjuk helyettesíteni úgy, hogy az appserver image-be is letöltünk egy mailpit binárist, ami továbbítja a leveleket a MailPit szerverünknek SMTP-vel.

Tehát saját image-et kell buildelni az appservernek. Hasonlóan kell eljárni, mint az egyéni PHP extension telepítéskor, a `Dockerfile`-ba pedig ilyesminek kell lennie:

```
FROM devwithlando/php:8.1-apache-4

# A sendmail telepítéséhez biztosítani kell, hogy a sendmail service is fut, ráadásul a hosts fájlt is írni kéne,
# de Mailpit használatához ennél sokkal egyszerűbb, ha csak egy Mailpit binárissal helyettesítjük küldőnek,
# és php.ini-be beállítjuk, hogy a sendmail helyét ez vegye át, illetve melyik Mailpit szervernek továbbítsa a mailt.
RUN curl -sL https://raw.githubusercontent.com/axllent/mailpit/develop/install.sh | bash -
```

A `.lando/php.ini`-be tegyük be ezt a sort:

```
[mail function]
sendmail_path = /usr/local/bin/mailpit sendmail -S OLDALNEV_mailpit_1:1025 -t -i
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y` és a http://mail.OLDALNEV.localhost oldalon fogod látni a kimenő e-maileket.

Ebben az esetben a Drupal oldalon nem kell változtatni beállítást, de azt ne felejtsd, hogy a Drupal alapból nem tud HTML e-maileket kiküldeni ilyen módon, azokra kell a Drupal Symfony Mailer modul.

Egyéb info: ha küldeni akarsz parancssorból próba e-mailt Mailpittel:

- hozz létre egy email.txt fájlt:

```
To: kasza.robert@example.com
From: kasza.robert@example.com
Subject: Test Email3

This is a test email sent using sendmail.

```

Majd futtasd:

```
/usr/local/bin/mailpit sendmail kasza.robert@example.com  < email.txt
```

### Drush útvonalának manuális megadása

Ha a drupal8, drupal9, vagy drupal10 recipe-t használjuk, akkor a drush-t a konténeren kívülről a <gyökérmappa>/vendor/bin/drush útvonalról fogja futtatni (gyökérmappa itt az, ahol a .lando.yml fájl van). 

Ha ez nem ott van, akkor a `tooling:` alá ez kerüljön (pl. lightning profil esetén itt van):

```
  drush:
    service: appserver
    cmd: "/app/docroot/vendor/bin/drush"
```

Itt az appserver konténeren belüli útvonalat kell megadni, ahol az előbb említett <gyökérmappa> be van mountolva a konténeren belül a /app/ útvonalra.

Hívás konténeren kívülről: `lando drush <utasítás>`


### NodeJS 10 Gulppal hozzáadása

A `services:` alá ez kerüljön: (az image neve legyen egyedi minden projektnél, tehát helyettesítsük a `PROJEKTNEV` részt az aktuális projekt nevével!)

```
  node:
    type: node:custom
    overrides:
      build: ./.lando/node_gulp
      image: my/node:10-gulp-PROJEKTNEV
```

A `tooling:` alá ez kerüljön:

```
  npm:
    service: node
  node:
    service: node
  gulp:
    service: node
  yarn:
    service: node
```

A `.lando/node_gulp` mappát hozzuk létre. Benne legyen egy `Dockerfile` nevű fájl (nincs fájlkiterjesztése)! A tartalma ez legyen:

```
FROM node:10
RUN npm install -g gulp-cli@2.3.0
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

### Apache Solr hozzáadása

#### Ha csak most adod hozzá

A `services:` alá ez kerüljön: (A solr core neve itt `drupal9`)

```
  solr:
    type: solr:8.6.0
    core: drupal9
    portforward: true

```

A `proxy:` alá ez kerüljön: (itt elérhető a solr admin felülete)

```
  solr:
    - solr.drupal1.localhost:8983
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Ha ez elindult, állítsd be a Drupalban a Solr Servert (szerver útvonala: solr, port: 8983). Majd töltsd le a config.zip-et és csomagold ki a web/config/solr/drupal9/conf mappába (drupal9 helyett itt a solr core nevét add meg).

Majd folytasd a következő alfejezettel:

#### Ha már vannak solr core fájlok (amit a + Get config.zip gombbal töltöttél le a Drupalban a Solr Server beállításakor)

A `services:` alá ez kerüljön: (A solr core neve itt `drupal9`, és a core config fájljai a `web/config/solr/drupal9/conf` mappában vannak)

```
  solr:
    type: solr:8.6.0
    core: drupal9
    portforward: true
    config:
      dir: web/config/solr/drupal9/conf
    overrides:
      environment:
        LANDO_SOLR_DATADIR: /var/solr/data
```

(elképzelhető, hogy az overrides rész nélkül is felfut valamikor. Legtöbb esetben ez a hibajön elő, ha azt kihagyod: https://github.com/lando/lando/issues/2866, ezért szerepel itt javaslatként)

A `proxy:` alá ez kerüljön: (itt elérhető a solr admin felülete)

```
  solr:
    - solr.drupal1.localhost:8983
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Ha a szerveren a localhoston fut a solr, akkor úgy legyen a git repoban becommitolva. És a lando fejlesztői környezetben pedig írjuk felül a solr szerver címét settings.php-ben:

```
$config['search_api.server.solr_content']['backend_config']['connector_config']['host'] = '<projektnev>_solr_1';
```

... ahol `<projektnev>` helyett add meg a Landofile tetején levő `name:` kulcsában megadott projektnevet. Hacsak a service nevével hivatkoznánk (solr), úgy 2 solr-os projektnél 404-es hibát kapnánk, azért kell a konténer nevét megadni itt.

Lehetséges még, hogy a rendszeren ki kell nyitni a portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

### Varnish hozzáadása

A Varnish konfigurációs fájlt tegyük egy `.lando` mappában belül `default.vcl` névvel!

Ez sajnos 1 esetben nem működik: ha a Drupal oldalon nyelvenként más domainek vannak beállítva (/admin/config/regional/language/detection/url). Ilyen esetben átmenetileg állítsd át, hogy URL prefixek alapján legyenek a nyelvek, és akkor nem fogja a varnish URL-ről mindig az adott nyelv URL-jére vinni.

Vigyázat!
Ebben a vcl fájlban ha localhostra van irányítva a Varnish felől a forgalom a webszerverre, akkor azt módosítani kell erre:

```
# Default backend definition. Set this to point to your content server.
# backend default {
#     .host = "127.0.0.1";
#     .port = "8081";
#     .first_byte_timeout = 300s;
# }
```

Ha ebben a vcl fájlban korlátozzuk IP-cím szerint, hogy ki küldhet PURGE és BAN kéréseket, akkor itt célszerű azt kikommentelni, mert a konténerek indításakor mindig változó lehet az IP-címe, ezért az itt nem tudjuk lefixálni. Ez azt jelenti, hogy a vcl fájlban minden `acl purge {` és `if (!client.ip ~ purge) {` utasításokat kommenteljük ki úgy, hogy a sor legelejére teszünk egy # karaktert, pl. így:

```
# Access control list for PURGE requests.
#acl purge {
#    "127.0.0.1";
#}
```

```
    # Only allow PURGE requests from IP addresses in the 'purge' ACL.
    if (req.method == "PURGE") {
#        if (!client.ip ~ purge) {
#            return (synth(405, "Not allowed."));
#        }
        return (hash);
    }
```

```
    # Only allow BAN requests from IP addresses in the 'purge' ACL.
    if (req.method == "BAN") {
        # Same ACL check as above:
#        if (!client.ip ~ purge) {
#            return (synth(403, "Not allowed."));
#        }

        # Logic for the ban, using the Cache-Tags header. For more info
        # see https://github.com/geerlingguy/drupal-vm/issues/397.
        if (req.http.Cache-Tags) {
            ban("obj.http.Cache-Tags ~ " + req.http.Cache-Tags);
        }
        else {
            return (synth(403, "Cache-Tags header missing."));
        }

        # Throw a synthetic page so the request won't go to the backend.
        return (synth(200, "Ban added."));
    }
```

A `services:` alá ez kerüljön:

```
  varnish:
    scanner: false
    type: varnish:6.0
    backends:
      - appserver
    ssl: true
    config:
      vcl: .lando/default.vcl
    overrides:
      environment:
        VARNISH_BACKEND_HOST: drupal1_appserver_1
        VARNISH_BACKEND_PORT: 80
        VARNISH_ALLOW_UNRESTRICTED_PURGE: 1
        VARNISHD_PARAM_HTTP_RESP_HDR_LEN: 65536
        VARNISHD_PARAM_HTTP_RESP_SIZE: 98304
        VARNISHD_PARAM_WORKSPACE_BACKEND: 131072

```

Ezért a `VARNISH_BACKEND_HOST` mellé ezen projekt appserver konténer nevét kell megadni - tehát cseréld le a kódmintában szereplő `drupal1`-et a Landofile tetején levő `name:` kulcsában megadott projektnévre! Ha Nginx van használva, akkor a `drupal1_appserver_nginx_1` módon kell ezt megadni.

Ismert hiba https://github.com/lando/varnish/issues/5: ha a VARNISH_BACKEND_HOST: appserver lenne, és más Lando projektek is futnak appserver nevű service-el, akkor a Varnish nem biztos, hogy az aktuális projekt appserverére fog mutatni valamiért. Ezért használjuk inkább a konténer nevét. Ha még így is más oldalat nyitna meg, akkor a jelenlegi oldalnál `lando poweroff && lando start` módon lehet átmenetileg javítani a problémát.

A `proxy:` alá ez kerüljön:

```
  varnish:
    - varnish.drupal1.localhost
```

A `tooling:` alá ez kerüljön:

```
  varnishadm:
    service: varnish
    user: root
  varnishstat:
    service: varnish
    user: root
  varnishlog:
    service: varnish
    user: root
```

Az oldal settings.php-jébe ezt kerüljön (a 0805aa0bc1 random számsort a Purge modul generálja ki, így az minden site-ra más lesz, úgyhogy nézzük meg a config fájlok közt a megfelelőt):

```
$config['varnish_purger.settings.0805aa0bc1']['hostname'] = 'drupal1_varnish_1';
$config['varnish_purger.settings.0805aa0bc1']['port'] = 80;
$config['varnish_purger.settings.0805aa0bc1']['http_errors'] = FALSE;

```


Esetünkben ugyan nem kell mást csinálni, de ha a Varnish és az Apache is ugyanazon a szerveren van, akkor a settings.php-ben a `$settings['reverse_proxy']` és a `$settings['reverse_proxy_addresses']` beállításokkal meg kell adni, hol van a Varnish. Ezt itt azért nem kell, mert külön URL-eken van az Apache (http://drupal1.localhost) és a Varnish (http://varnish.drupal1.localhost) - lásd, amit a proxy kulcs alatt adtunk meg.

Ne felejtsük el, hogy a /admin/config/development/performance oldalon ne "no-cache" legyen a Cache-Control headerre beállítva. Ha nincs itt idő megadva, akkor a Varnish csak továbbítja a kéréseket az Apache felé, és nem fog semmit cache-elni.

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Lehetséges még, hogy a rendszeren ki kell nyitni a portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

### Redis hozzáadása

A `services:` alá ez kerüljön:

```
  redis:
    type: redis:5.0.7
    persist: false
    portforward: false
    config:
      server: .lando/redis.conf
```

Hozzunk létre `.lando/redis.conf` fájlt: (alapból a Redis minden elérhető memóriát felhasznál, ezt limitáljuk pl. 1 GB-ra)

```
maxmemory 1GB
maxmemory-policy volatile-lfu
```

A drupal site `settings.php`-jába ez kerüljön: (plusz be kell kapcsolni a `redis` modult)

```
$settings['redis.connection']['host'] = 'redis';
$settings['redis.connection']['port'] = '6379';
$settings['redis.connection']['interface'] = 'PhpRedis';
$settings['redis.connection']['password'] = NULL;
$settings['redis.connection']['base'] = '0';
$settings['cache_prefix'] = 'drupal_';
$settings['cache']['default'] = 'cache.backend.redis';
$settings['cache']['bins']['cache_form'] = 'cache.backend.database';
$settings['container_yamls'][] = 'modules/contrib/redis/example.services.yml';
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

### Webpack NodeJS 16 Vue CLI-vel

A cél, hogy a webpack dev szerver a konténeren belül a 0.0.0.0 hoston fusson pl. 8080-as porton. Majd landoval egyéni webcímet adunk meg proxyval a 80-as portot használva (pl. http://vue.drupal1.localhost), amin keresztül elérjük majd a konténerben futó szervert.

A `services:` alá ez kerüljön: (az image neve legyen egyedi minden projektnél, tehát helyettesítsük a `PROJEKTNEV` részt az aktuális projekt nevével!)

```
  node_vue:
    type: node:custom
    port: 8080
    overrides:
      build: ./.lando/node_vue
      image: my/node:16-vue-PROJEKTNEV
```

A `proxy:` alá ez kerüljön:

```
  node_vue:
    - vue.drupal1.localhost:8080
```

A `tooling:` alá ez kerüljön: (itt adjuk meg, hogy a vue-s nodeJS szerveren futó npm parancsot a vue-npm paranccsal tudjuk elérni. Ez azért jó, hogyha többfajta NodeJS-t használunk, akkor minden szkript a saját verzióját fogja használni)

```
  vue-npm:
    cmd: npm
    service: node_vue
  vue-node:
    cmd: node
    service: node_vue
  vue-yarn:
    cmd: yarn
    service: node_vue
  vue:
    service: node_vue
```

A `.lando/node_vue` mappát hozzuk létre. Benne legyen egy `Dockerfile` nevű fájl (nincs fájlkiterjesztése)! A tartalma ez legyen:

```
FROM node:16
RUN npm install -g "@vue/cli"@4.5.15
```

A vue projekt főmappájába hozzunk létre egy `vue.config.js` fájlt, és abba tegyük ezt bele (ez letiltja a host ellenőrzést):

```
module.exports = {
    devServer: {
        disableHostCheck: true
    }
}
```

A package.json fájlban a "scripts" alá adjuk hozzá legelsőnek a következőt:

```
  "vue-dev": "vue-cli-service serve --host 0.0.0.0 --port 8080",
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Újrabuildelés után a Vue projekt mappájában (a `tooling:` résznél megadottak alapján) így lehet futtatni a fejlesztői szervert (ezzel biztosítjuk, hogy a konténerben futtatott webpack szervert elérhetővé tegyük a konténeren kívülre is):

```
lando vue-npm run vue-dev
```

Hasonló módon lehet futtatni a production buildet:

```
lando vue-npm run build
```

Ha így nem töltődik be az oldal, akkor lehetséges, hogy a rendszeren ki kell nyitni a 8080-as portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

Ha nem webpack, hanem vite-alapú projektet építünk, akkor ott a vite.config.js és package.json-t kell módosítani az eddig leírtakhoz hasonló módon. Lásd a https://dev.to/jiprochazka/starting-up-a-new-vue-3-project-with-vite-and-docker-3355 oldalon a "Setting up the Project for running under the Docker" részt.


### xdebug PHP extension hozzáadása az appserverhez

#### 1. Alap beállítás

A debugolás Xdebug 3 esetén a 9003-as porton fog futni alapból, így phpStormban is azt a portot kell beállítani rá.

Debugolás beállítása https://github.com/lando/lando/issues/1668#issuecomment-772829423 alapján:

A `config:` alá ez kerüljön: (alapból nem lesz a debugolás bekapcsolva)

```
  xdebug: off
  config:
    php: .lando/php.ini
```

A `services:` alá ez kerüljön: (ha már van appserver kulcsú elem a services alatt, akkor azt kell kiegészíteni az alábbi kóddal)

```
  appserver:
    overrides:
      environment:
        PHP_IDE_CONFIG: "serverName=appserver"
        XDEBUG_MODE:

```

A `tooling:` alá ez kerüljön:

```
  xdebug:
    description: Loads Xdebug in the selected mode.
    cmd:
      - appserver: /app/.lando/xdebug.sh
    user: root
```

A főmappában hozzunk létre egy `.lando` mappát és abban hozzunk létre egy `php.ini` nevű fájlt az xdebug beállításokkal: (létező esetén egészítsük ki ezekkel a sorokkal)

```
; Xdebug settings required for PhpStorm.
; https://github.com/lando/lando/issues/1668#issuecomment-772829423
xdebug.start_with_request = yes
xdebug.log_level=0
```

A főmappában hozzunk létre egy `.lando` mappát és abban hozzunk létre egy `xdebug.sh` nevű fájlt az xdebug beállításokkal:

```
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Xdebug has been turned off, please use the following syntax: 'lando xdebug <mode>'."
  echo "Valid modes: https://xdebug.org/docs/all_settings#mode."
  echo xdebug.mode = off > /usr/local/etc/php/conf.d/zzz-lando-xdebug.ini
  /etc/init.d/apache2 reload
else
  mode="$1"
  echo xdebug.mode = "$mode" > /usr/local/etc/php/conf.d/zzz-lando-xdebug.ini
  /etc/init.d/apache2 reload
  echo "Xdebug is loaded in "$mode" mode."
fi
```

Abban az esetben, ha a .lando.yml-ben Nginx-re lett lecserélve az appserver (ha találsz a config: alatt olyat, hogy `via: nginx`), akkor ez az `xdebug.sh` nevű fájl tartalma ez legyen:

```
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Xdebug has been turned off, please use the following syntax: 'lando xdebug <mode>'."
  echo "Valid modes: https://xdebug.org/docs/all_settings#mode."
  echo xdebug.mode = off > /usr/local/etc/php/conf.d/zzz-lando-xdebug.ini
  pkill -o -USR2 php-fpm
else
  mode="$1"
  echo xdebug.mode = "$mode" > /usr/local/etc/php/conf.d/zzz-lando-xdebug.ini
  pkill -o -USR2 php-fpm
  echo "Xdebug is loaded in "$mode" mode."
fi
```


Ebben a fájlban a sorvégződések LF-ek legyenek, ne pedig CRLF (Windows) vagy CR (Mac), különben a debugolás bekapcsolása `OCI runtime exec failed: exec failed: container_linux.go:380 : starting container process caused: no such file or directory: unknown` hibát fog dobni.

Engedélyezzük a szkript futtatását a `chmod +x .lando/xdebug.sh` paranccsal!

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

#### 2. Egyéb phpStorm beállítások Windows esetén

Windows alatt ha WSL2-ben futtatjuk a környezetet 2 féle módon lehet debugolni:
1. Windows alatt futtatjuk a phpStormot
   
   Így debugoláshoz elérhetővé kell tenni Windows számára a docker unix socketet, xdebugot át kell állítani a Windows-os IP-címre, valamint minden Windows újraindítás alkalmával a megváltozó Windows-os IP-cím miatt újra kell építeni MINDIG a projektet.

2. WSL2 alatt futtatjuk a phpStormot
  
   A Windows Subsystem for Linux 2 alatt nemcsak konzolos alkalmazásokat lehet futtatni, hanem grafikus felülettel rendelkezőket is. Így közel natív sebességet érhetsz el, mindent úgy használhatsz, mintha natív Linuxos gépen csinálnád, és nem kell a debugolás miatt újraépíteni a projektet minden nap. 

   Hátránya az, hogy még új és nem teljesen kiforrott megoldás ez. Előfordul néha, hogy a gép alvó állapotból ébresztése után eltűnnek az így megnyitott ablakok, illetve a vágólappal is gond lehet néha.

A továbbiakban részletezem az egyes módszerek esetén mit kell telepíteni, beállítani. Linuxos gépen ez nem kell, az esetben ugorj a "3. phpStorm beállítása debugolásra" fejezetre.

##### 2.1 Windows-on futtatott phpStorm esetén további szükséges beállítás

Mivel így a webszerver egy docker konténeren belül fut a WSL2 virtuális gépen, ezért:

1. A docker socketet elérhetővé kell tenni Windows alatt: (https://gist.github.com/styblope/dc55e0ad2a9848f2cc3307d4819d819f)
  
  ```
  sudo nano /etc/docker/daemon.json
  ```

  A fájl tartalma legyen a következő:

```
  {"hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]}
```

  Ctrl + X majd Y és Enter a mentéshez. Majd:

  ```
  sudo service docker restart
  ```

2. A Windows-os IP-re kell, hogy az xdebug csatlakozzon a client_host beállításával. Ám a jelenlegi IP-cím bármikor megváltozhat, ezért ezt nem jó statikusan beégetni egy fájlba. Helyette hozzunk létre változót ezzel az IP-címmel WSL-ben a .bashrc-ben (https://github.com/lando/lando/issues/1723#issuecomment-821823611):

  ```
  nano ~/.bashrc
  ```

  Adjuk hozzá a következő sort:

  ```
  # Set correct Host IP
  export HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}')
  ```

  Ctrl + X majd Y és Enter a mentéshez. 
  Majd töltsük újra a fájlt a konzol ablakban:  
  ```
  source ~/.bashrc
  ```

3. Mivel ez Windows-specifikus dolog, ezért ezt ne tegyük a fő `.lando.yml` fájlba (mert az a Linuxot használó kollégáknak rontaná el a debugolást), hanem egy mappában azzal a fájllal hozzunk létre egy `.lando.local.yml` fájlt, amiben ezt az 1 felülírást megcsináljuk ezzel a tartalommal (https://github.com/lando/lando/issues/1723#issuecomment-821823611):

  ```
  services:
    appserver:
      overrides:
        environment:
          XDEBUG_CONFIG: client_host=${WSL_IP}

  ```

Ezt a `.lando.local.yml` fájlt tegyük a .gitignore-ba és ne commitoljuk!

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Ennek a megközelítésnek az a hátránya, hogy ahányszor újraindítod a Windows-t, `lando rebuild -y` paranccsal újra kell építeni a projektet a megváltozó IP-cím miatt.

##### 2.2 WSL2 alatt futtatjuk a phpStormot

1.  Windows 10 Build 19044+ vagy Windows 11 esetén a telepített WSL2 alapból támogatja a grafikus felületű alkalmazások futtatását. Bővebben: https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps (ez elvileg működik az "Installed driver for vGPU" telepítése nélkül is, úgyhogy azt átugorhatod).

  Ennél régebbi Windows 10 esetén GWSL (https://opticos.github.io/gwsl/) vagy VCXSRV XServert (https://sourceforge.net/projects/vcxsrv/) kell Windows-ra telepíteni, amivel a Linuxon futó phpStorm ablakát lehet megjeleníteni. Továbbá a DISPLAY környezeti változót is át kell állítanod, hogy a GWSL/VCXSRV meg tudja jeleníteni a képet. Erről bővebben: https://techcommunity.microsoft.com/t5/modern-work-app-consult-blog/running-wsl-gui-apps-on-windows-10/ba-p/1493242 

2. telepítsük fel a phpstormot a WSL2-ben (NEM Windows alatt!): https://www.jetbrains.com/help/phpstorm/installation-guide.html#snap

3. WSL2 konzolból a `phpstorm` parancsot beírva tudjuk elindítani a programot. Vagy a Start menüben is lehet, hogy el lett helyezve parancsikon rá.

#### 3. phpStorm beállítása debugolásra

1. Docker beállítása: File > Settings ablakban Build, Execution, Deployment > Docker részben jobb oldalt nyomjuk meg a + gombot és a Connect to Docker daemon with:
   
  - Linux és WSL2 alatt futtatott phpStorm esetén: Unix socket

  - Windows-on futó phpStorm esetén: TCP socket, és Engine API URL: `tcp://localhost:2375` vagy `tcp://0.0.0.0:2375`

  Ha "Connection successful" választ írja, akkor sikeres a kapcsolódás a Dockerhez.
  
  Nyomj az OK gombra a mentéshez.

2. PHP környezet beállítása
  File > Settings ablakban Languages & Frameworks > PHP részben jobb oldalt:
  
  - PHP Language level: használt PHP-verió
  
  - CLI interpreter: 
  
     1) nyomjuk meg a ... gombot!
   
     2) A megjelenő ablakban bal oldalt a + gombra kattintva válasszuk a "From Docker, Vagrant ..." opciót!
   
     3) SSH helyett válasszuk ki a "Docker Compose" radio buttont!
   
     4) Server: Docker.
   
     5) Configuration files: nyomjunk a jobb oldali mappa ikonra, és a `/home/FELHASZNALOD/.lando/compose/PROJEKTNEV/` mappa alatt jelölj ki MINDEN yml-t! és kattints az OK gombra!

     6) Service: appserver

     7) Mentsük el OK-val

     7) Felül Name legyen `Lando`

     8) Lifecycle alatt legyen bejelölve a `Connect to existing container (docker-compose exec)`
     
     9) Mentsük el OK-val mindent.
  
  A Path mappings-nél ellenőrizzük, hogy a projekt mappája az a /app-ként legyen mappelve a konténeren belül. Elvileg ezt kiolvassa a Lando által generált docker-compose.yml fájlokból, de ha nem, akkor pl. a /opt/project-ről is módosítsuk /app-ra!
   

3. Debug port beállítása

   File > Settings ablakban Languages & Frameworks > PHP > Debug részben jobb oldalt az Xdebug szekcióban a Debug port: 9003 legyen!

4. Szerver fájl mapping beállítása

   File > Settings ablakban Languages & Frameworks > PHP > Servers részben jobb oldalt:

   - Nyomjuk meg a + gombot!

   - Name: virtual host neve, pl. drupal1.localhost (ha több ilyen hostot is definiálva van proxy > appserver kulcs alatt a .lando.yml-ben, akkor mindegyikre külön ilyet létre kell hozni)

   - Host: ugyanaz

   - Port: 80

   - Debugger: Xdebug

   - Pipáljuk be a "Use path mappings" opciót!

   - A megjelenő 2 oszlopos táblázatban a projekt főmappájához (ahol a `.lando.yml` van) írjuk be jobb oldali oszlopba (Absolute path on server) azt, hogy `/app`

   - Ez így lehetővé teszi a böngészőben betöltött oldalak debugolását. Hozzunk létre még egy ugyanilyet csak drupal1.localhost helyett `appserver` name és hosttal! Ez lehetővé teszi a CLI commandok debugolását.

5. Kattintsunk a kék OK-ra a mentéshez!

#### 4. Visual Studio Code beállítása debugolásra

1. VSCODE-ban telepítsd a "PHP Debug" extensiont az Xdebugtól (https://marketplace.visualstudio.com/items?itemName=xdebug.php-debug).

2. Add a projekt főmappájába a .vscode/launch.json fájlt ezzel a tartalommal:

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Listen for XDebug (9003)",
      "type": "php",
      "request": "launch",
      "port": 9003,
      "log": false,
      "pathMappings": {
        "/app/": "${workspaceRoot}/"
      }
    }
  ]
}
```

Javasolt a "log" értékét false-on hagyni, különben a Debug Console minden xdebug hívás paramétert logol, így ha változókat kérünk le Debug Console-ban, akkor az eredmény mellett még 20-50 soros scopesRequest és scopesResponse logolódik be.

#### 5. Használat

Ezentúl ahányszor indítjuk a projektet, az appserver konténeren belül bekapcsolható lesz az xdebug  `lando xdebug debug` parancsot futtatva. Ez bekapcsolja a böngészőhöz és a CLI-hez is a PHP szkriptek debugolását. Kikapcsolható az xdebug menet közben a `lando xdebug off` paranccsal. Nincs szükség a böngészőben az xdebug helper extensionre sem (mivel az xdebug.start_with_request lett beállítva a php.ini-ben).

Lehetséges még, hogy a rendszeren ki kell nyitni a portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

##### 5.1 Használat phpStormban

phpStormban debugolás engedélyezéséhez: Run > Start listening for PHP debug connections menüpontra, vagy az eszköztáron erre a piros sarkú ikonra kattintsunk. Ugyanerre kattintva letilthatjuk a debugolást.

##### 5.2 Használat Visual Studio Code-ban

1. Menj a Run & Debug tabra (Ctrl + Shift + D)

2. Bal oldalt fenn legyen kiválasztva az, hogy "Listen for XDebug (9003)"

3. Nyomd meg a zöld lejátszásra hasonlító gombot!

Forrás: https://gist.github.com/MatthieuScarset/0c3860def9ff1f0b84e32f618c740655

### Új PHP extension hozzáadása az appserverhez

Ehhez a használt php docker image-et kell lecserélni. Ezzel elveszítjük azt a flexibilitást, hogy a .lando.yml fájlban megadható legyen a PHP-verzió, mert php image buildelésekor fogjuk beégetni, melyik php verziót használjuk.

A `services:` alá ez kerüljön: (az image neve legyen egyedi minden projektnél, tehát helyettesítsük a `PROJEKTNEV` részt az aktuális projekt nevével!)

```
  appserver:
    type: php:custom
    overrides:
      build: ./.lando/php
      image: my/php:7.4-PROJEKTNEV
```

A `.lando/php` mappát hozzuk létre. Benne legyen egy `Dockerfile` nevű fájl (nincs fájlkiterjesztése)! A tartalma ez legyen:

```
FROM devwithlando/php:7.4-apache-4

RUN apt-get update -y \
    && pecl install mongodb \
    && docker-php-ext-enable mongodb

```

Ha Nginx-et használsz a projektben, akkor a PHP-FPM-es image-t kell megadni az első sorban:

```
FROM devwithlando/7.4-fpm-4

RUN apt-get update -y \
    && pecl install mongodb \
    && docker-php-ext-enable mongodb

```

PHP extension telepítésére és bekapcsolására a hivatalos php docker image-ben megvalósított segédparancsok használhatóak:
- Ha sima PHP-extensiont telepítünk, pl. jsmin esetén, akkor: `docker-php-ext-install jsmin && docker-php-ext-enable jsmin` (van még a `docker-php-ext-configure`, ha az extension valamely beállítását kívánjuk módosítani)
- Ha PECL-ből letölthető extensiont telepítünk, akkor a fent is látható példa szerint `pecl`-el telepíteni kell, majd `docker-php-ext-enable` paranccsal engedélyezni.

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Bővebben:

https://docs.lando.dev/guides/installing-php-extensions-on-lando.html#_2-using-dockerfiles

https://hub.docker.com/_/php "How to install more PHP extensions" rész

### wkhtmltopdf telepítése az appserverbe

Ehhez saját image-et kell buildelni az appservernek. Hasonlóan kell eljárni, mint az egyéni PHP extension telepítéskor, a Dockerfile-ba pedig ilyesminek kell lennie:

```
FROM devwithlando/php:7.4-apache-4

ARG  jpeg=libjpeg-dev
ARG  ssl=libssl-dev
ENV  CFLAGS=-w CXXFLAGS=-w

RUN apt-get update && apt-get install -y -q --no-install-recommends \
    build-essential \
    libfontconfig1-dev \
    libfreetype6-dev \
    $jpeg \
    libpng-dev \
    $ssl \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    python \
    zlib1g-dev \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.0.3-0ubuntu1_amd64.deb
RUN dpkg -i libjpeg-turbo8_2.0.3-0ubuntu1_amd64.deb
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN apt --fix-broken install
```
Ne felejtsd el, hogyha Nginx-et használ a projekt, akkor az első sorban a PHP-FPM-es image-et kell használnod: `FROM devwithlando/php:7.4-fpm-4`

A `tooling:` alá ez kerüljön: (ha kívülről parancssorból meg akarjuk hívni a wkhtmltopdf-et)

```
  wkhtmltopdf:
    service: appserver
```

Megj. a wkhtmltopdf (https://github.com/wkhtmltopdf/wkhtmltopdf) 2020 óta nincs fejlesztve, 2023-ban a repo archivált állapotú lett. A tudása is kb. 2012 körüli WebKit-alapú böngészővel egyezik meg, ezért manapság már inkább Headless Chrome használata javasolt.


### Headless Chrome telepítése az appserverbe

Ehhez saját image-et kell buildelni az appservernek. Hasonlóan kell eljárni, mint az egyéni PHP extension telepítéskor, a Dockerfile-ba pedig ilyesminek kell lennie:

```
FROM devwithlando/php:8.1-apache-4

# Headless Chrome-nak kell a sockets PHP extension.
RUN docker-php-ext-install sockets

# Headless Chrome telepítése.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && \
    apt-get install -y chromium chromium-driver
# Google Chrome alias a Chromiumhoz
RUN ln -s /usr/bin/chromium /usr/bin/google-chrome

```

Itt telepíthetnénk a google-chrome-stable is, csak az ARM processzoros gépen nem települ fel, ezért használjuk a chromiumot. Ne felejtsd el, hogyha Nginx-et használ a projekt, akkor az első sorban a PHP-FPM-es image-et kell használnod: `FROM devwithlando/php:8.1-fpm-4`

A `tooling:` alá ez kerüljön: (ha kívülről parancssorból meg akarjuk hívni a Headless Chrome-ot manuálisan)

```
  google-chrome:
    service: appserver
    cmd:
      - appserver: /usr/bin/google-chrome --disable-gpu --headless=old --no-sandbox --disable-dev-shm-usage --mute-audio --disable-extensions
```


### Portok megnyitása a konténerben futtatott szerverekre

Ugyan a legtöbb tűzfal engedi a 80-as és 443-as portot a kommunikációra, de lehetséges, hogy az xdebug (9003-as vagy 9000-es port), vagy a NodeJS szerver (8080-as port) nem elérhető, mert a rendszer tűzfala blokkolja azt. Ezt Ubuntun a következőképp lehet tenni: (dport paraméternek meg kell adni a portot) 

`sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 9003 -j ACCEPT`

### PHP codestyle check hozzáadása

Ha szeretnénk Drupal által előírt kódformázási szabályokat ellenőriztetni phpStormban, akkor azt így lehet landot használva használni:

A site composer.json-jához hozzá kell adni:

`lando composer require drupal/coder`

Ha konzolból akarod futtatni, csinálhatunk rá parancsot a landohoz, hogy ne kelljen ssh-zni a php konténerbe. Tehát a tooling alá ez menjen:

```
  phpcs:
    service: appserver
    cmd: "/app/vendor/bin/phpcs --standard=Drupal,DrupalPractice --extensions=php,module,inc,install,test,profile,theme,css,info,txt,md"
    options:
    description: Run phpcs for given folder or file.
  phpcbf:
    service: appserver
    cmd: "/app/vendor/bin/phpcbf --standard=Drupal,DrupalPractice --extensions=php,module,inc,install,test,profile,theme,css,info,txt,md"
    options:
    description: Run phpcs for given folder or file.
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Majd konzolból így lehet a codestyle ellenőrzést lefuttatni, pl. admin_toolbar modul esetén:

```
lando phpcs /app/web/modules/contrib/admin_toolbar
```

PHPStormban beállítható, hogy szerkesztés közben jelezze a codestyle hibákat, hogy ne kelljen mindig a konzolt futtatni újra és újra:
- Végezd el a PHP language level és CLI interpreter, Servers beállítását (Lásd: "phpStorm beállítása debugolásra")
- Languages & Frameworks > PHP > Quality Tools oldalon legyen az External formatters: PHP Code Beautifier and Fixer
- Languages & Frameworks > PHP > Quality Tools > PHP_CodeSniffer oldalon Configuration mellett kattints a ... gombra:
  - bal oldalt a + gombbal add hozzá a ugyanazt a Lando Interpretert, mint előbb.
  - PHP_CodeSniffer path: `/app/vendor/bin/phpcs`
  - PHP Code Beautifier and Fixer Settings-et nyisd le, és ott Path to phpcbf: `/app/vendor/bin/phpcbf`
- PHP_CodeSniffer inspection: ON
- Show warning as: `Weak warning`
- Check files with extensions: `php,module,inc,install,test,profile,theme,css,info,txt,md`
- Coding standard: `Custom`, majd a mellette lévő ... gombra kattintva az ablakban:
- Path to ruleset: `/app/vendor/drupal/coder/coder_sniffer/Drupal/ruleset.xml`
- OK gombbal mentsd el

Forrás:

https://github.com/HBFCrew/lando-docs-examples/blob/master/Drupal-PHPStorm-Lando-Setting-Code-Sniffer-Debugging.md

### Lokális szerverek elérése másik gépről vagy mobilról

Forrás: https://docs.lando.dev/guides/access-by-other-devices.html

Hiába fut a szerver egy porton localhoston, Lando alapértelmezetten csak a 127.0.0.1 címre érkező kéréseket szolgálja ki. Másik gépről az oldalat megnyitva nem a 127.0.0.1-re küldesz kérést, hanem annak a gépnek az IP-címére, ezért az nem fog működni - kapcsolat visszautasítva üzenet fog megjelenni a böngészőben. Szóval nem elég tűzfallal beengedni a kérést a portra, meg kell mondani Lando-nak, hogy szolgálja is ki azt.

#### Beállítás

Ehhez nyisd meg a globális Lando konfigurációs fájlt:

```
nano ~/.lando/config.yml
```

És tedd bele ezeket: (ha csak ez lenne a fájlban: `{}`, akkor töröld ki az üres kapcsos zárójel-párt)

```
# Bind my exposes services to all intefaces
bindAddress: "0.0.0.0"
```

Majd újra kell buildelned a Lando projekteket: `lando rebuild -y`


#### Használat

```
hostname -I | cut -d' ' -f1
```

Ez adja meg az IP címet, pl. 192.168.1.4

Ha LAN-on másik számítógépről akarsz kapcsolódni, akkor az IP-nek 192.168.0.0 – 192.168.255.255 közt kell lennie. Ha az így kapott IP nem innen van, akkor próbáld meg ezzel: `ip route get 1.1.1.1 | grep -o "src 192\.168\.[0-9]\+\.[0-9]\+"`  (https://www.baeldung.com/linux/find-primary-ip-address#1-the-primary-network-interface)

Ha így se kapsz megfelelő IP-t, akkor `ip addr show` kilistázza minden hálózati adaptert és docker networköt és itt megkeresheted, mi is a LAN IP-d.


```
lando info
```

Valami ilyesmit kell kapni erre:
```
 APPSERVER URLS   https://localhost:49158
                  http://localhost:49159
                  http://drupal1.localhost/
                  https://drupal1.localhost/
```

Ez megmondja, melyik portról érhető el az oldal. Pl. a HTTP verzió a 49159-en, tehát mobilról az oldaladat így tudod megnyitni:

```
http://192.168.1.4:49159
```

### Nginx átirányítások

Alapból a drupal9 recipe Apache-ot használ az egyszerűség végett. Ez átkapcsolható PHP-FPM+Nginx-re:

- A .lando.yml-ben felül a config: alatt adjuk hozzá, hogy `via: nginx`

- A config:config alatt, hogy milyen nginx host konfigurációt használunk: `vhosts: .lando/default.conf`

- Ha a proxy: alatt van bejegyzés az appserver-hez, azt módosítsuk `appserver_nginx`-re.

- Ne felejtsd el, hogyha saját Docker image-et használsz az appservernek, annak Dockerfile-jában a PHP-FPM-es image-ból indulj ki. Lásd: [Új PHP extension hozzáadása az appserverhez](#új-php-extension-hozzáadása-az-appserverhez)

  Tehát így kellene kinéznie pl.

```
name: drupal1
recipe: drupal9
config:
  webroot: web
  php: '8.1'
  via: nginx
  database: mariadb:10.3
  composer_version: '2.4.2'
  xdebug: off
  config:
    php: .lando/php.ini
    database: .lando/my_custom.cnf
    vhosts: .lando/default.conf

proxy:
  appserver_nginx:
    - drupal1.localhost

```

- Hozzuk létre a `.lando/default.conf` fájlt! Annak tartalma legyen alapból az, amit a Drupalos Nginx beállításra használ a Lando. Ezt kiderítheted a Lando Drupal recipe github repojából: https://github.com/lando/drupal/blob/main/config/drupal9/default.conf.tpl

- Ehhez a fájlhoz kell adni az átirányításokat alulra, még a server { } blokkon belülre!

- Ne felejtsd el, hogy Nginx-re váltva másképp kell az xdebugot ki- és bekapcsolni, tehát a `.lando/xdebug.sh` fájlt [xdebug PHP extension hozzáadása az appserverhez](#xdebug-php-extension-hozzáadása-az-appserverhez) szerint kell megadni.

- Ha megvan, újra kell buildelned a Lando projekteket: `lando rebuild -y`


### Hibás konténerek újraépítése

Előfordulhat, hogyha nem rendesen állítottuk le a konténereket lando stop paranccsal, akkor sérült lehet pár bináris állomány a konténerben, amiért többé az nem működik. Pl. 
- nem indul be az adatbázis-szerver, a konzolon a lando azt írja többször ki folyamatosan percek óta, hogy `Waiting until database service is ready...`. 
- Esetleg az oldal 404 page not found-ot ír, miközben a PHP fájlok ott vannak a szerveren.
- Ilyet ír a konzol: `Warning: copy(https://getcomposer.org/installer): Failed to open stream: php_network_getaddresses: getaddrinfo for getcomposer.org failed: Temporary failure in name resolution in Command line code on line 1
Could not open input file: /tmp/composer-setup.php
ERROR ==> Could not open input file: /tmp/composer-setup.php`
- curl hibák jelentkeznek minden hívásra: `GuzzleHttp\Exception\ConnectException: cURL error 6: Could not resolve host: updates.drupal.org (see https://curl.haxx.se/libcurl/c/libcurl-errors.html) in GuzzleHttp\Handler\CurlFactory::createRejection() (line 200 of /app/vendor/guzzlehttp/guzzle/src/Handler/CurlFactory.php)`.

Ez WSL2 (Windows Subsystem for Linux) alatt futó dockerrel szokott előjönni sajnos gyakran.

1. próbálkozás javításra:

```
lando rebuild -y
```

2. próbálkozás javításra: ha az előző se segít, akkor próbáljuk újrabuildelni őket:

```
lando poweroff
docker system prune
lando start
```

Forrás: https://github.com/lando/lando/issues/1264

#### Lando frissítési értesítő kikapcsolása

Ha új stable release van kiadva, akkor minden lando-val kiadott parancs a konzolon ezzel a bazi nagy üzenettel íródik ki pluszban:

```
pc@pc:~/lando-projects/drupal1.localhost(master)$ lando drush cim -y

  __  __        __     __        ___            _ __     __   __    ______
 / / / /__  ___/ /__ _/ /____   / _ |_  _____ _(_) /__ _/ /  / /__ / / / /
/ /_/ / _ \/ _  / _ `/ __/ -_) / __ | |/ / _ `/ / / _ `/ _ \/ / -_)_/_/_/ 
\____/ .__/\_,_/\_,_/\__/\__/ /_/ |_|___/\_,_/_/_/\_,_/_.__/_/\__(_|_|_)  
    /_/                                                                   

Updating helps us provide the best support and saves us tons of time

Use the link below to get the latest and greatest
https://github.com/lando/lando/releases/tag/v3.6.4

Lando is FREE and OPEN SOURCE software that relies on contributions from developers like you!
If you like Lando then help us spend more time making, updating and supporting it by contributing at the link below
https://github.com/sponsors/lando

If you would like to customize the behavior of this message then check out:
https://docs.lando.dev/config/releases.html

 [notice] There are no changes to import.
```


Ezt ki lehet kapcsolni így:

```
lando --channel none
```

Ha ezt kapod válasznak, akkor sikerült:

```
You will no longer receive update notifications.
  _      _____   ___  _  _______  _______
 | | /| / / _ | / _ \/ |/ /  _/ |/ / ___/
 | |/ |/ / __ |/ , _/    // //    / (_ / 
 |__/|__/_/ |_/_/|_/_/|_/___/_/|_/\___/  
                                         
If you do not continue to update manually this may limit our ability to support you!
```

Forrás:

https://github.com/lando/lando/issues/1000#issuecomment-1108267573

https://docs.lando.dev/core/v3/releases.html#:~:text=like%20on%20GitHub.-,You,-can%20also%20choose


#### Composer nem éri el a packagist.org oldalat IPv6-ról

Ezt kapod a composer require, composer update parancsokra:

```
curl error 28 while downloading https://repo.packagist.org/packages.json: Failed to connect to repo.packagist.org port 443: Connection timed out), package information was loaded from the local cache and may be out of date
```

Akkor jelenleg a DNS IPv6-os címet adott a packagist.org domainre neked, és azzal nem működik a composer. A https://github.com/composer/packagist/issues/950#issuecomment-424913225 szerint rá kell erőszakolni, hogy mindenképp IPv4-címről érje el a repot:

```
sudo nano /etc/hosts
```

Add hozzá ezt a sort:

```
142.44.164.255 repo.packagist.org
```

Majd Ctrl+X, Y.


### Drupal PHPUnit tesztek futtatása

A leírás ennek modernizálása alapján készült el: https://agile.coop/blog/drupal-phpunit-tests-lando/

Szerk.: https://www.drupal.org/project/drupalci_environments/issues/3208793#comment-14431946 2022.03.03-kor frissítették a drupalci/webdriver-chromedriver új verzióra, ami miatt új paraméterrel kell kiegészíteni a chromedriver commandját. Elvileg az itteni példának működnie kell az aktuálissal.


#### Beállítás

1. A `services:` részhez ezt add hozzá:

  ```
  appserver:
    overrides:
      environment:
        SIMPLETEST_BASE_URL: "http://drupal1.lndo.site"
        SIMPLETEST_DB: "mysql://drupal9:drupal9@database/drupal9"
        BROWSERTEST_OUTPUT_DIRECTORY: '/app/web/sites/simpletest/browser_output'
        MINK_DRIVER_ARGS_WEBDRIVER: '["chrome", {"browserName":"chrome","goog:chromeOptions":{"args":["--disable-gpu","--headless", "--no-sandbox", "--disable-dev-shm-usage"]}}, "http://chrome:9515"]'
  chrome:
    api: 3
    type: lando
    services:
      image: drupalci/webdriver-chromedriver:production
      command: chromedriver --log-path=/tmp/chromedriver.log --verbose --allowed-origins=* --whitelisted-ips=
  ```

  A nagy betűs változókban az URL-t, SQL-adatbázist és annak userét, valamint a mappa útvonalat ellenőrizd le, hogy jók-e! Az URL ha oldalnev.localhost domainnel van, akkor valamiért nem fogja tudni elérni a chromedriver, ezért a tesztekre használd a Landoba épített oldalnev.lndo.site domaint. Tehát ha a proxy alatt .localhostos URL-t adsz meg az appservernek, akkor biztosítsd, hogy a Lando default domainnel is menjen:

  ```
proxy:
  appserver:
    - drupal1.localhost
    - drupal1.lndo.site
  ```

Figyelem! Drupal 10.3 vagy régebbi esetén a `MINK_DRIVER_ARGS_WEBDRIVER` változóban a `goog:chromeOptions` legyen `chromeOptions` (https://www.drupal.org/node/3422624)!
  
2. A `tooling:` részhez ezt add hozzá:

  ```
  testdebug:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit --testdox -c /app/phpunit.xml"
  test:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit -c /app/phpunit.xml"
  phpunit:
    service: appserver
    cmd: "/app/vendor/bin/phpunit"
  ```

  Figyelem! Drupal 10 vagy régebbi esetén a testdebug-hoz tartozó cmd sor legyen ez: `cmd: "php /app/vendor/bin/phpunit -v -c /app/phpunit.xml"`

3. Fel kell telepíteni composerrel a tesztelési csomagokat, mert azok alapból nincsenek a drupal composer projektben:

  ```
lando composer require drupal/core-dev --dev --with-all-dependencies
  ```

4. Figyelem! Drupal 10 vagy régebbi esetén még kell ez is: `lando composer require --dev phpspec/prophecy-phpunit`

5. (ez csak akkor kell, ha contrib modulok függőségeivel akarsz tesztelni - lehet hogy behúz feleslegesen sok dev modult)

  ```
lando composer require --dev wikimedia/composer-merge-plugin
  ```

   composer.json-ba tedd az "extra" alá ezt: (ezzel biztosítjuk, hogyha egy modul a tesztekhez más modult igényel a másikkal való együttműködés tesztelésére, akkor az is legyen letöltve)

  ```
        "merge-plugin": {
            "include": [
                "web/modules/contrib/*/composer.json",
                "web/themes/contrib/*/composer.json"
            ]
        }
  ```
  Utána `lando composer update` (A `--lock` paraméterrel futtatva nem csinálna semmit)

6. Utána másold ki a `web/core/phpcs.xml.dist` fájlt a gyökérmappára a .lando.yml mellé!

  ```
  cp web/core/phpunit.xml.dist phpunit.xml
  ```

7. Ebben a fájlban bootstrap.php útvonalat az elején javítani kell erre:

  ```
<phpunit bootstrap="/app/web/core/tests/bootstrap.php" colors="true"
  ```
  Vagyis:

  ```
sed -i 's|tests\/bootstrap\.php|/app/web/core/tests/bootstrap.php|g' phpunit.xml
  ```

8. Hozd létre a `web/sites/simpletest/browser_output` mappát. A böngészőbeli `lando testdebug` paranccsal futtatott JS tesztek kimenetei ide lesznek mentve.

  ```
mkdir -p web/sites/simpletest/browser_output
  ```

9. Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

10. (Ez a lépés nem kell már Drupal 10-től, átugorhatod. Ha esetleg nem futnának le contrib modul tesztek, csak akkor vesződj ezzel) Ha egész modulok tesztjeit is akarod futtatni, akkor azokra ki kell javítani az útvonalakat a phpunit.xml-ben. Meg kell adnod, az XML-fájlhoz képest relatívan hol vannak tesztek. Ez az XML-felépítés Drupal verziónként más lehet, így a következő mintakód csak afféle útmutató, mintsem valódi kimásolandó kód:

```
  <testsuites>
    <testsuite name="unit">
      <file>web/core/tests/TestSuites/UnitTestSuite.php</file>
    </testsuite>
    <testsuite name="kernel">
      <file>web/core/tests/TestSuites/KernelTestSuite.php</file>
    </testsuite>
    <testsuite name="functional">
      <file>web/core/tests/TestSuites/FunctionalTestSuite.php</file>
    </testsuite>
    <testsuite name="functional-javascript">
      <file>web/core/tests/TestSuites/FunctionalJavascriptTestSuite.php</file>
    </testsuite>
    <testsuite name="build">
      <file>web/core/tests/TestSuites/BuildTestSuite.php</file>
    </testsuite>
  </testsuites>
  <listeners>
    <listener class="\Drupal\Tests\Listeners\DrupalListener">
    </listener>
  </listeners>
  <!-- Filter for coverage reports. -->
  <filter>
    <whitelist>
      <directory>web/includes</directory>
      <directory>web/lib</directory>
      <!-- Extensions can have their own test directories, so exclude those. -->
      <directory>web/modules</directory>
      <exclude>
        <directory>web/modules/*/src/Tests</directory>
        <directory>web/modules/*/tests</directory>
      </exclude>
      <directory>web/modules</directory>
      <exclude>
        <directory>web/modules/*/src/Tests</directory>
        <directory>web/modules/*/tests</directory>
        <directory>web/modules/*/*/src/Tests</directory>
        <directory>web/modules/*/*/tests</directory>
      </exclude>
      <directory>web/sites</directory>
     </whitelist>
  </filter>
```

#### Használat

Pl. a 4 fajta tesztre, amit a Drupal tud - ha mind zöld és OK, akkor működik minden. A `lando test` helyett `lando testdebug` paranccsal hiba esetén kiírja a konkrét hibát a teszt debugolás végett.

```
lando test web/core/modules/node/tests/src/Unit/NodeOperationAccessTest.php
lando test web/core/modules/help/tests/src/Kernel/HelpEmptyPageTest.php
lando test web/core/modules/block/tests/src/Functional/BlockHtmlTest.php
lando test web/core/modules/field/tests/src/FunctionalJavascript/Boolean/BooleanFormatterSettingsTest.php
```

Lekérheted, milyen modulokhoz van teszt:

```
lando test --list-groups
```

Így adod meg, mely modulok tesztjeit futtassa:

```
lando test --group commerce,commerce_log,commerce_order,commerce_promotion,commerce_shipping,commerce_store
```

Vagy úgy is futtathatsz modul tesztet, hogy a modul útvonalát adod meg:

```
lando test web/modules/contrib/commerce
```

Vagy modul konkrét teszt osztály teszt metódusa:

```
lando testdebug --filter testPublishInPastWhenItIsDisabled  web/modules/contrib/lightning_scheduler/tests/src/FunctionalJavascript/TransitionTest.php
```

#### Már feltelepített oldalhoz UI tesztek írása

[https://gitlab.com/weitzman/drupal-test-traits](https://git.drupalcode.org/project/dtt/) alapján.

11. 
```
composer require weitzman/drupal-test-traits --dev
```

12. `.lando.yml`-be még ezek kellenek:

  ```
  appserver:
    overrides:
      environment:
        # ... az alap teszteléshez szükséges ENV változók maradnak ugyanazok.
        # DTT testing.
        DTT_BASE_URL: "http://drupal1.lndo.site"
        DTT_MINK_DRIVER_ARGS: '["chrome", {"browserName":"chrome","goog:chromeOptions":{"args":["--disable-gpu","--headless", "--no-sandbox", "--disable-dev-shm-usage"]}}, "http://chrome:9515"]'
        DTT_API_OPTIONS: '{"socketTimeout": 360, "domWaitTimeout": 3600000}'
        SYMFONY_DEPRECATIONS_HELPER: 'disabled'
  ```

A `tooling:` alá még kerüljön be ez:

```
  testdtt:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit -v -c /app/phpunit_dtt.xml"

```

13. Utána másold ki a DTT-specifikus phpunit.xml fájlt a gyökérmappára a .lando.yml mellé! Vagy az is elég, hogyha a "existing-site" és "existing-site-javascript" testsuite definíciókat átmásolod a korábban szerkesztett phpunit.xml-be!

  ```
  cp vendor/weitzman/drupal-test-traits/docs/phpunit.xml phpunit_dtt.xml
  ```

  Ebben az egyszerűbb fejlesztés kedvéért cseréld le a `bootstrap="vendor/weitzman/drupal-test-traits/src/bootstrap-fast.php` sort `bootstrap="vendor/weitzman/drupal-test-traits/src/bootstrap.php` tehát ne a bootstrap-fast.php legyen az osztály autoloader, mert azzal csak a Test végződésű osztályok töltődnek be rendesen, és a parent class extend se működik benne megfelelően!
  
14. phpunit_dtt.xml minta fájl:

  ```
<?xml version="1.0" encoding="UTF-8"?>

<!-- Copy the samples below into your own phpunit.xml file.-->

<!-- Using this project's bootstrap file allows tests in `ExistingSite`,
    `ExistingSiteSelenium2DriverTest`, and `ExistingSiteWebDriverTest`
     to run alongside core's test types. -->

<!-- If you use the default `bootstrap-fast.php` and get 'class not 
     found' errors while running tests, head over to 
     https://gitlab.com/weitzman/drupal-test-traits/-/blob/master/src/bootstrap-fast.php
     for explanation on how to register those classes.
-->
<phpunit
  bootstrap="vendor/weitzman/drupal-test-traits/src/bootstrap.php"
  printerClass="\Drupal\Tests\Listeners\HtmlOutputPrinter"
>
    <php>
        <env name="DTT_BASE_URL" value="http://example.com"/>
        <env name="DTT_API_URL" value="http://localhost:9222"/>
        <!-- <env name="DTT_MINK_DRIVER_ARGS" value='["chrome", { "chromeOptions" : { "w3c": false } }, "http://localhost:4444/wd/hub"]'/> -->
        <env name="DTT_MINK_DRIVER_ARGS" value='["firefox", null, "http://localhost:4444/wd/hub"]'/>
        <env name="DTT_API_OPTIONS" value='{"socketTimeout": 360, "domWaitTimeout": 3600000}' />
        <!-- Example BROWSERTEST_OUTPUT_DIRECTORY value: /tmp
             Specify a temporary directory for storing debug images and html documents.
             These artifacts get copied to /sites/simpletest/browser_output by BrowserTestBase. -->
        <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="web/sites/simpletest/browser_output"/>
        <!-- To disable deprecation testing completely uncomment the next line. -->
        <!--<env name="SYMFONY_DEPRECATIONS_HELPER" value="disabled"/>-->
        <!-- Specify the default directory screenshots should be placed. -->
        <env name="DTT_SCREENSHOT_REPORT_DIRECTORY" value="web/sites/simpletest/browser_output"/>
        <!-- Specify the default directory page captures should be placed.
            When using the \Drupal\Tests\Listeners\HtmlOutputPrinter printerClass this will default to
            /sites/simpletest/browser_output. If using another printer such as teamcity this must be defined.
            -->
        <env name="DTT_HTML_OUTPUT_DIRECTORY" value="web/sites/simpletest/browser_output"/>
    </php>

    <testsuites>
        <testsuite name="unit">
            <directory>./web/modules/custom/*/tests/src/Unit</directory>
            <!--<directory>./web/profiles/custom/*/tests/src/Unit</directory>-->
        </testsuite>
        <testsuite name="kernel">
            <directory>./web/modules/custom/*/tests/src/Kernel</directory>
            <!--<directory>./web/profiles/custom/*/tests/src/Kernel</directory>-->
        </testsuite>
        <testsuite name="existing-site">
            <!-- Assumes tests are namespaced as \Drupal\Tests\custom_foo\ExistingSite. -->
            <directory>./web/modules/custom/*/tests/src/ExistingSite</directory>
            <!--<directory>./web/profiles/custom/*/tests/src/ExistingSite</directory>-->
        </testsuite>
        <testsuite name="existing-site-javascript">
            <!-- Assumes tests are namespaced as \Drupal\Tests\custom_foo\ExistingSiteJavascript. -->
            <directory>./web/modules/custom/*/tests/src/ExistingSiteJavascript</directory>
            <!--<directory>./web/profiles/custom/*/tests/src/ExistingSiteJavascript</directory>-->
        </testsuite>
    </testsuites>
</phpunit>

  ```

15. Ezután javasolt egy custom modult létrehozni, és abban a `drush gen test:existing` vagy `drush gen test:existing-js` segédszkripttel létrehozni a kiinduló teszt osztályokat abba a custom modulba. Ne felejtsd el, hogy itt is érvényes a class autoloading miatt, hogy minden teszt osztály a megfelelő útvonalon kell, hogy legyen és a fájlnév mindig `*Test.php` formájú legyen! Tehát pl. `AjaxTest2.php` rossz, `AjaxTest.php` a jó. A tesztek futtatása ugyanúgy történik, mint előbb, csak a `lando testdtd` segédparancsot használd!
    Segéd utility osztályokhoz is a Drupal Test Traits saját autoload.php-ja miatt azok is vagy a 
tests/src/ExistingSite vagy a tests/src/ExistingSiteJavascript alá menjenek (mehetnek ezalá "Utility", "Helper", stb. mappákba is). Ha egy class neve Test-re végződik, és nincs benne asserteket tartalmazó teszt metódus, akkor arra Warningot fog dobni a PhpUnit, ezért a segéd class-okanak találj ki valami más nevet!


#### Tesztek indítása phpStormból

1. Végezd el a PHP language level és CLI interpreter, Servers beállítását (Lásd: "phpStorm beállítása debugolásra")

2. File > Settings > PHP > Test Frameworks, jobb oldalt + gombbal adj hozzá újat "PHPUnit by Remote Interpreter", az Interpreter a létrehozott `Lando` legyen!

3. Use Composer autoloader legyen bejelölve

4. Path to script: `/app/vendor/autoload.php`

5. Test runner alatt a Default configuration file: `/app/phpunit_dtt.lando.xml`

6. Mentsd el OK-val

7. Egy teszt metódus neve mellett ha a zöld lejátszás ikonra kattintasz, akkor elindul phpStormban a teszt. Jobb klikkel az ikonon meg a teszt debugolását tudod elindítani. Természetesen debugolás előtt aktiválnod kell az xdebug extensiont, ami lassúsága miatt alapból le van tiltva a PHP-s image-ben: `lando xdebug debug`

Forrás: https://gist.github.com/quentint/6331aa9a75313ed955b2ea20d33557af


### PHPStan futtatása

Ha a Drupalt feltelepítetted már, akkor a vendor mappában már a PHPStan ott lesz. Lando-val így tudod azt használni:

A `tooling:` alá ez kerüljön:

```
  phpstan:
    service: appserver
    cmd: "vendor/bin/phpstan"

```

Használat pl. "content_redirect_to_front" contrib modulon: 

```
lando phpstan analyze /app/web/modules/contrib/content_redirect_to_front
```

Ha pedig pl. a modulnak van PHPStan ellenőrzési konfigurációja is:

```
lando phpstan analyze /app/web/modules/contrib/content_redirect_to_front -c /app/web/modules/contrib/content_redirect_to_front/phpstan.neon
```

### Google Cloud SDK Landoval

#### Beállítás

A `services:` alá ez kerüljön:

```
  cloud-sdk:
    api: 3
    type: lando
    app_mount: delegated
    services:
      image: google/cloud-sdk:389.0.0
      command: tail -f /dev/null
    volumes:
      cloud-sdk:

```

A `tooling:` alá ez kerüljön:

```
  gcloud:
    service: cloud-sdk
  gsutil:
    service: cloud-sdk

```

Majd újra kell buildelned a Lando projekteket: `lando rebuild -y`


#### Használat

Ugyanúgy kell mindent csinálni, mind simán a gcloud, gsutil konzol-alkalmazásokkal, csak elé kell írnod, hogy lando.

Először autentikálni kell magad: (https://stackoverflow.com/questions/71561730/authorizing-client-libraries-without-access-to-a-web-browser-gcloud-auth-appli)


```
lando gcloud init --console-only
```

Kilistázni, mely fiókokkal vagy autentikálva:

```
lando gcloud auth list
```

Ha itt már szerepelnek fiókok, akkor végezhetsz a jogosultságodnak megfelelő műveleteket.

Pl. CORS-beállítások lekérése egy GCS buckethez:

```
lando gsutil cors get gs://mybucket123
```

### Amazon Web Services CLI Landoval

#### Beállítás

A `services:` illesszük be ezt:

```
  aws:
    scanner: false
    api: 3
    type: lando
    app_mount: delegated
    services:
      user: root
      image: amazon/aws-cli:2.7.11
      command: tail -f /dev/null
      volumes:
        - aws:/root/.aws
      environment:
        LANDO_DROP_USER: root
    volumes:
      aws:

```

A `tooling:` illesszük be ezt:

```
  aws:
    service: aws
    user: root

```

Ne felejtsd újraépíteni a projektet: `lando rebuild -y`
Projekt újraépítéskor nem vesznek el az aws beállításai, mivel volume-ba van téve az a mappa.

#### Használat

Ugyanúgy kell mindent csinálni, mind simán az aws konzol-alkalmazással, csak elé kell írnod, hogy lando.

Először autentikálni kell magad:

```
lando aws configure
```

A létező konfigurációt ki is listázhatod:

```
lando aws configure list
```

Pl.: elérhető S3 bucketek kilistázása:

```
lando aws s3api list-buckets --query "Buckets[].Name"
```
