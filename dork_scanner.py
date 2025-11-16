#!/usr/bin/env python3
"""
Google Dork Scanner - Herramienta de reconocimiento automatizado
Escanea dominios y subdominios usando Google Dorks
"""

import requests
import argparse
import time
import random
import json
import sys
from urllib.parse import quote_plus, urlparse
from datetime import datetime
from typing import List, Dict, Set
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    def __init__(self, domain: str, delay: int = 2, max_threads: int = 3):
        self.domain = domain
        self.delay = delay
        self.max_threads = max_threads
        self.subdomains = set()
        self.results = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def print_banner(self):
        banner = f"""
{Colors.OKCYAN}
╔═══════════════════════════════════════════════════════════╗
║           Google Dork Scanner v1.1                        ║
║           Automated Reconnaissance Tool                    ║
║           Mejorado - Sin dependencia de API keys          ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.WARNING}[!] Use this tool only on domains you own or have permission to test{Colors.ENDC}
{Colors.OKBLUE}[*] Target Domain: {self.domain}{Colors.ENDC}
{Colors.OKBLUE}[*] Fuentes de subdominios: crt.sh, HackerTarget, AlienVault, ThreatCrowd, Common{Colors.ENDC}
"""
        print(banner)

    def get_random_headers(self) -> Dict:
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def enumerate_subdomains_crtsh(self) -> Set[str]:
        """Enumera subdominios usando crt.sh (certificados SSL públicos)"""
        print(f"{Colors.OKBLUE}[*] Enumerando subdominios via crt.sh...{Colors.ENDC}", end=' ')
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    if name:
                        # Puede haber múltiples nombres separados por \n
                        for subdomain in name.split('\n'):
                            subdomain = subdomain.strip().lower()
                            # Limpiar wildcards
                            subdomain = subdomain.replace('*.', '')
                            if subdomain.endswith(self.domain) and subdomain:
                                subdomains.add(subdomain)
                print(f"{Colors.OKGREEN}✓ {len(subdomains)} encontrados{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠ No disponible (status {response.status_code}){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.WARNING}⚠ Error: {str(e)[:50]}{Colors.ENDC}")

        return subdomains

    def enumerate_subdomains_hackertarget(self) -> Set[str]:
        """Enumera subdominios usando HackerTarget API (gratuita, sin auth)"""
        print(f"{Colors.OKBLUE}[*] Enumerando subdominios via HackerTarget...{Colors.ENDC}", end=' ')
        subdomains = set()
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                lines = response.text.split('\n')
                # Verificar si hay error de rate limit
                if 'error' in response.text.lower() or 'quota' in response.text.lower():
                    print(f"{Colors.WARNING}⚠ API rate limit alcanzado{Colors.ENDC}")
                    return subdomains

                for line in lines:
                    if ',' in line:
                        subdomain = line.split(',')[0].strip().lower()
                        if subdomain and subdomain.endswith(self.domain):
                            subdomains.add(subdomain)
                print(f"{Colors.OKGREEN}✓ {len(subdomains)} encontrados{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠ No disponible (status {response.status_code}){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.WARNING}⚠ Error: {str(e)[:50]}{Colors.ENDC}")

        return subdomains

    def enumerate_subdomains_common(self) -> Set[str]:
        """Genera lista de subdominios usando prefijos comunes"""
        print(f"{Colors.OKBLUE}[*] Generando subdominios comunes...{Colors.ENDC}", end=' ')
        subdomains = set()

        # Prefijos comunes de subdominios (expandido)
        common_prefixes = [
            'www', 'mail', 'ftp', 'webmail', 'smtp', 'pop', 'pop3', 'imap',
            'webdisk', 'ns', 'ns1', 'ns2', 'ns3', 'ns4', 'dns', 'dns1', 'dns2',
            'email', 'mx', 'mx1', 'mx2',
            'news', 'test', 'dev', 'development', 'staging', 'stage', 'beta', 'alpha',
            'api', 'api-dev', 'api-staging', 'api-prod', 'api1', 'api2',
            'admin', 'administrator', 'portal', 'dashboard', 'panel',
            'vpn', 'remote', 'access', 'citrix',
            'blog', 'shop', 'store', 'ecommerce', 'cart',
            'secure', 'login', 'signin', 'signup', 'auth', 'authentication',
            'git', 'gitlab', 'github', 'bitbucket', 'svn',
            'jenkins', 'ci', 'cd', 'build',
            'jira', 'confluence', 'wiki', 'docs', 'documentation', 'help', 'support',
            'forum', 'community', 'chat',
            'cpanel', 'whm', 'plesk', 'directadmin',
            'cloud', 'aws', 'azure', 'gcp',
            'mobile', 'm', 'app', 'apps',
            'static', 'assets', 'cdn', 'media', 'images', 'img', 'upload', 'uploads',
            'ftp', 'sftp', 'files', 'download', 'downloads',
            'db', 'database', 'sql', 'mysql', 'postgres', 'mongo',
            'backup', 'backups', 'old', 'new',
            'legacy', 'v1', 'v2', 'v3', 'version1', 'version2',
            'demo', 'sandbox', 'lab', 'labs',
            'monitoring', 'monitor', 'grafana', 'prometheus', 'kibana',
            'status', 'health', 'metrics',
            'payments', 'pay', 'checkout', 'billing',
            'crm', 'erp', 'hr', 'finance',
            'intranet', 'internal', 'corp', 'corporate',
            'extranet', 'partner', 'partners', 'vendor', 'vendors'
        ]

        for prefix in common_prefixes:
            subdomain = f"{prefix}.{self.domain}"
            subdomains.add(subdomain)

        print(f"{Colors.OKGREEN}✓ {len(subdomains)} generados{Colors.ENDC}")
        return subdomains

    def enumerate_subdomains_alienvault(self) -> Set[str]:
        """Enumera subdominios usando AlienVault OTX (gratuito, sin auth)"""
        print(f"{Colors.OKBLUE}[*] Enumerando subdominios via AlienVault OTX...{Colors.ENDC}", end=' ')
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
                print(f"{Colors.OKGREEN}✓ {len(subdomains)} encontrados{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠ No disponible (status {response.status_code}){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.WARNING}⚠ Error: {str(e)[:50]}{Colors.ENDC}")

        return subdomains

    def enumerate_subdomains_threatcrowd(self) -> Set[str]:
        """Enumera subdominios usando ThreatCrowd (gratuito, sin auth)"""
        print(f"{Colors.OKBLUE}[*] Enumerando subdominios via ThreatCrowd...{Colors.ENDC}", end=' ')
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
                print(f"{Colors.OKGREEN}✓ {len(subdomains)} encontrados{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠ No disponible (status {response.status_code}){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.WARNING}⚠ Error: {str(e)[:50]}{Colors.ENDC}")

        return subdomains

    def enumerate_all_subdomains(self) -> Set[str]:
        """Enumera subdominios usando múltiples fuentes (todas gratuitas y sin API key)"""
        print(f"\n{Colors.HEADER}[*] Iniciando enumeración de subdominios...{Colors.ENDC}\n")

        all_subdomains = set()
        all_subdomains.add(self.domain)  # Agregar el dominio principal

        # Fuente 1: crt.sh (certificados SSL públicos)
        try:
            subs = self.enumerate_subdomains_crtsh()
            all_subdomains.update(subs)
            time.sleep(2)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error crítico en crt.sh: {str(e)}{Colors.ENDC}")

        # Fuente 2: HackerTarget (API gratuita sin auth, puede tener límites)
        try:
            subs = self.enumerate_subdomains_hackertarget()
            all_subdomains.update(subs)
            time.sleep(2)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error crítico en HackerTarget: {str(e)}{Colors.ENDC}")

        # Fuente 3: AlienVault OTX (gratuito, sin auth)
        try:
            subs = self.enumerate_subdomains_alienvault()
            all_subdomains.update(subs)
            time.sleep(2)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error crítico en AlienVault: {str(e)}{Colors.ENDC}")

        # Fuente 4: ThreatCrowd (gratuito, sin auth)
        try:
            subs = self.enumerate_subdomains_threatcrowd()
            all_subdomains.update(subs)
            time.sleep(2)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error crítico en ThreatCrowd: {str(e)}{Colors.ENDC}")

        # Fuente 5: Prefijos comunes (siempre disponible, no depende de APIs)
        try:
            subs = self.enumerate_subdomains_common()
            all_subdomains.update(subs)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error crítico en generación común: {str(e)}{Colors.ENDC}")

        # Limpiar subdominios inválidos
        valid_subdomains = set()
        for subdomain in all_subdomains:
            # Limpiar wildcards y caracteres extraños
            subdomain = subdomain.replace('*.', '').strip()
            # Validar que es un subdominio válido
            if subdomain and '.' in subdomain and subdomain.endswith(self.domain):
                valid_subdomains.add(subdomain)

        self.subdomains = valid_subdomains

        print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[+] Total subdominios únicos encontrados: {len(self.subdomains)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}\n")

        return valid_subdomains

    def get_google_dorks(self) -> List[Dict]:
        """Retorna lista completa de Google Dorks categorizados"""
        dorks = [
            # Archivos sensibles
            {"category": "Archivos Sensibles", "dork": 'site:{domain} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini'},
            {"category": "Archivos Sensibles", "dork": 'site:{domain} ext:sql | ext:dbf | ext:mdb'},
            {"category": "Archivos Sensibles", "dork": 'site:{domain} ext:log'},
            {"category": "Archivos Sensibles", "dork": 'site:{domain} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup'},
            {"category": "Archivos Sensibles", "dork": 'site:{domain} filetype:env "DB_PASSWORD"'},
            {"category": "Archivos Sensibles", "dork": 'site:{domain} filetype:env'},
            {"category": "Archivos Sensibles", "dork": 'site:{domain} ext:git | ext:svn'},

            # Credenciales
            {"category": "Credenciales", "dork": 'site:{domain} intext:"password" | intext:"passwd" | intext:"pwd"'},
            {"category": "Credenciales", "dork": 'site:{domain} intext:"username" | intext:"user" filetype:log'},
            {"category": "Credenciales", "dork": 'site:{domain} inurl:auth'},
            {"category": "Credenciales", "dork": 'site:{domain} "your password is"'},
            {"category": "Credenciales", "dork": 'site:{domain} filetype:xls | filetype:xlsx intext:password'},
            {"category": "Credenciales", "dork": 'site:{domain} "Index of /" +.htaccess'},
            {"category": "Credenciales", "dork": 'site:{domain} intext:"MySQL_ROOT_PASSWORD:"'},
            {"category": "Credenciales", "dork": 'site:{domain} intext:"API_KEY" | intext:"api key" | intext:"apikey"'},

            # Directorios expuestos
            {"category": "Directorios Expuestos", "dork": 'site:{domain} intitle:"index of"'},
            {"category": "Directorios Expuestos", "dork": 'site:{domain} intitle:"index of" "parent directory"'},
            {"category": "Directorios Expuestos", "dork": 'site:{domain} intitle:"index of" "backup"'},
            {"category": "Directorios Expuestos", "dork": 'site:{domain} intitle:"index of" "admin"'},
            {"category": "Directorios Expuestos", "dork": 'site:{domain} intitle:"index of" "upload"'},
            {"category": "Directorios Expuestos", "dork": 'site:{domain} intitle:"index of" "config"'},

            # Paneles de administración
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:admin'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:login'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:portal'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:dashboard'},
            {"category": "Paneles Admin", "dork": 'site:{domain} intitle:"Admin Panel"'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:wp-admin'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:administrator'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:cpanel'},
            {"category": "Paneles Admin", "dork": 'site:{domain} inurl:phpmyadmin'},

            # Información del servidor
            {"category": "Info Servidor", "dork": 'site:{domain} intitle:"Apache Status"'},
            {"category": "Info Servidor", "dork": 'site:{domain} intitle:"server status"'},
            {"category": "Info Servidor", "dork": 'site:{domain} inurl:server-status'},
            {"category": "Info Servidor", "dork": 'site:{domain} ext:php intitle:phpinfo "published by the PHP Group"'},
            {"category": "Info Servidor", "dork": 'site:{domain} intitle:"PHP Version"'},

            # Errores y debug
            {"category": "Errores", "dork": 'site:{domain} intext:"sql syntax near" | intext:"syntax error has occurred" | intext:"incorrect syntax near"'},
            {"category": "Errores", "dork": 'site:{domain} "Warning: mysql_connect()" | "Warning: mysql_query()" | "Warning: pg_connect()"'},
            {"category": "Errores", "dork": 'site:{domain} "fatal error" | "warning" filetype:php'},
            {"category": "Errores", "dork": 'site:{domain} intitle:"error occurred"'},

            # Documentos sensibles
            {"category": "Documentos", "dork": 'site:{domain} filetype:pdf "confidential"'},
            {"category": "Documentos", "dork": 'site:{domain} filetype:doc | filetype:docx'},
            {"category": "Documentos", "dork": 'site:{domain} filetype:xls | filetype:xlsx'},
            {"category": "Documentos", "dork": 'site:{domain} filetype:ppt | filetype:pptx'},
            {"category": "Documentos", "dork": 'site:{domain} filetype:pdf "internal use only"'},

            # CMS específicos
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:wp-content'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:joomla'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} inurl:drupal'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} "powered by Django"'},
            {"category": "CMS/Frameworks", "dork": 'site:{domain} "Laravel"'},

            # Información de email
            {"category": "Emails", "dork": 'site:{domain} intext:"@{domain}" filetype:txt'},
            {"category": "Emails", "dork": 'site:{domain} intext:"@{domain}" filetype:xls'},
            {"category": "Emails", "dork": 'site:{domain} intext:"email" | intext:"mail" filetype:csv'},

            # Subidas de archivos
            {"category": "Upload", "dork": 'site:{domain} inurl:upload'},
            {"category": "Upload", "dork": 'site:{domain} intitle:"Upload"'},

            # Git exposure
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:".git"'},
            {"category": "Git/SVN", "dork": 'site:{domain} intitle:"Index of /.git"'},
            {"category": "Git/SVN", "dork": 'site:{domain} inurl:".svn"'},

            # Cloud storage
            {"category": "Cloud Storage", "dork": 'site:{domain} "S3 Bucket"'},
            {"category": "Cloud Storage", "dork": 'site:{domain} inurl:s3.amazonaws.com'},

            # Webcams y dispositivos
            {"category": "Dispositivos", "dork": 'site:{domain} inurl:"/view/index.shtml"'},
            {"category": "Dispositivos", "dork": 'site:{domain} intitle:"webcamXP 5"'},

            # Instaladores
            {"category": "Instaladores", "dork": 'site:{domain} intitle:"installation" | intitle:"setup"'},
            {"category": "Instaladores", "dork": 'site:{domain} inurl:install.php'},

            # Traversal y LFI
            {"category": "Path Traversal", "dork": 'site:{domain} inurl:file= | inurl:path= | inurl:folder='},
            {"category": "Path Traversal", "dork": 'site:{domain} inurl:page= | inurl:include='},

            # Parámetros comunes
            {"category": "Parámetros", "dork": 'site:{domain} inurl:id='},
            {"category": "Parámetros", "dork": 'site:{domain} inurl:user='},
            {"category": "Parámetros", "dork": 'site:{domain} inurl:redirect='},

            # Shell backdoors
            {"category": "Shells", "dork": 'site:{domain} inurl:shell.php | inurl:cmd.php | inurl:backdoor.php'},
            {"category": "Shells", "dork": 'site:{domain} "c99shell" | "r57shell" | "WSO"'},

            # Jenkins/CI-CD
            {"category": "CI/CD", "dork": 'site:{domain} inurl:jenkins'},
            {"category": "CI/CD", "dork": 'site:{domain} inurl:gitlab'},
            {"category": "CI/CD", "dork": 'site:{domain} inurl:circleci'},

            # APIs
            {"category": "APIs", "dork": 'site:{domain} inurl:api | inurl:v1 | inurl:v2'},
            {"category": "APIs", "dork": 'site:{domain} inurl:graphql'},
            {"category": "APIs", "dork": 'site:{domain} inurl:swagger'},

            # Configuración de frameworks
            {"category": "Config Files", "dork": 'site:{domain} "config.json" | "app.json" | "package.json"'},
            {"category": "Config Files", "dork": 'site:{domain} ".env" | "config.php" | "settings.php"'},

            # Otros
            {"category": "Otros", "dork": 'site:{domain} intitle:"test page"'},
            {"category": "Otros", "dork": 'site:{domain} inurl:temp | inurl:tmp'},
            {"category": "Otros", "dork": 'site:{domain} "robots.txt" "Disallow:"'},
        ]

        return dorks

    def search_google_dork(self, dork: str, category: str, target: str) -> Dict:
        """Realiza búsqueda de un dork específico"""
        formatted_dork = dork.format(domain=target)
        search_url = f"https://www.google.com/search?q={quote_plus(formatted_dork)}"

        try:
            time.sleep(self.delay + random.uniform(0, 2))  # Anti-rate limiting
            headers = self.get_random_headers()

            response = requests.get(search_url, headers=headers, timeout=10)

            # Verificar si hay resultados
            has_results = False
            result_count = 0

            if response.status_code == 200:
                content = response.text.lower()

                # Múltiples indicadores de resultados
                if 'did not match any documents' not in content and \
                   'no results found' not in content and \
                   'did not find any matches' not in content:
                    # Buscar indicadores de resultados
                    if 'search' in content or 'result' in content:
                        has_results = True

                        # Intentar extraer número de resultados
                        match = re.search(r'about ([\d,]+) results', content)
                        if match:
                            result_count = match.group(1)

            return {
                'category': category,
                'dork': formatted_dork,
                'target': target,
                'url': search_url,
                'has_results': has_results,
                'result_count': result_count,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'category': category,
                'dork': formatted_dork,
                'target': target,
                'url': search_url,
                'has_results': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def scan_dorks(self):
        """Escanea todos los dorks contra todos los subdominios"""
        print(f"\n{Colors.HEADER}[*] Iniciando escaneo de Google Dorks...{Colors.ENDC}")

        dorks = self.get_google_dorks()
        total_combinations = len(dorks) * len(self.subdomains)

        print(f"{Colors.OKBLUE}[*] Total de dorks: {len(dorks)}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Total de subdominios: {len(self.subdomains)}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Total de combinaciones a probar: {total_combinations}{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] Esto puede tomar un tiempo considerable...{Colors.ENDC}\n")

        successful_results = []
        counter = 0

        for subdomain in self.subdomains:
            print(f"\n{Colors.OKCYAN}[*] Escaneando: {subdomain}{Colors.ENDC}")

            for dork_info in dorks:
                counter += 1
                category = dork_info['category']
                dork = dork_info['dork']

                progress = (counter / total_combinations) * 100
                print(f"  [{counter}/{total_combinations}] ({progress:.1f}%) {category}: ", end='', flush=True)

                result = self.search_google_dork(dork, category, subdomain)
                self.results.append(result)

                if result.get('has_results', False):
                    print(f"{Colors.OKGREEN}✓ ENCONTRADO{Colors.ENDC}")
                    successful_results.append(result)
                else:
                    print(f"{Colors.FAIL}✗{Colors.ENDC}")

        return successful_results

    def generate_report(self, successful_results: List[Dict]):
        """Genera reporte de resultados"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Reporte en consola
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}RESULTADOS DEL ESCANEO{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

        print(f"{Colors.OKGREEN}[+] Total dorks encontrados: {len(successful_results)}{Colors.ENDC}\n")

        if successful_results:
            # Agrupar por categoría
            by_category = {}
            for result in successful_results:
                cat = result['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(result)

            for category, results in by_category.items():
                print(f"\n{Colors.OKCYAN}[{category}] - {len(results)} resultados:{Colors.ENDC}")
                for r in results:
                    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {r['target']}")
                    print(f"    Dork: {r['dork']}")
                    print(f"    URL: {r['url']}\n")

        # Guardar JSON
        json_file = f"dork_scan_{self.domain}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'domain': self.domain,
                'scan_date': timestamp,
                'total_subdomains': len(self.subdomains),
                'subdomains': list(self.subdomains),
                'total_dorks_tested': len(self.results),
                'successful_dorks': len(successful_results),
                'results': successful_results,
                'all_results': self.results
            }, f, indent=2, ensure_ascii=False)

        print(f"{Colors.OKGREEN}[+] Reporte JSON guardado en: {json_file}{Colors.ENDC}")

        # Guardar reporte de texto
        txt_file = f"dork_scan_{self.domain}_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Google Dork Scanner - Reporte\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Dominio objetivo: {self.domain}\n")
            f.write(f"Fecha de escaneo: {timestamp}\n")
            f.write(f"Total subdominios: {len(self.subdomains)}\n")
            f.write(f"Total dorks probados: {len(self.results)}\n")
            f.write(f"Dorks exitosos: {len(successful_results)}\n\n")

            if successful_results:
                f.write(f"RESULTADOS POSITIVOS:\n")
                f.write(f"{'='*60}\n\n")

                by_category = {}
                for result in successful_results:
                    cat = result['category']
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(result)

                for category, results in by_category.items():
                    f.write(f"\n[{category}] - {len(results)} resultados:\n")
                    f.write(f"{'-'*60}\n")
                    for r in results:
                        f.write(f"Target: {r['target']}\n")
                        f.write(f"Dork: {r['dork']}\n")
                        f.write(f"URL: {r['url']}\n\n")

        print(f"{Colors.OKGREEN}[+] Reporte de texto guardado en: {txt_file}{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(
        description='Google Dork Scanner - Herramienta de reconocimiento automatizado',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 dork_scanner.py -d example.com
  python3 dork_scanner.py -d example.com --delay 5 --threads 2
  python3 dork_scanner.py --domain example.com --no-subdomain-enum

Advertencia:
  Use esta herramienta solo en dominios que posee o tiene permiso para probar.
  El uso indebido puede violar términos de servicio y leyes locales.
        """
    )

    parser.add_argument('-d', '--domain', required=True, help='Dominio objetivo (ej: example.com)')
    parser.add_argument('--delay', type=int, default=3, help='Delay entre peticiones en segundos (default: 3)')
    parser.add_argument('--threads', type=int, default=3, help='Número máximo de threads (default: 3)')
    parser.add_argument('--no-subdomain-enum', action='store_true', help='Omitir enumeración de subdominios')

    args = parser.parse_args()

    # Validar dominio
    domain = args.domain.lower().strip()
    if domain.startswith('http://') or domain.startswith('https://'):
        parsed = urlparse(domain)
        domain = parsed.netloc

    # Inicializar scanner
    scanner = GoogleDorkScanner(domain, delay=args.delay, max_threads=args.threads)
    scanner.print_banner()

    try:
        # Enumerar subdominios
        if not args.no_subdomain_enum:
            scanner.enumerate_all_subdomains()
        else:
            scanner.subdomains.add(domain)
            print(f"{Colors.WARNING}[!] Enumeración de subdominios omitida. Solo se escaneará el dominio principal.{Colors.ENDC}")

        # Mostrar subdominios encontrados
        if len(scanner.subdomains) > 1:
            print(f"\n{Colors.OKCYAN}Subdominios encontrados:{Colors.ENDC}")
            for sub in sorted(scanner.subdomains):
                print(f"  • {sub}")

        # Confirmar antes de continuar
        print(f"\n{Colors.WARNING}[!] Se van a probar {len(scanner.get_google_dorks())} dorks contra {len(scanner.subdomains)} subdominios.{Colors.ENDC}")
        response = input(f"{Colors.BOLD}¿Desea continuar? (s/n): {Colors.ENDC}").lower()

        if response != 's':
            print(f"{Colors.FAIL}[!] Escaneo cancelado por el usuario.{Colors.ENDC}")
            sys.exit(0)

        # Escanear dorks
        successful_results = scanner.scan_dorks()

        # Generar reporte
        scanner.generate_report(successful_results)

        print(f"\n{Colors.OKGREEN}[+] Escaneo completado exitosamente!{Colors.ENDC}")

    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] Escaneo interrumpido por el usuario.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}[!] Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
