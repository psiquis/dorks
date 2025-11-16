# Google Dork Scanner v2.1 🔍

**Herramienta de reconocimiento automatizado con enumeración dinámica de subdominios y 300+ Google Dorks de GHDB**

## 🎯 ¿Qué hay de nuevo en v2.1?

### ✅ Enumeración DINÁMICA de Subdominios
- **Obtiene subdominios REALES** de fuentes online:
  - **crt.sh** - Certificados SSL públicos
  - **HackerTarget** - API gratuita
  - **AlienVault OTX** - Passive DNS
  - **ThreatCrowd** - Threat Intelligence
- **Fallback inteligente**: Si las APIs fallan, usa 200+ prefijos comunes
- **Modo Híbrido**: Combina subdominios reales de APIs + prefijos comunes

### 🚀 300+ Google Dorks de GHDB
- Base de datos completa de **306 Google Dorks**
- Basado en **GHDB** (Google Hacking Database de Exploit-DB)
- **35 categorías** organizadas

### ⚡ Flexible
- **Modo Online** (default): Usa APIs + fallback
- **Modo --offline**: Solo usa prefijos comunes (sin internet)
- **Robusto**: Continúa funcionando aunque APIs fallen

## ⚠️ Advertencia Legal

**IMPORTANTE:** Esta herramienta debe utilizarse únicamente en:
- Dominios de tu propiedad
- Sistemas para los cuales tienes autorización explícita
- Entornos de prueba/laboratorio
- Programas de Bug Bounty donde el dominio esté en scope

El uso no autorizado puede violar leyes locales e internacionales.

## 📋 Requisitos

- **Python 3.6+**
- **requests** (para enumeración de subdominios)

## 🔧 Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd dorks

# Instalar dependencias
pip3 install -r requirements.txt

# Dar permisos de ejecución
chmod +x dork_scanner.py
```

## 💻 Uso

### Sintaxis Básica

```bash
python3 dork_scanner.py -d <dominio> [opciones]
```

### Opciones

```
-d, --domain DOMAIN      Dominio objetivo (requerido)
--no-subdomain-gen       Omitir generación de subdominios (solo dominio principal)
--offline                Modo offline: solo prefijos comunes, no APIs
-h, --help               Mostrar ayuda
```

### Ejemplos

**1. Escaneo completo con enumeración dinámica (RECOMENDADO):**
```bash
python3 dork_scanner.py -d example.com
```
*Usa APIs para obtener subdominios reales + agrega prefijos comunes como fallback*

**2. Modo offline (sin APIs):**
```bash
python3 dork_scanner.py -d example.com --offline
```
*Solo usa 200+ prefijos comunes, no requiere internet*

**3. Solo dominio principal:**
```bash
python3 dork_scanner.py -d example.com --no-subdomain-gen
```
*Genera ~306 URLs solo para el dominio principal*

## 📊 Ejemplo de Ejecución

```bash
$ python3 dork_scanner.py -d example.com

╔═══════════════════════════════════════════════════════════╗
║           Google Dork Scanner v2.1                        ║
║           Enumeración Dinámica de Subdominios             ║
║           Base de datos GHDB completa (300+ dorks)        ║
╚═══════════════════════════════════════════════════════════╝

[!] Use this tool only on domains you own or have permission to test
[*] Target Domain: example.com
[*] Modo: ONLINE (APIs + Fallback)

[*] Enumerando subdominios desde fuentes online...

[*] crt.sh... ✓ 47
[*] HackerTarget... ✓ 23
[*] AlienVault OTX... ✓ 31
[*] ThreatCrowd... ✓ 18

[+] Subdominios desde APIs: 87
[*] Agregando prefijos comunes... ✓ 200 agregados

============================================================
[+] Total subdominios únicos: 245
============================================================

[*] Iniciando escaneo de Google Dorks...
[*] Total de dorks (GHDB): 306
[*] Total de subdominios: 245
[*] Total de combinaciones: 74,970

[+] Reporte JSON guardado: dork_scan_example.com_20251116_120000.json
[+] Reporte TXT guardado: dork_scan_example.com_20251116_120000.txt
[+] Lista de URLs guardada: dork_urls_example.com_20251116_120000.txt

[+] Generación completada exitosamente!
```

## 📁 Archivos Generados

El programa genera **3 archivos**:

### 1. JSON (`dork_scan_<dominio>_<timestamp>.json`)
- Datos estructurados completos
- Subdominios encontrados
- Todas las URLs generadas
- Metadata del escaneo

### 2. TXT (`dork_scan_<dominio>_<timestamp>.txt`)
- Reporte legible para humanos
- Organizado por categoría
- Incluye: target, dork y URL

### 3. URLs (`dork_urls_<dominio>_<timestamp>.txt`)
- Solo las URLs de Google
- Una por línea
- Listo para copiar/pegar en navegador

## 🎯 Enumeración de Subdominios

### Fuentes de Subdominios (APIs Gratuitas)

| Fuente | Descripción | Autenticación | Rate Limit |
|--------|-------------|---------------|------------|
| **crt.sh** | Certificados SSL públicos | ❌ No | ✅ Sin límites |
| **HackerTarget** | API gratuita DNS | ❌ No | ⚠️ 100/día |
| **AlienVault OTX** | Passive DNS | ❌ No | ✅ Generoso |
| **ThreatCrowd** | Threat Intel | ❌ No | ✅ Generoso |
| **Prefijos Comunes** | 200+ generados localmente | ❌ No | ✅ Ilimitado |

### ¿Qué pasa si las APIs fallan?

El programa es **robusto y resiliente**:

- ✅ Si crt.sh falla → Continúa con las otras fuentes
- ✅ Si HackerTarget alcanza el límite → Continúa con las otras
- ✅ Si todas las APIs fallan → Usa 200+ prefijos comunes
- ✅ **SIEMPRE** agrega prefijos comunes como fallback
- ✅ Nunca falla completamente

### Modo Offline vs Online

| Característica | Modo ONLINE (default) | Modo OFFLINE (--offline) |
|----------------|----------------------|--------------------------|
| APIs externas | ✅ Sí | ❌ No |
| Requiere internet | ✅ Sí | ❌ No |
| Subdominios reales | ✅ Sí | ❌ No |
| Prefijos comunes | ✅ Sí (como fallback) | ✅ Sí (únicos) |
| Velocidad | Media (APIs + delays) | Rápida (local) |
| Cobertura | Alta (reales + comunes) | Media (solo comunes) |

**Recomendación:** Usa modo ONLINE para máxima cobertura.

## 🔍 Base de Datos de Google Dorks

### 306 Dorks en 35 Categorías

<details>
<summary>Ver todas las categorías (click para expandir)</summary>

1. **Config Files** (10) - Archivos .env, .ini, .conf, .yaml
2. **Backups** (7) - .bak, .backup, .old, dumps SQL
3. **Log Files** (6) - Logs de errores y acceso
4. **Database Files** (6) - .sql, .mdb, sqlite
5. **Credentials** (9) - Passwords, usernames
6. **API Keys** (8) - AWS keys, tokens, secrets
7. **Directory Listing** (10) - Directorios expuestos
8. **Admin Panels** (14) - Login, admin, dashboard
9. **Server Info** (9) - phpinfo, server status
10. **Errors** (10) - SQL errors, PHP warnings
11. **Documents** (8) - PDFs, Office files
12. **CMS/Frameworks** (10) - WordPress, Drupal, Laravel
13. **Emails** (5) - Direcciones de correo expuestas
14. **Upload** (4) - Formularios de carga
15. **Git/SVN** (7) - Repositorios expuestos (.git, .svn)
16. **Cloud Storage** (5) - S3, Azure Blob, GCS
17. **Devices** (5) - Webcams, IoT
18. **Installers** (5) - Scripts de instalación
19. **Path Traversal** (4) - Parámetros vulnerables
20. **Common Parameters** (6) - id=, user=, redirect=
21. **Shells** (6) - Web shells, backdoors
22. **CI/CD** (6) - Jenkins, GitLab, Travis
23. **APIs** (7) - Swagger, GraphQL, API docs
24. **Containers** (5) - Docker, Kubernetes
25. **Monitoring** (7) - Grafana, Prometheus, Kibana
26. **Dev Databases** (6) - phpMyAdmin, Adminer
27. **Robots/Sitemaps** (3) - robots.txt, sitemap.xml
28. **Test Pages** (4) - Páginas de prueba
29. **Temp Files** (4) - Archivos temporales
30. **SSH Keys** (5) - Claves privadas SSH
31. **Certificates** (4) - .crt, .pem, .p12
32. **Financial** (4) - Credit cards, invoices
33. **Apache Config** (3) - .htaccess, .htpasswd
34. **User Info** (3) - Listas de usuarios
35. **Registry** (2) - WHOIS, registrant

**TOTAL: 306 dorks**

</details>

## 📝 Flujo de Trabajo Recomendado

### 1. Ejecutar Scanner
```bash
python3 dork_scanner.py -d target.com
```

### 2. Revisar Resultados
```bash
# Ver reporte de texto
less dork_scan_target.com_*.txt

# Ver subdominios encontrados
jq '.subdomains[]' dork_scan_target.com_*.json

# Filtrar categorías críticas
jq '.results[] | select(.category | test("API Keys|Credentials|SSH Keys"))' \
   dork_scan_target.com_*.json | jq -r '.url' > critical_urls.txt
```

### 3. Abrir URLs Manualmente
```bash
# Ver archivo de URLs
cat dork_urls_target.com_*.txt

# Copiar y pegar cada URL en tu navegador
# Verificar resultados de Google manualmente
```

### 4. Documentar Hallazgos
- Toma screenshots
- Documenta severidad
- Reporta responsablemente

## 🎯 Casos de Uso

### Bug Bounty
```bash
# Máxima cobertura
python3 dork_scanner.py -d target.com

# Filtrar críticos
jq '.results[] | select(.category=="API Keys")' dork_scan_*.json | jq -r '.url'
```

### Auditoría Pre-Lanzamiento
```bash
# Solo dominio principal
python3 dork_scanner.py -d newsite.com --no-subdomain-gen
```

### Pentesting
```bash
# Escaneo completo
python3 dork_scanner.py -d client.com

# Analizar resultados
cat dork_scan_client.com_*.txt | less
```

## 🛡️ Buenas Prácticas

### 1. Autorización
- ✅ Obtén permiso escrito siempre
- ✅ Verifica scope del programa

### 2. Rate Limiting de Google
- ❌ NO abras todas las URLs automáticamente
- ✅ Abre manualmente con pausas (10+ segundos)
- ✅ Si ves CAPTCHA, espera horas

### 3. Verificación Manual
- ✅ Verifica cada hallazgo manualmente
- ✅ Puede haber falsos positivos

## 🔧 Troubleshooting

### "No encuentra subdominios"
```bash
# Prueba modo offline
python3 dork_scanner.py -d example.com --offline

# O solo dominio principal
python3 dork_scanner.py -d example.com --no-subdomain-gen
```

### "requests no está instalado"
```bash
pip3 install requests

# O usa modo offline
python3 dork_scanner.py -d example.com --offline
```

### "HackerTarget rate limit"
**Normal.** El programa continúa con las otras 3 fuentes + prefijos comunes.

### "Google muestra CAPTCHA"
- Estás buscando demasiado rápido
- Espera varias horas
- Usa VPN o cambia IP
- Espacía búsquedas en días

## 📊 Estadísticas v2.1

```
Google Dorks: 306
Categorías: 35
Fuentes de subdominios: 4 APIs + 1 local
Prefijos comunes: 200+
Dependencias: 1 (requests)
```

## 📚 Recursos

- **GHDB Oficial**: https://www.exploit-db.com/google-hacking-database
- **Google Dorks GitHub**: https://github.com/readloud/Google-Hacking-Database
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/

## 📝 Changelog

### v2.1 (2025-11-16)
- ✨ **NUEVA**: Enumeración DINÁMICA de subdominios
- ✨ **4 fuentes de APIs**: crt.sh, HackerTarget, AlienVault OTX, ThreatCrowd
- ✨ **Modo híbrido**: APIs + fallback a prefijos comunes
- ✨ **Flag --offline**: Para uso sin internet
- ✨ **Robusto**: Continúa funcionando si APIs fallan
- ✨ **Smart fallback**: Siempre agrega prefijos comunes
- 📖 Documentación actualizada

### v2.0 (2025-11-16)
- 306 Google Dorks de GHDB
- 200+ prefijos de subdominios
- 100% offline (en v2.0)
- 3 formatos de reporte

### v1.x
- Versiones anteriores

## 📄 Licencia

Esta herramienta se proporciona "tal cual" solo para fines educativos y de seguridad autorizada.

---

**v2.1 - Enumeración Dinámica | 306 GHDB Dorks | 4 APIs + Fallback | Modo Híbrido**

**Recuerda**: Usa esta herramienta éticamente y solo en dominios autorizados. 🔒
