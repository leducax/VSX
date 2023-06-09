import requests
import re
from bs4 import BeautifulSoup
from tkinter import *
import threading

def scan_url(url):
    try:
        print("\033[91mScanning URL for vulnerabilities...\033[0m")
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.findAll('a', {'href': re.compile('^http')}):
            href = link.get('href')
            thread = threading.Thread(target=check_vulnerability, args=(href,))
            thread.start()
    except:
        print("\033[91mURL not found. Please enter a valid URL\033[0m")
def check_vulnerability(url):
    page_source = requests.get(url)
    page_text = page_source.text
    check_vuln = re.findall('[Vv]ulnerability|[Xx]ss|[Hh]ack', page_text)
    if check_vuln:
        print(f"\033[91mVulnerability found at {url}\033[0m")
        exploit_vuln(url)
def exploit_vuln(url):
    try:
        print("\033[92mExploiting vulnerability to gain admin access...\033[0m")
        admin_page = requests.get(url + "/admin")
        admin_text = admin_page.text
        admin_soup = BeautifulSoup(admin_text, 'html.parser')
        admin_form = admin_soup.find('form')
        admin_inputs = admin_form.find_all('input')
        fields = {}
        for input in admin_inputs:
            input_name = input.get('name')
            input_value = input.get('value')
            if input_name and input_value:
                fields[input_name] = input_value
        admin_data = requests.post(url + "/admin", data=fields)
        if admin_data.status_code == 200:
            print("\033[92mSuccess! Admin access granted.\033[0m")
            get_db_info(url)
        else:
            print("\033[91mFailed to gain admin access.\033[0m")
    except:
        print("\033[91mExploit failed.\033[0m")
def get_db_info(url):
    try:
        print("\033[93mRetrieving database information...\033[0m")
        db_page = requests.get(url + "/db")
        db_text = db_page.text
        db_soup = BeautifulSoup(db_text, 'html.parser')
        db_tables = db_soup.find_all('table')
        db_rows = []
        for table in db_tables:
            rows = table.find_all('tr')
            for row in rows:
                db_rows.append(row.text)
        print("\033[93mDatabase information retrieved.\033[0m")
        show_gui(db_rows)
    except:
        print("\033[91mDatabase info could not be retrieved.\033[0m")
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
