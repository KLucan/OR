# Otvoreno Računarstvo: Laboratorijske vježbe

Repozitorij sadrži informacije o nekim izabranim video igrama.
Osim osnovnih informacija o igrama također sadrži imena i međusobne odnose među razvojnim studjima (developers) i izdavačima (publishers).
Podaci su dostupni kao `.sql`, `.json` i `.csv`

Autor: Karlo Lučan

Verzija: 1.0

Jezik: engleski

Licencija: MIT

Datum zadnje izmjene podataka: 2025-10-26

Ključne riječi: games, developers, publishers


## Shema podataka

### Games

- name: ime igre, do 60 znakova
- publisher: izdavač igre
- developer: razvojni studio koji je stvorio igru
- release_date: datum kada je igra izašla, ISO 8601 format YYYY-MM-DD
    - u slučaju više datuma (recimo igra je izašla najprije u Japanu pa zatim ostatku svijeta), uzima se onaj koji je prvi
- score: "Top Critic Average" ocjena sa stranice [OpenCritic](https://opencritic.com/)
- length: duljina igre u satima kao što je zapisano na stranici [HowLongToBeat](https://howlongtobeat.com/)
- has_multiplayer: ima li igra neki oblik multiplayera

### Companies

- name: ime firme, do 60 znakova
- country_code: dvoslovni kod države u kojoj je središte firme, ISO 3166 format
- parent: firma vlasnik

### Genres

- name: kratki unikatni indikator, do 20 znakova
- readable_name: čitljivije ime žanra
- parent: žanr čiji je podvrsta