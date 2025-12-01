from bs4 import BeautifulSoup
import os

def extract_spielinfo(html_path):
    soup = BeautifulSoup(f, "html.parser")

    # 1. Quoten extrahieren
    quoten = []
    quoten_td = soup.find("td", class_="nw quoten")
    if quoten_td:
        for q in quoten_td.find_all("a", class_="quote"):
            label = q.find("span", class_="quote-label")
            value = q.find("span", class_="quote-text")
            if label and value:
                quoten.append({"Ergebnis": label.text.strip(), "Quote": value.text.strip()})

    # 2. Letzte Ergebnisse extrahieren
    def get_ergebnisse(table_class):
        ergebnisse = []
        table = soup.find("table", class_=table_class)
        if table:
            for row in table.find_all("tr"):
                tds = row.find_all("td")
                if len(tds) >= 4:
                    wettbewerb = tds[0].text.strip()
                    gegner = tds[1].text.strip()
                    team = tds[2].text.strip()
                    ergebnis = tds[3].text.strip()
                    ergebnisse.append({
                        "Wettbewerb": wettbewerb,
                        "Gegner": gegner,
                        "Team": team,
                        "Ergebnis": ergebnis
                    })
        return ergebnisse
    ergebnisse_heim = get_ergebnisse("spielinfoHeim")
    ergebnisse_gast = get_ergebnisse("spielinfoGast")

    # 3. Tabellenplatz und Torverhältnis extrahieren
    tabelle = []
    tabelle_table = soup.find("table", class_="sporttabelle drei_punkte_regel")
    if tabelle_table:
        for row in tabelle_table.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) >= 6:
                platz = tds[0].text.strip()
                verein = tds[1].text.strip()
                tore = tds[4].text.strip()
                diff = tds[5].text.strip()
                tabelle.append({
                    "Platz": platz,
                    "Verein": verein,
                    "Tore": tore,
                    "Diff": diff
                })

    return {
        "Quoten": quoten,
        "Letzte Ergebnisse Heim": ergebnisse_heim,
        "Letzte Ergebnisse Gast": ergebnisse_gast,
        "Tabelle": tabelle
    }

if __name__ == "__main__":
    html_path = os.path.join(os.path.dirname(__file__), "spielinfo.html")
    info = extract_spielinfo(html_path)
    print("Quoten:")
    for q in info["Quoten"]:
        print(q)
    print("\nLetzte Ergebnisse Heim:")
    for e in info["Letzte Ergebnisse Heim"]:
        print(e)
    print("\nLetzte Ergebnisse Gast:")
    for e in info["Letzte Ergebnisse Gast"]:
        print(e)
    print("\nTabellenplatz und Torverhältnis:")
    for t in info["Tabelle"]:
        print(t)

