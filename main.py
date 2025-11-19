import requests
from bs4 import BeautifulSoup
import csv
import sys

zakladniUrl = "https://www.volby.cz/pls/ps2017nss/"

# Pouzij argument skriptu
url = sys.argv[1]
if not url:
    print("Nezadali jste odkaz na volby")
    quit()
csv_soubor = sys.argv[2]
if not csv_soubor:
    print("Nezadali jste nazev souboru")
    quit()


def ziskejObce(soup):
    """
    Najde obce v základní tabulce a dohledá číslo obce, název obce a odkaz
    k dohledání dalších detailů
    """
    rows = soup.findAll("tr")
    obce = []
    for row in rows:
        bunky = row.findAll("td")
        if len(bunky):
            odkaz = bunky[0].find('a')
            if odkaz: 
                obce.append({
                    "cislo": bunky[0].get_text(),
                    "nazev": bunky[1].get_text(),
                    "odkaz": zakladniUrl + "/" + odkaz.get("href")
                })
    return obce


def ulozDoSouboru(jmeno, hlavicka, data):
    """
    Uloží data do csv souboru.
    hlavičku souboru tvoří klíče slovníku se zpracovanými daty.
    """
    with open(jmeno, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=hlavicka)
        writer.writeheader()  # Write header row
        writer.writerows(data)  # Write data rows


def stahniDetailyJedneObce(cislo, nazev, urlDetail):
    """
    Stáhne všechny detaily ze stránky s výsledky voleb v obcích.
    Vrátí všechny získane informace včetně čísla a názvu obce.
    """
    detailStranka = requests.get(urlDetail)
    soupDetail = BeautifulSoup(detailStranka.text, "html.parser")
    prvniTabulka = soupDetail.find("table", {"id": "ps311_t1"})
    sloupce = prvniTabulka.find_all("td")
    tabulky = soupDetail.find_all("table", {"class": "table"})
    radkytabulek = tabulky[1].find_all("tr")[2:]
    radkytabulek.extend(
        tabulky[2].find_all("tr")[2:]
    )

    radeksouboru = {
        "kód obce": cislo,
        "název obce": nazev,
        "voliči v seznamu": sloupce[3].get_text().replace("\xa0", ""), 
        "vydané obálky": sloupce[4].get_text(), 
        "platné hlasy": sloupce[7].get_text() 
    }

    for tr in radkytabulek:
        td_na_radku = tr.find_all("td")
        if td_na_radku[1].text != '-':
            sloupec = td_na_radku[1].text
            hodnota = td_na_radku[2].text
            radeksouboru[sloupec] = hodnota

    return radeksouboru


def stahniDetailyVsechObci(obce): 
    """
    Postupně projde každou obci v okresu a stáhne výsledky.
    Výsledné pole výsledku pak vrátí.
    """
    data = []
    for obec in obce: 
        cisloObce = obec["cislo"]
        nazevObce = obec["nazev"]
        odkaz = obec["odkaz"]
        vysledek = stahniDetailyJedneObce(cisloObce, nazevObce, odkaz) 
        data.append(vysledek)
        print(vysledek["název obce"])
    return data


# stahneme stranku
odp_serveru = requests.get(url)
soup = BeautifulSoup(odp_serveru.text, "html.parser")

# ziskame seznam obci
obceSeznam = ziskejObce(soup)

# ziskame seznam detailu obci
detailyObci = stahniDetailyVsechObci(obceSeznam)

# ulozime vysledek do souboru
sloupce = list(detailyObci[0].keys())
ulozDoSouboru(csv_soubor, sloupce, detailyObci)
