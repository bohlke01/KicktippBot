import os
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
if USERNAME is None or PASSWORD is None:
    from credentials import USERNAME, PASSWORD

def write_html_to_file(html_content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

def login(session):
    login_url = 'https://www.kicktipp.de/info/profil/login'
    post_url = 'https://www.kicktipp.de/info/profil/loginaction'

    response = session.get(login_url, timeout=10)
    response.raise_for_status()
    payload = {
        'kennung': USERNAME,
        'passwort': PASSWORD,
        'submitbutton': 'Anmelden'
    }
    login_response = session.post(post_url, data=payload, timeout=10)
    login_response.raise_for_status()
    write_html_to_file(login_response.text, "login.html")
    if 'Sie wurden erfolgreich eingeloggt.' not in login_response.text:
        raise Exception("Login failed")
    print("Login successful")


def logout(session):
    logout_url = 'https://www.kicktipp.de/info/profil/logout'
    logout_response = session.get(logout_url, timeout=10)
    logout_response.raise_for_status()
    if 'Die Abmeldung war erfolgreich.' not in logout_response.text:
        raise Exception("Logout failed")
    print("Logout successful")


def open_tipps_page(session, with_spielinfo=False):
    tipps_url = 'https://www.kicktipp.de/dummy5/tippabgabe'
    tipps_response = session.get(tipps_url, timeout=10)
    tipps_response.raise_for_status()
    write_html_to_file(tipps_response.text, "tipps.html")

    if not with_spielinfo:
        print("Skipping Spielinfo retrieval as per configuration.")
        # tippe_beste_quote(tipps_response.text)
    else:
        soup = BeautifulSoup(tipps_response.text, 'html.parser')
        spielinfo_link = soup.find('a', string=lambda t: t and 'Tippabgabe mit Spielinfos' in t)
        if not spielinfo_link or not spielinfo_link.has_attr('href'):
            raise Exception("'Spielinfo' link not found in the Tipp Übersicht page.")
        spielinfo_url = 'https://www.kicktipp.de' + spielinfo_link['href']
        spielinfo_response = session.get(spielinfo_url, timeout=10)
        spielinfo_response.raise_for_status()
        write_html_to_file(spielinfo_response.text, "spielinfo.html")


def extract_tipps_and_submit(session):
    tipps_url = 'https://www.kicktipp.de/dummy5/tippabgabe'
    response = session.get(tipps_url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", id="tippabgabeForm")

    table = form.find("table", id="tippabgabeSpiele")

    game_ids = []
    odds_list = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        game_id = tds[3].find("input")["id"].split("_")[1]
        odds = [float(value.text.strip()) for value in tds[4].find_all("span", class_="quote-text")]
        game_ids.append(game_id)
        odds_list.append(odds)

    outcomes = [[1,2] for _ in game_ids]  # Dummy outcomes, replace with your model's predictions

    payload = {}
    for inp in form.find_all("input", {"type": ["hidden"]}):
        if inp.has_attr("name") and inp.has_attr("value"):
            payload[inp["name"]] = inp["value"]
    for game_id, outcome in zip(game_ids, outcomes):
        payload[f"spieltippForms[{game_id}].tippAbgegeben"] = "true"
        payload[f"spieltippForms[{game_id}].heimTipp"] = str(outcome[0])
        payload[f"spieltippForms[{game_id}].gastTipp"] = str(outcome[1])

    # submit the form
    submit_url = form["action"] if form.has_attr("action") else tipps_url
    result = session.post("https://www.kicktipp.de" + submit_url if submit_url.startswith("/") else submit_url, data=payload, timeout=10)
    result.raise_for_status()
    print("Tipps submitted with status code:", result.status_code)


def main():
    with requests.Session() as session:
        try:
            login(session)
            # open_tipps_page(session, with_spielinfo=False)
            extract_tipps_and_submit(session)
        finally:
            logout(session)

if __name__ == "__main__":
    main()

