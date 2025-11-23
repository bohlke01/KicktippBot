import requests
from bs4 import BeautifulSoup

# URL der Login-Seite
login_url = 'https://www.kicktipp.de/info/profil/login'

# Erstelle eine Session
session = requests.Session()

# Hole die Login-Seite, um die CSRF-Token zu erhalten
response = session.get(login_url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

# Finde die CSRF-Token (falls vorhanden)
# csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

# Deine Login-Daten
payload = {
    'username': 'kicktipprobot@gmail.com',
    'password': '',
    # 'csrf_token': csrf_token
}

# Sende die Login-Daten
login_response = session.post(login_url, data=payload, verify=False)

# Überprüfe, ob der Login erfolgreich war
if login_response.url == 'https://www.kicktipp.de/info/profil/':
    print('Login erfolgreich')
else:
    print('Login fehlgeschlagen')