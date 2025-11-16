# Google Dork Scanner v2.0 🔍

**Herramienta 100% OFFLINE de reconocimiento automatizado usando Google Dorks de GHDB (Exploit-DB)**

## 🎯 ¿Qué hay de nuevo en v2.0?

### ✅ 100% OFFLINE - SIN APIs Externas
- **Eliminadas TODAS las dependencias de APIs externas**
- No requiere crt.sh, HackerTarget, AlienVault, ni ThreatCrowd
- No requiere conexión a internet para generar subdominios y dorks
- **Cero dependencias de Python** - Solo librería estándar

### 🚀 Base de Datos Masiva de Google Dorks
- **300+ Google Dorks** basados en GHDB (Google Hacking Database de Exploit-DB)
- **25+ categorías** de dorks organizados
- Cobertura completa de vectores de reconocimiento

### 📡 Generación de Subdominios Mejorada
- **200+ prefijos comunes** de subdominios
- Basado en patrones reales de pentesting
- Generación local sin APIs

## ⚠️ Advertencia Legal

**IMPORTANTE:** Esta herramienta debe utilizarse únicamente en:
- Dominios de tu propiedad
- Sistemas para los cuales tienes autorización explícita para realizar pruebas de seguridad
- Entornos de prueba/laboratorio
- Programas de Bug Bounty donde el dominio esté en scope

El uso no autorizado puede violar:
- Términos de servicio de Google
- Leyes de privacidad y protección de datos
- Leyes de ciberseguridad locales e internacionales

El autor no se hace responsable del uso indebido de esta herramienta.

## 🚀 Características

### 🎯 Generación de Subdominios (100% Offline)
- **200+ prefijos comunes** expandidos de subdominios
- Incluye: infraestructura web, email, FTP, DNS, desarrollo, APIs, admin, bases de datos, monitoreo, DevOps, cloud, contenido, e-commerce, documentación, mobile, backups, CRM, networking y más
- **Sin dependencia de APIs externas**
- Generación instantánea local

### 🔍 Base de Datos de Google Dorks (GHDB - Exploit-DB)

**300+ dorks en 25+ categorías:**

1. **Config Files** - Archivos de configuración sensibles
2. **Backups** - Archivos de respaldo expuestos
3. **Log Files** - Archivos de logs con información sensible
4. **Database Files** - Archivos de bases de datos
5. **Credentials** - Contraseñas y credenciales
6. **API Keys** - Keys y tokens de APIs
7. **Directory Listing** - Listados de directorios
8. **Admin Panels** - Paneles de administración
9. **Server Info** - Información del servidor
10. **Errors** - Mensajes de error y debug
11. **Documents** - Documentos sensibles (PDF, Office)
12. **CMS/Frameworks** - WordPress, Drupal, Django, Laravel
13. **Emails** - Direcciones de correo expuestas
14. **Upload** - Formularios de carga de archivos
15. **Git/SVN** - Repositorios de código expuestos
16. **Cloud Storage** - S3, Azure Blob, Google Cloud Storage
17. **Devices** - Cámaras y dispositivos IoT
18. **Installers** - Scripts de instalación
19. **Path Traversal** - Vulnerabilidades de path traversal
20. **Common Parameters** - Parámetros comunes vulnerables
21. **Shells** - Web shells y backdoors
22. **CI/CD** - Jenkins, GitLab, CircleCI
23. **APIs** - Documentación y endpoints de APIs
24. **Containers** - Docker y Kubernetes
25. **Monitoring** - Grafana, Prometheus, Kibana
26. **Dev Databases** - phpMyAdmin, Adminer
27. **Robots/Sitemaps** - robots.txt y sitemaps
28. **Test Pages** - Páginas de prueba
29. **Temp Files** - Archivos temporales
30. **SSH Keys** - Claves SSH expuestas
31. **Certificates** - Certificados
32. **Financial** - Información financiera
33. **Apache Config** - .htaccess y .htpasswd
34. **User Info** - Información de usuarios
35. **Registry** - Información de registro

### 📊 Reportes Generados

El programa genera **3 archivos** de salida:

1. **JSON** (`dork_scan_<dominio>_<timestamp>.json`)
   - Datos estructurados completos
   - Metadata del escaneo
   - Todos los subdominios
   - Todas las categorías
   - Todos los resultados

2. **TXT** (`dork_scan_<dominio>_<timestamp>.txt`)
   - Reporte legible para humanos
   - Organizado por categoría
   - Incluye target, dork y URL

3. **URLs** (`dork_urls_<dominio>_<timestamp>.txt`)
   - Solo las URLs de Google
   - Una por línea
   - Listo para copiar y pegar en navegador

## 📋 Requisitos

- **Python 3.6 o superior**
- **¡Nada más!** - Sin dependencias externas

## 🔧 Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd dorks

# Dar permisos de ejecución
chmod +x dork_scanner.py

# ¡Listo para usar! No se requiere pip install
```

## 💻 Uso

### Sintaxis Básica

```bash
python3 dork_scanner.py -d <dominio>
```

### Ejemplos

**Escaneo completo con generación de subdominios:**
```bash
python3 dork_scanner.py -d example.com
```

**Solo dominio principal (sin subdominios):**
```bash
python3 dork_scanner.py -d example.com --no-subdomain-gen
```

### Opciones Disponibles

```
-d, --domain DOMAIN          Dominio objetivo (requerido)
--no-subdomain-gen          Omitir generación de subdominios
-h, --help                  Mostrar ayuda
```

## 📊 Ejemplo de Uso

```bash
$ python3 dork_scanner.py -d example.com

╔═══════════════════════════════════════════════════════════╗
║           Google Dork Scanner v2.0                        ║
║           100% OFFLINE - Sin dependencias de APIs         ║
║           Base de datos GHDB completa (300+ dorks)        ║
╚═══════════════════════════════════════════════════════════╝

[!] Use this tool only on domains you own or have permission to test
[*] Target Domain: example.com
[*] Modo: 100% Offline - Generación local de subdominios

[*] Generando subdominios candidatos (método offline)...

[*] Generando subdominios con 200+ prefijos comunes... ✓ 201 subdominios generados

[*] Iniciando escaneo de Google Dorks...
[*] Total de dorks (GHDB): 306
[*] Total de subdominios: 201
[*] Total de combinaciones: 61506
[!] Nota: Las búsquedas se generan pero NO se ejecutan automáticamente
[!] Debes copiar las URLs y abrirlas manualmente en tu navegador

[+] Total URLs generadas: 61506

[+] Reporte JSON guardado: dork_scan_example.com_20251116_120000.json
[+] Reporte TXT guardado: dork_scan_example.com_20251116_120000.txt
[+] Lista de URLs guardada: dork_urls_example.com_20251116_120000.txt

[+] Generación completada exitosamente!
[*] Abre el archivo de URLs y prueba cada una en tu navegador
```

## 📝 Flujo de Trabajo Recomendado

### 1. Ejecutar el Scanner
```bash
python3 dork_scanner.py -d target.com
```

### 2. Revisar los Archivos Generados
```bash
# Ver reporte de texto
less dork_scan_target.com_*.txt

# Ver JSON con jq
jq '.results[] | select(.category=="API Keys")' dork_scan_target.com_*.json

# Ver solo URLs
cat dork_urls_target.com_*.txt
```

### 3. Abrir URLs en Navegador

**Opción A - Manual:**
- Abre `dork_urls_target.com_*.txt`
- Copia y pega cada URL en tu navegador
- Verifica manualmente los resultados de Google

**Opción B - Script Bash (Cuidado con rate limiting):**
```bash
# NO recomendado - puede activar CAPTCHA de Google
while read url; do
    xdg-open "$url" # Linux
    # open "$url"   # macOS
    sleep 10
done < dork_urls_target.com_*.txt
```

### 4. Documentar Hallazgos

Para cada URL con resultados positivos en Google:
- Toma screenshot
- Documenta el hallazgo
- Verifica manualmente si es sensible
- Clasifica por severidad
- Reporta responsablemente

## 🎯 Categorías de Dorks Explicadas

### Críticas (High Priority)

**Config Files** - Archivos de configuración que pueden contener:
- Database credentials
- API keys
- Secret keys
- Connection strings

**Backups** - Backups expuestos:
- Database dumps
- Code backups
- Configuration backups

**Credentials** - Credenciales en texto plano:
- Passwords
- Usernames
- Default credentials

**API Keys** - Tokens y keys:
- AWS credentials
- API tokens
- OAuth secrets

**SSH Keys** - Claves privadas SSH expuestas

### Altas (Medium Priority)

**Admin Panels** - Paneles de administración:
- Login pages
- Admin dashboards
- Control panels

**Database Files** - Archivos de BD expuestos:
- .sql files
- .mdb files
- sqlite databases

**Git/SVN** - Repositorios expuestos:
- .git directories
- Source code

**Log Files** - Logs con información sensible:
- Error logs
- Access logs
- Debug logs

### Informativas (Low Priority)

**Server Info** - Información del servidor:
- phpinfo()
- Server status pages

**CMS/Frameworks** - Detección de CMS:
- WordPress
- Drupal
- Laravel

**Documents** - Documentos públicos:
- PDFs
- Office files

## 🔥 Casos de Uso

### 1. Bug Bounty
```bash
# Generar todas las URLs
python3 dork_scanner.py -d target.com

# Filtrar categorías críticas
jq '.results[] | select(.category | test("Credentials|API Keys|Config Files"))' \
   dork_scan_target.com_*.json | jq -r '.url' > critical_urls.txt

# Revisar URLs críticas manualmente
```

### 2. Auditoría de Seguridad Pre-Lanzamiento
```bash
# Solo dominio principal
python3 dork_scanner.py -d newsite.com --no-subdomain-gen

# Verificar que NO hay información sensible indexada
```

### 3. Análisis de Superficie de Ataque
```bash
# Escaneo completo
python3 dork_scanner.py -d mycompany.com

# Analizar todas las categorías
cat dork_scan_mycompany.com_*.txt | less
```

## 📊 Estadísticas

### Base de Datos de Dorks v2.0

| Categoría | Cantidad de Dorks |
|-----------|-------------------|
| Config Files | 10 |
| Backups | 7 |
| Log Files | 6 |
| Database Files | 6 |
| Credentials | 9 |
| API Keys | 8 |
| Directory Listing | 10 |
| Admin Panels | 14 |
| Server Info | 9 |
| Errors | 10 |
| Documents | 8 |
| CMS/Frameworks | 10 |
| Emails | 5 |
| Upload | 4 |
| Git/SVN | 7 |
| Cloud Storage | 5 |
| Devices | 5 |
| Installers | 5 |
| Path Traversal | 4 |
| Common Parameters | 6 |
| Shells | 6 |
| CI/CD | 6 |
| APIs | 7 |
| Containers | 5 |
| Monitoring | 7 |
| Dev Databases | 6 |
| Robots/Sitemaps | 3 |
| Test Pages | 4 |
| Temp Files | 4 |
| SSH Keys | 5 |
| Certificates | 4 |
| Financial | 4 |
| Apache Config | 3 |
| User Info | 3 |
| Registry | 2 |
| **TOTAL** | **306** |

### Prefijos de Subdominios

| Categoría | Cantidad |
|-----------|----------|
| Infraestructura Web | 10 |
| Email y Comunicación | 20 |
| FTP y Archivos | 17 |
| DNS | 10 |
| Desarrollo y Testing | 26 |
| APIs | 14 |
| Administración | 19 |
| Autenticación | 19 |
| Bases de Datos | 17 |
| Monitoreo | 21 |
| DevOps y CI/CD | 27 |
| Cloud | 16 |
| Contenido y Media | 25 |
| E-commerce | 12 |
| Colaboración | 21 |
| Mobile | 7 |
| Backups | 13 |
| CRM y Business | 16 |
| Interno/Corporativo | 14 |
| Servicios Específicos | 14 |
| Networking | 14 |
| Otros | 27 |
| **TOTAL** | **200+** |

## 🛡️ Buenas Prácticas

### 1. Autorización
- **SIEMPRE** obtén permiso escrito antes de escanear
- Verifica que el dominio está en scope
- Documenta la autorización

### 2. Rate Limiting de Google
- **NO** abras todas las URLs automáticamente
- Abre URLs manualmente con pausas
- Usa delays de al menos 10 segundos entre búsquedas
- Si ves CAPTCHA, espera varias horas

### 3. Verificación Manual
- **NUNCA** confíes 100% en los resultados automáticos
- Verifica manualmente cada hallazgo
- Puede haber falsos positivos

### 4. Documentación
- Guarda todos los reportes generados
- Toma screenshots de hallazgos
- Mantén evidencia de la autorización

### 5. Divulgación Responsable
- Reporta vulnerabilidades de manera responsable
- No explotes más allá de la verificación
- Sigue las políticas de disclosure del programa

## 🔧 Troubleshooting

### "El programa no encuentra nada"
- **Normal:** El programa solo genera URLs
- Debes abrir las URLs manualmente en Google
- Google mostrará los resultados reales

### "Demasiadas URLs generadas"
```bash
# Solo dominio principal
python3 dork_scanner.py -d example.com --no-subdomain-gen

# Esto genera solo ~300 URLs en lugar de 60,000+
```

### "Google muestra CAPTCHA"
- Estás haciendo demasiadas búsquedas muy rápido
- Espera varias horas antes de continuar
- Usa VPN o cambia tu IP
- Considera espaciar las búsquedas en varios días

### "Quiero solo ciertas categorías"
```bash
# Filtrar con jq
jq '.results[] | select(.category=="API Keys")' dork_scan_*.json | jq -r '.url'
```

## 📚 Recursos Adicionales

- **GHDB Original**: https://www.exploit-db.com/google-hacking-database
- **Google Dorks GitHub**: https://github.com/readloud/Google-Hacking-Database
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **Bug Bounty Platforms**:
  - HackerOne: https://hackerone.com
  - Bugcrowd: https://bugcrowd.com
  - YesWeHack: https://yeswehack.com

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
- Nuevos dorks basados en GHDB
- Más prefijos de subdominios
- Mejoras en la generación de reportes
- Corrección de bugs
- Documentación adicional

## 📝 Changelog

### v2.0 (2025-11-16) - **VERSIÓN MAYOR**
- 🔥 **CAMBIO RADICAL**: 100% Offline - Sin APIs externas
- 🚀 **300+ Google Dorks** de GHDB (Exploit-DB)
- 📡 **200+ prefijos** de subdominios (vs 90 en v1.1)
- ✅ **Cero dependencias** de Python
- 🗑️ Eliminado: requests, crt.sh, HackerTarget, AlienVault, ThreatCrowd
- ⚡ Generación instantánea de URLs (no hace peticiones HTTP)
- 📊 3 formatos de reporte: JSON, TXT, URLs
- 🎯 25+ categorías de dorks organizadas
- 📖 Documentación completamente reescrita

### v1.1 (2025-11-16)
- Agregadas fuentes: AlienVault OTX, ThreatCrowd
- Expandida lista de prefijos comunes a 90+
- Manejo robusto de errores

### v1.0 (2025-11-16)
- Versión inicial
- 80 Google Dorks
- Enumeración de subdominios con APIs
- Anti-detección básica

## 📄 Licencia

Esta herramienta se proporciona "tal cual" solo para fines educativos y de seguridad autorizada.

## 👤 Autor

Desarrollado para pruebas de seguridad autorizadas, Bug Bounty y reconocimiento ético.

---

**v2.0 - 100% Offline | 300+ GHDB Dorks | 200+ Subdomain Prefixes | Zero Dependencies**

**Recuerda**: Con gran poder viene gran responsabilidad. Usa esta herramienta éticamente y solo en dominios autorizados.
