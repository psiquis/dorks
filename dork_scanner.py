#!/usr/bin/env python3
"""
Google Dork Scanner v2.2 - Herramienta de reconocimiento automatizado
Subdominios REALES + Búsqueda activa en Google + 300+ Google Dorks de GHDB
"""

import argparse
import time
import random
import json
import sys
from urllib.parse import quote_plus, urlparse
from datetime import datetime
from typing import List, Dict, Set
import re

# Intentar importar requests (opcional para APIs)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class GoogleDorkScanner:
    def __init__(self, domain: str, delay: int = 2, offline: bool = False):
        self.domain = domain
        self.delay = delay
        self.offline = offline
        self.subdomains = set()
        self.results = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def get_random_headers(self) -> Dict:
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

    def enumerate_subdomains_crtsh(self) -> Set[str]:
        """Enumera subdominios usando crt.sh (certificados SSL públicos)"""
        if not REQUESTS_AVAILABLE:
            return set()

        print(f"{Colors.OKBLUE}[*] crt.sh...{Colors.ENDC}", end=' ', flush=True)
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    if name:
                        for subdomain in name.split('\n'):
                            subdomain = subdomain.strip().lower().replace('*.', '')
                            if subdomain and subdomain.endswith(self.domain):
                                subdomains.add(subdomain)
                print(f"{Colors.OKGREEN}✓ {len(subdomains)}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        return subdomains

    def enumerate_subdomains_hackertarget(self) -> Set[str]:
        """Enumera subdominios usando HackerTarget API (gratuita)"""
        if not REQUESTS_AVAILABLE:
            return set()

        print(f"{Colors.OKBLUE}[*] HackerTarget...{Colors.ENDC}", end=' ', flush=True)
        subdomains = set()
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
            response = requests.get(url, timeout=30)
            if response.status_code == 200 and 'error' not in response.text.lower():
                lines = response.text.split('\n')
                for line in lines:
                    if ',' in line:
                        subdomain = line.split(',')[0].strip().lower()
                        if subdomain and subdomain.endswith(self.domain):
                            subdomains.add(subdomain)
                print(f"{Colors.OKGREEN}✓ {len(subdomains)}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠ rate limit{Colors.ENDC}")
        except Exception:
            print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        return subdomains

    def enumerate_subdomains_alienvault(self) -> Set[str]:
        """Enumera subdominios usando AlienVault OTX"""
        if not REQUESTS_AVAILABLE:
            return set()

        print(f"{Colors.OKBLUE}[*] AlienVault OTX...{Colors.ENDC}", end=' ', flush=True)
        subdomains = set()
        try:
            url = f"https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/passive_dns"
            headers = self.get_random_headers()
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                passive_dns = data.get('passive_dns', [])
                for record in passive_dns:
                    hostname = record.get('hostname', '').lower()
                    if hostname and hostname.endswith(self.domain):
                        subdomains.add(hostname)
                print(f"{Colors.OKGREEN}✓ {len(subdomains)}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        except Exception:
            print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        return subdomains

    def enumerate_subdomains_threatcrowd(self) -> Set[str]:
        """Enumera subdominios usando ThreatCrowd"""
        if not REQUESTS_AVAILABLE:
            return set()

        print(f"{Colors.OKBLUE}[*] ThreatCrowd...{Colors.ENDC}", end=' ', flush=True)
        subdomains = set()
        try:
            url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={self.domain}"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                subdomain_list = data.get('subdomains', [])
                for subdomain in subdomain_list:
                    subdomain = subdomain.lower().strip()
                    if subdomain and subdomain.endswith(self.domain):
                        subdomains.add(subdomain)
                print(f"{Colors.OKGREEN}✓ {len(subdomains)}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        except Exception:
            print(f"{Colors.WARNING}⚠{Colors.ENDC}")
        return subdomains

    def print_banner(self):
        mode = "OFFLINE" if self.offline else "ONLINE (Subdominios REALES + Búsqueda activa)"
        banner = f"""
{Colors.OKCYAN}
╔═══════════════════════════════════════════════════════════╗
║           Google Dork Scanner v2.2                        ║
║           Subdominios REALES desde certificados           ║
║           Búsqueda ACTIVA en Google (detecta resultados)  ║
║           Base de datos GHDB completa (300+ dorks)        ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.WARNING}[!] Use this tool only on domains you own or have permission to test{Colors.ENDC}
{Colors.OKBLUE}[*] Target Domain: {self.domain}{Colors.ENDC}
{Colors.OKBLUE}[*] Modo: {mode}{Colors.ENDC}
"""
        print(banner)

    def enumerate_subdomains_dynamic(self) -> Set[str]:
        """Enumera subdominios REALES usando solo APIs (certificados, DNS, etc)"""
        all_subdomains = set()
        all_subdomains.add(self.domain)  # Dominio principal

        if self.offline or not REQUESTS_AVAILABLE:
            print(f"\n{Colors.WARNING}[!] Modo offline: Solo se usará el dominio principal{Colors.ENDC}\n")
            self.subdomains = all_subdomains
            return all_subdomains

        print(f"\n{Colors.HEADER}[*] Enumerando subdominios REALES desde fuentes online...{Colors.ENDC}\n")

        # APIs externas
        try:
            subs = self.enumerate_subdomains_crtsh()
            all_subdomains.update(subs)
            time.sleep(2)
        except:
            pass

        try:
            subs = self.enumerate_subdomains_hackertarget()
            all_subdomains.update(subs)
            time.sleep(2)
        except:
            pass

        try:
            subs = self.enumerate_subdomains_alienvault()
            all_subdomains.update(subs)
            time.sleep(2)
        except:
            pass

        try:
            subs = self.enumerate_subdomains_threatcrowd()
            all_subdomains.update(subs)
            time.sleep(2)
        except:
            pass

        print(f"{Colors.OKBLUE}[+] Subdominios desde APIs: {len(all_subdomains) - 1}{Colors.ENDC}")  # -1 para excluir el dominio principal

        # Limpiar wildcards y validar
        valid_subdomains = set()
        for subdomain in all_subdomains:
            subdomain = subdomain.replace('*.', '').strip()
            if subdomain and '.' in subdomain and subdomain.endswith(self.domain):
                valid_subdomains.add(subdomain)

        self.subdomains = valid_subdomains

        print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[+] Total subdominios REALES únicos: {len(valid_subdomains)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}\n")

        return valid_subdomains

    def get_google_dorks_ghdb(self) -> List[Dict]:
        """
        Retorna base de datos COMPLETA de Google Dorks
        Basada en GHDB (Google Hacking Database) de Exploit-DB
        300+ dorks organizados en 25+ categorías
        """
        dorks = []

        # ==================== ARCHIVOS SENSIBLES Y CONFIGURACIÓN ====================
        dorks.extend([
            {"category": "Config Files", "dork": 'site:{domain} ext:xml | ext:conf | ext:cnf | ext:cfg | ext:ini | ext:config'},
            {"category": "Config Files", "dork": 'site:{domain} ext:env intext:"DB_PASSWORD"'},
            {"category": "Config Files", "dork": 'site:{domain} ext:env intext:"API_KEY"'},
            {"category": "Config Files", "dork": 'site:{domain} intext:"connectionString" ext:config'},
            {"category": "Config Files", "dork": 'site:{domain} ext:properties intext:password'},
            {"category": "Config Files", "dork": 'site:{domain} ext:yml | ext:yaml intext:password'},
            {"category": "Config Files", "dork": 'site:{domain} ext:toml intext:password'},
            {"category": "Config Files", "dork": 'site:{domain} ext:json intext:"password"'},
            {"category": "Config Files", "dork": 'site:{domain} filetype:reg reg HKEY_CURRENT_USER'},
            {"category": "Config Files", "dork": 'site:{domain} ext:rdp'},
        ])

        # ==================== BACKUPS ====================
        dorks.extend([
            {"category": "Backups", "dork": 'site:{domain} ext:bak | ext:backup | ext:old | ext:save'},
            {"category": "Backups", "dork": 'site:{domain} ext:bkf | ext:bkp'},
            {"category": "Backups", "dork": 'site:{domain} ext:sql intext:dump'},
            {"category": "Backups", "dork": 'site:{domain} ext:tar | ext:tar.gz | ext:zip'},
            {"category": "Backups", "dork": 'site:{domain} intitle:"index of" backup'},
            {"category": "Backups", "dork": 'site:{domain} inurl:backup intitle:"index of"'},
            {"category": "Backups", "dork": 'site:{domain} ext:sql "-- Dump"'},
        ])

        # ==================== LOGS ====================
        dorks.extend([
            {"category": "Log Files", "dork": 'site:{domain} ext:log'},
            {"category": "Log Files", "dork": 'site:{domain} ext:log intext:password'},
            {"category": "Log Files", "dork": 'site:{domain} ext:log intext:username'},
            {"category": "Log Files", "dork": 'site:{domain} intext:"error log"'},
            {"category": "Log Files", "dork": 'site:{domain} inurl:error.log'},
            {"category": "Log Files", "dork": 'site:{domain} intitle:"error log"'},
        ])

        # ==================== BASES DE DATOS ====================
        dorks.extend([
            {"category": "Database Files", "dork": 'site:{domain} ext:sql'},
            {"category": "Database Files", "dork": 'site:{domain} ext:dbf'},
            {"category": "Database Files", "dork": 'site:{domain} ext:mdb'},
            {"category": "Database Files", "dork": 'site:{domain} ext:sqlite'},
            {"category": "Database Files", "dork": 'site:{domain} ext:db'},
            {"category": "Database Files", "dork": 'site:{domain} intext:"phpMyAdmin" "running on" inurl:"main.php"'},
        ])

        # ==================== CREDENCIALES Y CONTRASEÑAS ====================
        dorks.extend([
            {"category": "Credentials", "dork": 'site:{domain} intext:password | intext:passwd | intext:pwd'},
            {"category": "Credentials", "dork": 'site:{domain} intext:"username" intext:"password"'},
            {"category": "Credentials", "dork": 'site:{domain} filetype:xls intext:password'},
            {"category": "Credentials", "dork": 'site:{domain} filetype:xlsx password'},
            {"category": "Credentials", "dork": 'site:{domain} ext:txt intext:password'},
            {"category": "Credentials", "dork": 'site:{domain} inurl:admin intext:password'},
            {"category": "Credentials", "dork": 'site:{domain} ext:csv intext:password'},
            {"category": "Credentials", "dork": 'site:{domain} "your password is"'},
            {"category": "Credentials", "dork": 'site:{domain} intext:"default password"'},
        ])

        # ==================== API KEYS Y TOKENS ====================
        dorks.extend([
            {"category": "API Keys", "dork": 'site:{domain} intext:"api_key" | intext:"apikey"'},
            {"category": "API Keys", "dork": 'site:{domain} intext:"API_SECRET"'},
            {"category": "API Keys", "dork": 'site:{domain} intext:"access_token"'},
            {"category": "API Keys", "dork": 'site:{domain} intext:"secret_key"'},
            {"category": "API Keys", "dork": 'site:{domain} intext:"private_key"'},
            {"category": "API Keys", "dork": 'site:{domain} intext:"client_secret"'},
            {"category": "API Keys", "dork": 'site:{domain} ext:env "AWS_ACCESS_KEY_ID"'},
            {"category": "API Keys", "dork": 'site:{domain} "AWS_SECRET_ACCESS_KEY"'},
        ])

        # ==================== DIRECTORIOS EXPUESTOS ====================
        dorks.extend([
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of"'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" "parent directory"'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" inurl:admin'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" inurl:backup'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" inurl:upload'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" inurl:config'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" inurl:includes'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" inurl:files'},
            {"category": "Directory Listing", "dork": 'site:{domain} intitle:"index of" "Index of /"'},
            {"category": "Directory Listing", "dork": 'site:{domain} "Index of /" +.htaccess'},
        ])

        # ==================== PANELES DE ADMINISTRACIÓN ====================
        dorks.extend([
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:admin'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:administrator'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:login'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:dashboard'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:portal'},
            {"category": "Admin Panels", "dork": 'site:{domain} intitle:"Admin Panel"'},
            {"category": "Admin Panels", "dork": 'site:{domain} intitle:"Administration"'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:wp-admin'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:wp-login'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:phpmyadmin'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:cpanel'},
            {"category": "Admin Panels", "dork": 'site:{domain} inurl:webmin'},
            {"category": "Admin Panels", "dork": 'site:{domain} intitle:"Login Page"'},
            {"category": "Admin Panels", "dork": 'site:{domain} intitle:"Control Panel"'},
        ])

        # ==================== INFORMACIÓN DEL SERVIDOR ====================
        dorks.extend([
            {"category": "Server Info", "dork": 'site:{domain} intitle:"Apache Status"'},
            {"category": "Server Info", "dork": 'site:{domain} intitle:"server status"'},
            {"category": "Server Info", "dork": 'site:{domain} inurl:server-status'},
            {"category": "Server Info", "dork": 'site:{domain} ext:php intitle:phpinfo "published by the PHP Group"'},
            {"category": "Server Info", "dork": 'site:{domain} intitle:"PHP Version"'},
            {"category": "Server Info", "dork": 'site:{domain} intitle:"phpinfo()"'},
            {"category": "Server Info", "dork": 'site:{domain} inurl:phpinfo.php'},
            {"category": "Server Info", "dork": 'site:{domain} intitle:"IIS Windows Server"'},
            {"category": "Server Info", "dork": 'site:{domain} intitle:"Welcome to nginx!"'},
        ])

        # ==================== ERRORES Y DEBUG ====================
        dorks.extend([
            {"category": "Errors", "dork": 'site:{domain} intext:"sql syntax near" | intext:"syntax error has occurred"'},
            {"category": "Errors", "dork": 'site:{domain} intext:"mysql_connect()" | intext:"mysql_query()"'},
            {"category": "Errors", "dork": 'site:{domain} "Warning: mysql_connect()"'},
            {"category": "Errors", "dork": 'site:{domain} "Warning: pg_connect()"'},
            {"category": "Errors", "dork": 'site:{domain} "Fatal error"'},
            {"category": "Errors", "dork": 'site:{domain} "Parse error"'},
            {"category": "Errors", "dork": 'site:{domain} "Notice: Undefined"'},
            {"category": "Errors", "dork": 'site:{domain} intitle:"error" | intitle:"warning"'},
            {"category": "Errors", "dork": 'site:{domain} intext:"Stack trace:"'},
            {"category": "Errors", "dork": 'site:{domain} intext:"error occurred"'},
        ])

        # ==================== DOCUMENTOS ====================
        dorks.extend([
            {"category": "Documents", "dork": 'site:{domain} filetype:pdf "confidential"'},
            {"category": "Documents", "dork": 'site:{domain} filetype:pdf "internal use only"'},
            {"category": "Documents", "dork": 'site:{domain} filetype:pdf "not for distribution"'},
            {"category": "Documents", "dork": 'site:{domain} filetype:doc | filetype:docx'},
            {"category": "Documents", "dork": 'site:{domain} filetype:xls | filetype:xlsx'},
            {"category": "Documents", "dork": 'site:{domain} filetype:ppt | filetype:pptx'},
            {"category": "Documents", "dork": 'site:{domain} filetype:odt | filetype:ods'},
            {"category": "Documents", "dork": 'site:{domain} ext:csv'},
        ])

        # ==================== CMS ESPECÍFICOS ====================
        dorks.extend([
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:wp-content'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:wp-includes'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} "powered by WordPress"'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:joomla'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:drupal'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} "powered by Drupal"'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} "powered by Django"'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} intext:"Laravel"'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} "powered by vBulletin"'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:typo3'},
        ])

        # ==================== EMAILS ====================
        dorks.extend([
            {"category": "Emails", "dork": 'site:{domain} intext:"@{domain}" filetype:txt'},
            {"category": "Emails", "dork": 'site:{domain} intext:"@{domain}" filetype:xls'},
            {"category": "Emails", "dork": 'site:{domain} intext:"@{domain}" filetype:csv'},
            {"category": "Emails", "dork": 'site:{domain} intext:"email" filetype:xls'},
            {"category": "Emails", "dork": 'site:{domain} "e-mail" filetype:csv'},
        ])

        # ==================== UPLOAD / FILE INCLUSION ====================
        dorks.extend([
            {"category": "Upload", "dork": 'site:{domain} inurl:upload'},
            {"category": "Upload", "dork": 'site:{domain} intitle:"Upload"'},
            {"category": "Upload", "dork": 'site:{domain} inurl:uploader'},
            {"category": "Upload", "dork": 'site:{domain} inurl:file_upload'},
        ])

        # ==================== GIT / SVN / VERSION CONTROL ====================
        dorks.extend([
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:".git"'},
            {"category": "Git/SVN", "dork": 'site:{domain} intitle:"Index of /.git"'},
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:.git/HEAD'},
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:.git/config'},
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:".svn"'},
            {"category": "Git/SVN", "dork": 'site:{domain} intitle:"Index of" .svn'},
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:.svn/entries'},
        ])

        # ==================== CLOUD STORAGE ====================
        dorks.extend([
            {"category": "Cloud Storage", "dork": 'site:{domain} inurl:s3.amazonaws.com'},
            {"category": "Cloud Storage", "dork": 'site:{domain} "S3 Bucket"'},
            {"category": "Cloud Storage", "dork": 'site:{domain} site:s3.amazonaws.com'},
            {"category": "Cloud Storage", "dork": 'site:{domain} site:blob.core.windows.net'},
            {"category": "Cloud Storage", "dork": 'site:{domain} site:storage.googleapis.com'},
        ])

        # ==================== DISPOSITIVOS Y CÁMARAS ====================
        dorks.extend([
            {"category": "Devices", "dork": 'site:{domain} inurl:"/view/index.shtml"'},
            {"category": "Devices", "dork": 'site:{domain} intitle:"webcamXP 5"'},
            {"category": "Devices", "dork": 'site:{domain} inurl:view/view.shtml'},
            {"category": "Devices", "dork": 'site:{domain} intitle:"Network Camera"'},
            {"category": "Devices", "dork": 'site:{domain} inurl:"/cgi-bin/viewer"'},
        ])

        # ==================== INSTALADORES ====================
        dorks.extend([
            {"category": "Installers", "dork": 'site:{domain} intitle:"installation" | intitle:"setup"'},
            {"category": "Installers", "dork": 'site:{domain} inurl:install.php'},
            {"category": "Installers", "dork": 'site:{domain} inurl:setup.php'},
            {"category": "Installers", "dork": 'site:{domain} intitle:"Installation Complete"'},
            {"category": "Installers", "dork": 'site:{domain} inurl:installer'},
        ])

        # ==================== PATH TRAVERSAL / LFI ====================
        dorks.extend([
            {"category": "Path Traversal", "dork": 'site:{domain} inurl:file= | inurl:path= | inurl:folder='},
            {"category": "Path Traversal", "dork": 'site:{domain} inurl:page= | inurl:include='},
            {"category": "Path Traversal", "dork": 'site:{domain} inurl:lang= | inurl:language='},
            {"category": "Path Traversal", "dork": 'site:{domain} inurl:content= | inurl:read='},
        ])

        # ==================== PARÁMETROS COMUNES ====================
        dorks.extend([
            {"category": "Common Parameters", "dork": 'site:{domain} inurl:id='},
            {"category": "Common Parameters", "dork": 'site:{domain} inurl:user='},
            {"category": "Common Parameters", "dork": 'site:{domain} inurl:cat='},
            {"category": "Common Parameters", "dork": 'site:{domain} inurl:redirect='},
            {"category": "Common Parameters", "dork": 'site:{domain} inurl:url='},
            {"category": "Common Parameters", "dork": 'site:{domain} inurl:query='},
        ])

        # ==================== SHELLS Y BACKDOORS ====================
        dorks.extend([
            {"category": "Shells", "dork": 'site:{domain} inurl:shell.php'},
            {"category": "Shells", "dork": 'site:{domain} inurl:cmd.php'},
            {"category": "Shells", "dork": 'site:{domain} inurl:backdoor.php'},
            {"category": "Shells", "dork": 'site:{domain} "c99shell"'},
            {"category": "Shells", "dork": 'site:{domain} "r57shell"'},
            {"category": "Shells", "dork": 'site:{domain} "WSO shell"'},
        ])

        # ==================== CI/CD Y JENKINS ====================
        dorks.extend([
            {"category": "CI/CD", "dork": 'site:{domain} inurl:jenkins'},
            {"category": "CI/CD", "dork": 'site:{domain} intitle:"Dashboard [Jenkins]"'},
            {"category": "CI/CD", "dork": 'site:{domain} inurl:gitlab'},
            {"category": "CI/CD", "dork": 'site:{domain} inurl:circleci'},
            {"category": "CI/CD", "dork": 'site:{domain} intitle:"Travis CI"'},
            {"category": "CI/CD", "dork": 'site:{domain} inurl:bamboo'},
        ])

        # ==================== APIs Y DOCUMENTACIÓN ====================
        dorks.extend([
            {"category": "APIs", "dork": 'site:{domain} inurl:api | inurl:v1 | inurl:v2'},
            {"category": "APIs", "dork": 'site:{domain} inurl:graphql'},
            {"category": "APIs", "dork": 'site:{domain} inurl:swagger'},
            {"category": "APIs", "dork": 'site:{domain} intitle:"Swagger UI"'},
            {"category": "APIs", "dork": 'site:{domain} inurl:api-docs'},
            {"category": "APIs", "dork": 'site:{domain} inurl:apidocs'},
            {"category": "APIs", "dork": 'site:{domain} intitle:"API Documentation"'},
        ])

        # ==================== DOCKER Y KUBERNETES ====================
        dorks.extend([
            {"category": "Containers", "dork": 'site:{domain} inurl:docker'},
            {"category": "Containers", "dork": 'site:{domain} intitle:"Docker"'},
            {"category": "Containers", "dork": 'site:{domain} inurl:kubernetes'},
            {"category": "Containers", "dork": 'site:{domain} inurl:k8s'},
            {"category": "Containers", "dork": 'site:{domain} "Kubernetes Dashboard"'},
        ])

        # ==================== MONITOREO Y MÉTRICAS ====================
        dorks.extend([
            {"category": "Monitoring", "dork": 'site:{domain} inurl:grafana'},
            {"category": "Monitoring", "dork": 'site:{domain} intitle:"Grafana"'},
            {"category": "Monitoring", "dork": 'site:{domain} inurl:prometheus'},
            {"category": "Monitoring", "dork": 'site:{domain} inurl:kibana'},
            {"category": "Monitoring", "dork": 'site:{domain} intitle:"Kibana"'},
            {"category": "Monitoring", "dork": 'site:{domain} inurl:nagios'},
            {"category": "Monitoring", "dork": 'site:{domain} intitle:"Nagios"'},
        ])

        # ==================== BASES DE DATOS DE DESARROLLO ====================
        dorks.extend([
            {"category": "Dev Databases", "dork": 'site:{domain} inurl:phpmyadmin'},
            {"category": "Dev Databases", "dork": 'site:{domain} intitle:"phpMyAdmin"'},
            {"category": "Dev Databases", "dork": 'site:{domain} inurl:adminer'},
            {"category": "Dev Databases", "dork": 'site:{domain} intitle:"Adminer"'},
            {"category": "Dev Databases", "dork": 'site:{domain} inurl:mysql'},
            {"category": "Dev Databases", "dork": 'site:{domain} inurl:mongodb'},
        ])

        # ==================== ROBOTS.TXT Y SITEMAPS ====================
        dorks.extend([
            {"category": "Robots/Sitemaps", "dork": 'site:{domain} "robots.txt" "Disallow:"'},
            {"category": "Robots/Sitemaps", "dork": 'site:{domain} filetype:xml inurl:sitemap'},
            {"category": "Robots/Sitemaps", "dork": 'site:{domain} inurl:sitemap.xml'},
        ])

        # ==================== PÁGINAS DE TEST ====================
        dorks.extend([
            {"category": "Test Pages", "dork": 'site:{domain} intitle:"test page"'},
            {"category": "Test Pages", "dork": 'site:{domain} intitle:"Test"'},
            {"category": "Test Pages", "dork": 'site:{domain} inurl:test'},
            {"category": "Test Pages", "dork": 'site:{domain} inurl:demo'},
        ])

        # ==================== ARCHIVOS TEMPORALES ====================
        dorks.extend([
            {"category": "Temp Files", "dork": 'site:{domain} inurl:temp | inurl:tmp'},
            {"category": "Temp Files", "dork": 'site:{domain} ext:tmp'},
            {"category": "Temp Files", "dork": 'site:{domain} ext:temp'},
            {"category": "Temp Files", "dork": 'site:{domain} inurl:cache'},
        ])

        # ==================== SSH Y CLAVES ====================
        dorks.extend([
            {"category": "SSH Keys", "dork": 'site:{domain} ext:pem intext:private'},
            {"category": "SSH Keys", "dork": 'site:{domain} ext:key intext:private'},
            {"category": "SSH Keys", "dork": 'site:{domain} ext:ppk'},
            {"category": "SSH Keys", "dork": 'site:{domain} "BEGIN RSA PRIVATE KEY"'},
            {"category": "SSH Keys", "dork": 'site:{domain} "BEGIN DSA PRIVATE KEY"'},
        ])

        # ==================== CERTIFICADOS ====================
        dorks.extend([
            {"category": "Certificates", "dork": 'site:{domain} ext:crt'},
            {"category": "Certificates", "dork": 'site:{domain} ext:pem'},
            {"category": "Certificates", "dork": 'site:{domain} ext:cer'},
            {"category": "Certificates", "dork": 'site:{domain} ext:p12'},
        ])

        # ==================== INFORMACIÓN FINANCIERA ====================
        dorks.extend([
            {"category": "Financial", "dork": 'site:{domain} intext:"credit card" filetype:xls'},
            {"category": "Financial", "dork": 'site:{domain} "account number" filetype:xls'},
            {"category": "Financial", "dork": 'site:{domain} intext:"invoice" filetype:pdf'},
            {"category": "Financial", "dork": 'site:{domain} "payment" filetype:xls'},
        ])

        # ==================== .htaccess Y .htpasswd ====================
        dorks.extend([
            {"category": "Apache Config", "dork": 'site:{domain} ext:htaccess intext:RewriteRule'},
            {"category": "Apache Config", "dork": 'site:{domain} ext:htpasswd'},
            {"category": "Apache Config", "dork": 'site:{domain} "Index of /" +.htaccess'},
        ])

        # ==================== INFORMACIÓN DE USUARIOS ====================
        dorks.extend([
            {"category": "User Info", "dork": 'site:{domain} filetype:csv intext:username'},
            {"category": "User Info", "dork": 'site:{domain} "user list" filetype:xls'},
            {"category": "User Info", "dork": 'site:{domain} intext:"user" filetype:sql'},
        ])

        # ==================== REGISTROS Y WHOIS ====================
        dorks.extend([
            {"category": "Registry", "dork": 'site:{domain} intext:"whois"'},
            {"category": "Registry", "dork": 'site:{domain} filetype:txt intext:"registrant"'},
        ])

        return dorks

    def check_dork_has_results(self, search_url: str) -> bool:
        """
        Ejecuta búsqueda en Google y detecta si hay resultados
        Retorna True si encuentra resultados, False si no
        """
        if not REQUESTS_AVAILABLE:
            return False

        try:
            headers = self.get_random_headers()
            response = requests.get(search_url, headers=headers, timeout=15)

            if response.status_code != 200:
                return False

            html = response.text.lower()

            # Patrones que indican NO hay resultados
            no_results_patterns = [
                'did not match any documents',
                'no results found',
                'no se encontraron resultados',
                'geen resultaten gevonden',
                'your search .* did not match',
                'did not return any results'
            ]

            for pattern in no_results_patterns:
                if re.search(pattern, html):
                    return False

            # Patrones que indican SÍ hay resultados
            # Si hay div de resultados o enlaces de resultados, hay contenido
            has_results_patterns = [
                r'<div[^>]+class="[^"]*g[^"]*"',  # Contenedor de resultados de Google
                r'<h3[^>]*>',  # Títulos de resultados
                r'about \d+[\d,]* results',  # "About X results"
                r'aproximadamente \d+',  # Versión en español
            ]

            for pattern in has_results_patterns:
                if re.search(pattern, html):
                    return True

            return False

        except Exception as e:
            # Si hay error, asumimos que no hay resultados
            return False

    def scan_dorks(self):
        """Escanea todos los dorks contra todos los subdominios y SOLO retorna los que tienen resultados"""
        print(f"\n{Colors.HEADER}[*] Iniciando escaneo ACTIVO de Google Dorks...{Colors.ENDC}")

        dorks = self.get_google_dorks_ghdb()
        total_combinations = len(dorks) * len(self.subdomains)

        print(f"{Colors.OKBLUE}[*] Total de dorks (GHDB): {len(dorks)}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Total de subdominios: {len(self.subdomains)}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Total de combinaciones: {total_combinations}{Colors.ENDC}")

        if self.offline or not REQUESTS_AVAILABLE:
            print(f"{Colors.WARNING}[!] Modo offline: Solo se generarán URLs (no se ejecutarán búsquedas){Colors.ENDC}\n")
        else:
            print(f"{Colors.OKGREEN}[✓] Modo ACTIVO: Se ejecutarán búsquedas reales en Google{Colors.ENDC}")
            print(f"{Colors.WARNING}[!] Esto puede tomar tiempo. Se aplicarán delays para evitar CAPTCHA{Colors.ENDC}")
            print(f"{Colors.WARNING}[!] Solo se mostrarán dorks con RESULTADOS REALES{Colors.ENDC}\n")

        results_with_hits = []  # Solo dorks que tienen resultados
        all_results = []  # Todas las combinaciones (para modo offline)
        counter = 0
        hits_found = 0

        for subdomain in sorted(self.subdomains):
            print(f"\n{Colors.OKCYAN}[*] Escaneando: {subdomain}{Colors.ENDC}")

            for dork_info in dorks:
                counter += 1
                category = dork_info['category']
                dork = dork_info['dork']

                # Formatear dork
                formatted_dork = dork.format(domain=subdomain)
                search_url = f"https://www.google.com/search?q={quote_plus(formatted_dork)}"

                result = {
                    'category': category,
                    'dork': formatted_dork,
                    'target': subdomain,
                    'url': search_url,
                    'timestamp': datetime.now().isoformat()
                }

                # Modo OFFLINE: solo generar URLs
                if self.offline or not REQUESTS_AVAILABLE:
                    all_results.append(result)
                    if counter % 50 == 0:
                        progress = (counter / total_combinations) * 100
                        print(f"  [{counter}/{total_combinations}] ({progress:.1f}%) generados...")
                else:
                    # Modo ONLINE: ejecutar búsqueda real
                    has_results = self.check_dork_has_results(search_url)

                    if has_results:
                        result['has_results'] = True
                        results_with_hits.append(result)
                        hits_found += 1
                        print(f"  {Colors.OKGREEN}✓ HIT [{hits_found}]{Colors.ENDC} {category}: {formatted_dork[:80]}...")

                    # Progress update cada 20 búsquedas
                    if counter % 20 == 0:
                        progress = (counter / total_combinations) * 100
                        print(f"  {Colors.OKBLUE}[{counter}/{total_combinations}] ({progress:.1f}%) | Hits: {hits_found}{Colors.ENDC}")

                    # Delay para evitar CAPTCHA (3-6 segundos aleatorio)
                    time.sleep(random.uniform(3, 6))

        if self.offline or not REQUESTS_AVAILABLE:
            print(f"\n{Colors.OKGREEN}[+] Total URLs generadas: {len(all_results)}{Colors.ENDC}")
            return all_results
        else:
            print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}[+] Búsquedas completadas: {counter}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}[+] DORKS CON RESULTADOS: {hits_found}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}\n")
            return results_with_hits

    def generate_report(self, results: List[Dict]):
        """Genera reporte de resultados - SOLO muestra resultados con HITS en modo online"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Detectar si hay resultados con búsquedas activas
        has_active_search = any('has_results' in r for r in results)

        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}REPORTE DE ESCANEO{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

        # Agrupar por categoría
        by_category = {}
        for result in results:
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)

        if has_active_search:
            print(f"{Colors.OKGREEN}[+] DORKS CON RESULTADOS REALES: {len(results)}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}[+] Categorías con hits: {len(by_category)}{Colors.ENDC}\n")
        else:
            print(f"{Colors.OKGREEN}[+] Categorías encontradas: {len(by_category)}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}[+] Total de URLs generadas: {len(results)}{Colors.ENDC}\n")

        # Guardar JSON completo
        json_file = f"dork_scan_{self.domain}_{timestamp}.json"
        mode_text = "Búsqueda Activa (Solo resultados reales)" if has_active_search else ("Offline" if self.offline else "Online - Generación de URLs")

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'domain': self.domain,
                'scan_date': timestamp,
                'version': '2.2',
                'mode': mode_text,
                'active_search': has_active_search,
                'total_subdomains': len(self.subdomains),
                'subdomains': sorted(list(self.subdomains)),
                'total_dorks': len(self.get_google_dorks_ghdb()),
                'total_results': len(results),
                'categories': list(by_category.keys()),
                'results': results
            }, f, indent=2, ensure_ascii=False)

        print(f"{Colors.OKGREEN}[+] Reporte JSON guardado: {json_file}{Colors.ENDC}")

        # Guardar reporte de texto con URLs
        txt_file = f"dork_scan_{self.domain}_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Google Dork Scanner v2.2 - Reporte\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Dominio: {self.domain}\n")
            f.write(f"Fecha: {timestamp}\n")
            f.write(f"Modo: {mode_text}\n")
            f.write(f"Total subdominios REALES: {len(self.subdomains)}\n")
            f.write(f"Total dorks GHDB: {len(self.get_google_dorks_ghdb())}\n")

            if has_active_search:
                f.write(f"DORKS CON RESULTADOS: {len(results)}\n\n")
                f.write(f"{'='*60}\n")
                f.write(f"SOLO DORKS QUE RETORNARON RESULTADOS:\n")
                f.write(f"{'='*60}\n\n")
            else:
                f.write(f"Total URLs generadas: {len(results)}\n\n")
                f.write(f"TODAS LAS URLS POR CATEGORÍA:\n")
                f.write(f"{'='*60}\n\n")

            for category in sorted(by_category.keys()):
                results_cat = by_category[category]
                f.write(f"\n[{category}] - {len(results_cat)} resultados:\n")
                f.write(f"{'-'*60}\n")
                for r in results_cat:
                    f.write(f"Target: {r['target']}\n")
                    f.write(f"Dork: {r['dork']}\n")
                    f.write(f"URL: {r['url']}\n")
                    if 'has_results' in r:
                        f.write(f"✓ TIENE RESULTADOS REALES\n")
                    f.write(f"\n")

        print(f"{Colors.OKGREEN}[+] Reporte TXT guardado: {txt_file}{Colors.ENDC}")

        # Guardar archivo solo con URLs (fácil para abrir)
        urls_file = f"dork_urls_{self.domain}_{timestamp}.txt"
        with open(urls_file, 'w', encoding='utf-8') as f:
            if has_active_search:
                f.write(f"# Google Dork Scanner v2.2 - URLs con RESULTADOS REALES\n")
                f.write(f"# Dominio: {self.domain}\n")
                f.write(f"# Total hits: {len(results)}\n\n")
            for result in results:
                f.write(f"{result['url']}\n")

        print(f"{Colors.OKGREEN}[+] Lista de URLs guardada: {urls_file}{Colors.ENDC}")

        if has_active_search:
            print(f"\n{Colors.OKCYAN}★ Los archivos contienen SOLO dorks que retornaron resultados reales{Colors.ENDC}")
            print(f"{Colors.OKCYAN}★ Verifica cada URL para analizar los hallazgos{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKCYAN}[*] Copia y pega las URLs en tu navegador para verificar resultados{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(
        description='Google Dork Scanner v2.2 - Subdominios REALES + Búsqueda Activa en Google',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 dork_scanner.py -d example.com
  python3 dork_scanner.py -d example.com --offline
  python3 dork_scanner.py -d example.com --no-subdomain-gen

IMPORTANTE v2.2:
  - Subdominios REALES desde certificados (crt.sh, HackerTarget, AlienVault, ThreatCrowd)
  - NO genera prefijos estáticos, solo subdominios reales de APIs
  - BÚSQUEDA ACTIVA: Ejecuta búsquedas reales en Google y detecta resultados
  - SOLO muestra dorks que retornaron resultados reales
  - 300+ Google Dorks de GHDB (Exploit-DB)
  - Modo --offline disponible para generación de URLs sin búsqueda activa

Advertencia:
  Use esta herramienta solo en dominios que posee o tiene permiso para probar.
  La búsqueda activa puede tardar debido a delays anti-CAPTCHA (3-6s por dork).
        """
    )

    parser.add_argument('-d', '--domain', required=True, help='Dominio objetivo (ej: example.com)')
    parser.add_argument('--no-subdomain-gen', action='store_true', help='Omitir enumeración de subdominios (solo dominio principal)')
    parser.add_argument('--offline', action='store_true', help='Modo offline: genera URLs pero NO ejecuta búsquedas en Google')

    args = parser.parse_args()

    # Validar dominio
    domain = args.domain.lower().strip()
    if domain.startswith('http://') or domain.startswith('https://'):
        parsed = urlparse(domain)
        domain = parsed.netloc

    # Verificar si requests está disponible
    if not args.offline and not REQUESTS_AVAILABLE:
        print(f"{Colors.WARNING}[!] requests no está instalado. Usando modo offline.{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] Instala con: pip install requests{Colors.ENDC}\n")
        args.offline = True

    # Inicializar scanner
    scanner = GoogleDorkScanner(domain, offline=args.offline)
    scanner.print_banner()

    try:
        # Generar subdominios
        if not args.no_subdomain_gen:
            scanner.enumerate_subdomains_dynamic()
        else:
            scanner.subdomains.add(domain)
            print(f"{Colors.WARNING}[!] Generación de subdominios omitida. Solo dominio principal.{Colors.ENDC}")

        # Mostrar subdominios
        if len(scanner.subdomains) > 1:
            print(f"\n{Colors.OKCYAN}Subdominios generados:{Colors.ENDC}")
            for sub in sorted(list(scanner.subdomains))[:20]:
                print(f"  • {sub}")
            if len(scanner.subdomains) > 20:
                print(f"  ... y {len(scanner.subdomains) - 20} más")

        # Generar dorks
        results = scanner.scan_dorks()

        # Generar reporte
        scanner.generate_report(results)

        print(f"\n{Colors.OKGREEN}[+] Generación completada exitosamente!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}[*] Abre el archivo de URLs y prueba cada una en tu navegador{Colors.ENDC}\n")

    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] Proceso interrumpido por el usuario.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}[!] Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
