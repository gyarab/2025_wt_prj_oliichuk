# automatizovany tracker statistik pro ranked hry v valorant

### co dělá
Aplikace se automaticky připojuje k Riot API a po každé ranked hře stahuje herní statistiky. Ukládá specifikovane údaje (kills, deaths, assists, rank changes, atd.) do databáze a pouziva frontend pro lehci access k datam.

### technologie

- Django framework
- Riot Games API
- SQLite/PostgreSQL databáze

### odborny clanek 
Automatizovaný _tracker_ _statistik_ pro _ranked_ hry ve Valorantu je specializovaná webová _aplikace_, která umožňuje dlouhodobě sledovat výkonnost hráče a vývoj jeho _ranku_ na základě reálných dat po každém odehraném _matchi_. Základním cílem řešení je automatizovat sběr a interpretaci herních metrik tak, aby uživatel nemusel manuálně zapisovat výsledky a měl okamžitý přehled o svém progresu i slabých stránkách.

Systém se pravidelně připojuje k _Riot Games API_ (autorizovaný přístup přes _API token_) a po dokončení každé _ranked_ hry stahuje relevantní _match data_. Následně provádí _parsování_ odpovědi, validaci a ukládání vybraných údajů do _databáze_ (např. _kills_, _deaths_, _assists_, změna _MMR_ / _rank rating_, _agent_, _mapa_, _K/D ratio_, _ACS_ a časové _timestampy_). Backend postavený na _Django frameworku_ řeší _datový model_, _ORM_, _REST API_ pro frontend, správu _uživatelských účtů_ a bezpečnost (např. _rate limiting_ a ošetření chybových stavů typu _HTTP 429_). Volitelně lze použít _SQLite_ pro lokální vývoj a _PostgreSQL_ pro produkční nasazení kvůli lepší práci s indexy, agregacemi a škálováním.

V aplikaci běžně rozlišujeme tři role. _Anonymní návštěvník_ může prohlížet veřejné dashboardy a základní agregované _statistiky_ (např. průměrné _K/D_ nebo trend _ranku_), ale nemá přístup k personalizovaným funkcím. _Registrovaný uživatel_ si propojí svůj _účet_ s hráčským identifikátorem, spravuje vlastní profil, získává historii _zápasů_, může přidávat _komentáře_ a udělovat _hodnocení_ (např. kvalita zápasu, subjektivní forma). _Administrátor_ spravuje _uživatele_, moderuje _komentáře_, nastavuje limity volání _API_, kontroluje integritu _databáze_ a řeší incidenty (např. výpadky synchronizace). Tímto vzniká robustní nástroj pro analýzu výkonu ve Valorantu opřený o data, automatizaci a standardní webovou architekturu.

### diagram user flow + navrh wireframes 
![IMG_20260306_093542](https://github.com/user-attachments/assets/268760c5-786a-4883-ab14-e8e3254f3550)
