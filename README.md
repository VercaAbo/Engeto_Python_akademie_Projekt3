# Engeto_Python_akademie_Projekt3

Tento projekt je projektem Engeto Python akademie. Jde o program, který stahuje výsledky voleb do poslanecké sněmovny z roku 2017, z určitého okresu (výběr provede uživatel vložením odkazu na okres, který chce stáhnout). 

Data ve výsledném souboru obsahují informace o jednotlivých obcích okresu a dále sloupce odpovídající politickým stranám, které se voleb účastnily a jejich získaným počtům hlasů. 

K puštění projektu je potřeba nainstalovat knihovny ze souboru requirements.txt, který je přiložen v tomto Repositoriu. 


**Návod na spuštění projektu:**

1) Jak nainstalovat knihovny pomocí souboru Requirements.txt: 
Použijte následující příkaz:

```
pip install -r requirements.txt 
```

2) Jak spustit projekt:
Nachystejte si odkaz na výsledky voleb daného okresu - například https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 . Poté spusťte projekt se dvěma argumenty - prvním argumentem je uvedený odkaz, druhým název výsledného souboru. 
```
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_voleb.csv"
```

**Příklad výsledného csv souboru (otevřeného v Excelu):**

<img width="2741" height="617" alt="image" src="https://github.com/user-attachments/assets/4b58ca01-20b6-4f2f-9f29-71c15316adbc" />
