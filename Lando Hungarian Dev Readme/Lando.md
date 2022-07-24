# Lando dev environment

Docker-alapú fejlesztői környezet Drupal oldalhoz egy paranccsal indítva. A memóriahasználat miatt javasolt egyszerre csak 1 vagy 2 site-ot futtatni.

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

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

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
    type: solr:8.11.0
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
    type: solr:8.11.0
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
$config['search_api.server.solr_content']['backend_config']['connector_config']['host'] = 'solr';
```

... ahol solr_content a machine ID-ja a beállított Search API Solr szervernek.

Lehetséges még, hogy a rendszeren ki kell nyitni a portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

### Varnish hozzáadása

A Varnish konfigurációs fájlt tegyük egy `.lando` mappában belül `default.vcl` névvel!


Vigyázat!
Ebben a vcl fájlban ha localhostra van irányítva a Varnish felől a forgalom a webszerverre, akkor azt módosítani kell erre:

```
# Default backend definition. Set this to point to your content server.
backend default {
    .host = "{{ getenv "VARNISH_BACKEND_HOST" }}";
    .port = "{{ getenv "VARNISH_BACKEND_PORT" "80" }}";
    .first_byte_timeout = 300s;
}
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
    type: varnish:6.0
    backends:
      - appserver
    ssl: true
    config:
      vcl: .lando/default.vcl
    overrides:
      environment:
        VARNISH_BACKEND_HOST: appserver
        VARNISH_BACKEND_PORT: 80
        VARNISH_ALLOW_UNRESTRICTED_PURGE: 1
        VARNISHD_PARAM_HTTP_RESP_HDR_LEN: 65536
        VARNISHD_PARAM_HTTP_RESP_SIZE: 98304
        VARNISHD_PARAM_WORKSPACE_BACKEND: 131072
        VARNISHD_VCL_SCRIPT: "/etc/varnish/lando.vcl"

```

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
$config['varnish_purger.settings.0805aa0bc1']['hostname'] = 'varnish.drupal1.localhost';
$config['varnish_purger.settings.0805aa0bc1']['port'] = 80;
```


Esetünkben ugyan nem kell mást csinálni, de ha a Varnish és az Apache is ugyanazon a szerveren van, akkor a settings.php-ben a `$settings['reverse_proxy']` és a `$settings['reverse_proxy_addresses']` beállításokkal meg kell adni, hol van a Varnish. Ezt itt azért nem kell, mert külön URL-eken van az Apache (http://drupal1.localhost) és a Varnish (http://varnish.drupal1.localhost) - lásd, amit a proxy kulcs alatt adtunk meg.

Ne felejtsük el, hogy a /admin/config/development/performance oldalon ne "no-cache" legyen a Cache-Control headerre beállítva. Ha nincs itt idő megadva, akkor a Varnish csak továbbítja a kéréseket az Apache felé, és nem fog semmit cache-elni.

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Lehetséges még, hogy a rendszeren ki kell nyitni a portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

#### Ismert hiba https://github.com/lando/varnish/issues/5: ha több appserver fut egyéb Lando projektekkel, akkor a Varnish konténerből nem biztos, hogy az aktuális projekt appserverére mutat valamiért. Ezért varnish-t használó projekt esetén:

```
lando poweroff
lando start
```

És ne indíts el más projektet egyszerre, hogy a Varnish jól működjön!

### Redis hozzáadása

A `services:` alá ez kerüljön:

```
  redis:
    type: redis:5.0.7
    persist: false
    portforward: false
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

Ebben a fájlban a sorvégződések LF-ek legyenek, ne pedig CRLF (Windows) vagy CR (Mac), különben a debugolás bekapcsolása `OCI runtime exec failed: exec failed: container_linux.go:380 : starting container process caused: no such file or directory: unknown` hibát fog dobni.

Engedélyezzük a szkript futtatását a `chmod +x .lando/xdebug.sh` paranccsal!

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

#### 2. Windows esetén

Windows alatt ha WSL2-ben futtatjuk a környezetet 2 féle módon lehet debugolni:
1. Windows alatt futtatjuk a phpStormot
   
   Így debugoláshoz elérhetővé kell tenni Windows számára a docker unix socketet, xdebugot át kell állítani a Windows-os IP-címre, valamint minden Windows újraindítás alkalmával a megváltozó Windows-os IP-cím miatt újra kell építeni MINDIG a projektet.

2. WSL2 alatt futtatjuk a phpStormot
   
   GWSL vagy VCXSRV XServert kell Windows-ra telepíteni, amivel a Linuxon futó phpStorm ablakát lehet megjeleníteni. Előfordulhat, hogy a gép alvó állapotból ébresztése után eltűnnek az így megnyitott ablakok, illetve a vágólappal is gond lehet néha, de cserébe mindent ugyanúgy kell a phpStormba állítani, mintha Linuxos gépen használnád, így nem kell újraépíteni a projektet minden nap.

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

1. telepítsük fel Windowsra a GWSL-t: https://opticos.github.io/gwsl/ és indítsuk el! Ha nem akarsz a Windows Store-ból telepíteni, akkor használhatod a vcxsrv programot is https://sourceforge.net/projects/vcxsrv/ Ezek teszik lehetővé, hogy a konzolról indíthass grafikus alkalmazásokat, amik így Linux alatt fognak futni.
2. telepítsük fel a phpstormot a WSL2-ben (NEM Windows alatt!): https://www.jetbrains.com/help/phpstorm/installation-guide.html#snap
3. WSL2 konzolból a `phpstorm` parancsot beírva tudjuk elindítani a programot.

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
   
     3) SSH helyett válasszuk ki a Docker radio buttont!
   
     4) Server: legyen az 1. pontban létrehozott Docker.
   
     5) Image name: pedig az "appserver" konténerhez használt image. Ez valami ilyesmi nevű lesz: "devwithlando/php:7.4-apache-4" ha az alapértelmezett van használva a `.lando.yml` fájlban. Ezért mindenképpen ellenőrizzük le a `.lando.yml` fájlban, hogy nem-e használ az oldal saját image-et, mert akkor azt kell itt megadni!
   
     6) Mentsük el OK-val mindent.

3. Debug port beállítása

   File > Settings ablakban Languages & Frameworks > PHP > Debug részben jobb oldalt az Xdebug szekcióban a Debug port: 9003 legyen!

4. Szerver fájl mapping beállítása

   File > Settings ablakban Languages & Frameworks > PHP > Servers részben jobb oldalt:

   - Nyomjuk meg a + gombot!

   - Name: virtual host neve, pl. drupal1.localhost

   - Host: ugyanaz

   - Port: 80

   - Debugger: Xdebug

   - Pipáljuk be a "Use path mappings" opciót!

   - A megjelenő 2 oszlopos táblázatban a projekt főmappájához (ahol a `.lando.yml` van) írjuk be jobb oldali oszlopba (Absolute path on server) azt, hogy `/app`

5. Kattintsunk a kék OK-ra a mentéshez!

#### 4. Használat

Ezentúl ahányszor indítjuk a projektet, az appserver konténeren belül bekapcsolható lesz az xdebug  `lando xdebug debug` parancsot futtatva. Ez bekapcsolja a böngészőhöz és a CLI-hez is a PHP szkriptek debugolását. Kikapcsolható az xdebug menet közben a `lando xdebug off` paranccsal. Nincs szükség a böngészőben az xdebug helper extensionre sem (mivel az xdebug.start_with_request lett beállítva a php.ini-ben).

phpStormban debugolás engedélyezéséhez: Run > Start listening for PHP debug connections menüpontra, vagy az eszköztáron erre a piros sarkú ikonra kattintsunk. Ugyanerre kattintva letilthatjuk a debugolást.

Lehetséges még, hogy a rendszeren ki kell nyitni a portot a tűzfalon. Lásd: "Portok megnyitása a konténerben futtatott szerverekre" fejezet.

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
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.0.6-0ubuntu2_amd64.deb
RUN dpkg -i libjpeg-turbo8_2.0.6-0ubuntu2_amd64.deb
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN apt --fix-broken install
```

A `tooling:` alá ez kerüljön: (ha kívülről parancssorból meg akarjuk hívni a wkhtmltopdf-et)

```
  wkhtmltopdf:
    service: appserver
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
    cmd: "/app/vendor/bin/phpcs --standard=Drupal"
    options:
    description: Run phpcs for given folder or file.
  phpcbf:
    service: appserver
    cmd: "/app/vendor/bin/phpcbf --standard=Drupal"
    options:
    description: Run phpcbf for given folder or file.
```

Ezután ne felejtsük újraépíteni a projektet: `lando rebuild -y`

Majd konzolból így lehet a codestyle ellenőrzést lefuttatni, pl. admin_toolbar modul esetén:

```
lando phpcs /app/web/modules/contrib/admin_toolbar
```

PHPStormban beállítható, hogy szerkesztés közben jelezze a codestyle hibákat, hogy ne kelljen mindig a konzolt futtatni újra és újra:
- PHP CLI Interpreter legyen a docker konténerben lévő PHP-re beállítva (valami hasonló ehhez a nevűhöz: devwithlando/php:7.4-apache-4, vigyázz a PHP-verziókra, hogy biztos jót válassz ki. Ha saját, Dockerfile-al buildelt szervert használ az oldal, akkor azt kell itt megadni)
- Languages & Frameworks > PHP > Quality Tools oldalon kattints a Configuration sornál a ... gombra:
  - bal oldalt a + gombbal add hozzá a ugyanazt a dockeres PHP CLI Interpretert, mint előbb.
  - PHP_CondeSniffer path: `/opt/project/vendor/bin/phpcs` (ne a Local, hanem a dockeres interpreterhez állítsd az útvonalat, ezt )
  - PHP Code Beautifier and Fixer Settings-et nyisd le, és ott Path to phpcbf: `/opt/project/vendor/bin/phpcbf`
- Editor > Inspections > PHP > Quality Tools > PHP_CodeSniffer legyen bepipálva, és jobb oldalt:
  - Show warning as: `Weak warning`
  - Check files with extensions: `php,js,css,inc,module,theme`
  - Coding standard: `Custom`, majd a mellette lévő ... gombra kattintva az ablakban:
  - Path to ruleset: `/opt/project/vendor/drupal/coder/coder_sniffer/Drupal/ruleset.xml`

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

Figyelem!
Ezt csak végső esetben használjuk!

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
        MINK_DRIVER_ARGS_WEBDRIVER: '["chrome", {"browserName":"chrome","chromeOptions":{"args":["--disable-gpu","--headless", "--no-sandbox", "--disable-dev-shm-usage"]}}, "http://chrome:9515"]'
  chrome:
    type: compose
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
  
2. A `tooling:` részhez ezt add hozzá:

  ```
  testdebug:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit -v -c /app/phpunit.xml"
  test:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit -c /app/phpunit.xml"
  phpunit:
    service: appserver
    cmd: "/app/vendor/bin/phpunit"
  ```

3. Fel kell telepíteni composerrel a tesztelési csomagokat, mert azok alapból nincsenek a drupal composer projektben:

  ```
lando composer require drupal/core-dev --dev --with-all-dependencies
lando composer require --dev phpspec/prophecy-phpunit
lando composer require --dev wikimedia/composer-merge-plugin
  ```

4. composer.json-ba tedd az "extra" alá ezt: (ezzel biztosítjuk, hogyha egy modul a tesztekhez más modult igényel a másikkal való együttműködés tesztelésére, akkor az is legyen letöltve)

  ```
        "merge-plugin": {
            "include": [
                "web/modules/contrib/*/composer.json",
                "web/themes/contrib/*/composer.json"
            ]
        }
  ```

5. Utána `composer update` (A `--lock` paraméterrel futtatva nem csinálna semmit)

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

10. Ha egész modulok tesztjeit is akarod futtatni, akkor azokra ki kell javítani az útvonalakat a phpunit.xml-ben. Meg kell adnod, az XML-fájlhoz képest relatívan hol vannak tesztek. Ez az XML-felépítés Drupal verziónként más lehet, így a következő mintakód csak afféle útmutató, mintsem valódi kimásolandó kód:

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
lando test web/core/modules/color/tests/src/Functional/ColorConfigSchemaTest.php
lando test web/core/modules/action/tests/src/FunctionalJavascript/ActionFormAjaxTest.php
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

### Google Cloud SDK Landoval

#### Beállítás

A `services:` alá ez kerüljön:

```
  cloud-sdk:
    type: compose
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
    type: compose
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
