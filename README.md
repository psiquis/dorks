# Google Dork Scanner 🔍

Herramienta automatizada de reconocimiento que utiliza Google Dorks para identificar información sensible en dominios y subdominios.

## ⚠️ Advertencia Legal

**IMPORTANTE:** Esta herramienta debe utilizarse únicamente en:
- Dominios de tu propiedad
- Sistemas para los cuales tienes autorización explícita para realizar pruebas de seguridad
- Entornos de prueba/laboratorio

El uso no autorizado puede violar:
- Términos de servicio de Google
- Leyes de privacidad y protección de datos
- Leyes de ciberseguridad locales e internacionales

El autor no se hace responsable del uso indebido de esta herramienta.

## 🚀 Características

- **Enumeración automática de subdominios** usando múltiples fuentes **GRATUITAS y SIN API KEYS**:
  - **crt.sh** - Certificados SSL/TLS públicos
  - **HackerTarget** - API gratuita (puede tener rate limits)
  - **AlienVault OTX** - Passive DNS (gratuito, sin autenticación)
  - **ThreatCrowd** - Threat intelligence (gratuito, sin autenticación)
  - **Prefijos Comunes** - 90+ prefijos comunes expandidos
  - ✅ **Manejo robusto de errores** - Continúa aunque algunas fuentes fallen

- **Base de datos exhaustiva de Google Dorks** que incluye:
  - Archivos sensibles (configs, backups, logs)
  - Credenciales y secretos
  - Directorios expuestos
  - Paneles de administración
  - Errores y debugging
  - Información de servidores
  - Documentos confidenciales
  - APIs y endpoints
  - Git/SVN exposure
  - Y más de 80 patrones diferentes

- **Características anti-detección**:
  - User agents aleatorios
  - Delays configurables entre peticiones
  - Headers realistas

- **Reportes detallados**:
  - Salida en consola con colores
  - Reporte JSON con todos los detalles
  - Reporte en texto plano

## 📋 Requisitos

- Python 3.6 o superior
- Módulos de Python:
  - requests

## 🔧 Instalación

1. Clonar o descargar el script:
```bash
git clone <repo-url>
cd dorks
```

2. Instalar dependencias:
```bash
pip3 install requests
# o usar el archivo requirements.txt
pip3 install -r requirements.txt
```

3. Dar permisos de ejecución:
```bash
chmod +x dork_scanner.py
```

## 💻 Uso

### Uso básico
```bash
python3 dork_scanner.py -d example.com
```

### Opciones disponibles

```bash
python3 dork_scanner.py --help
```

**Parámetros:**

- `-d, --domain DOMAIN` : **[Requerido]** Dominio objetivo (ej: example.com)
- `--delay SECONDS` : Delay entre peticiones en segundos (default: 3)
- `--threads NUM` : Número máximo de threads (default: 3)
- `--no-subdomain-enum` : Omitir enumeración de subdominios (solo escanea dominio principal)

### Ejemplos

**Escaneo completo con enumeración de subdominios:**
```bash
python3 dork_scanner.py -d example.com
```

**Escaneo solo del dominio principal (sin subdominios):**
```bash
python3 dork_scanner.py -d example.com --no-subdomain-enum
```

**Escaneo con delay personalizado (más lento, más seguro):**
```bash
python3 dork_scanner.py -d example.com --delay 5
```

**Escaneo conservador (delay largo, pocos threads):**
```bash
python3 dork_scanner.py -d example.com --delay 10 --threads 1
```

## 📊 Salida

La herramienta genera tres tipos de salida:

### 1. Consola
Muestra en tiempo real el progreso del escaneo con colores:
- 🔵 Azul: Información general
- 🟢 Verde: Resultados exitosos
- 🔴 Rojo: Sin resultados
- 🟡 Amarillo: Advertencias

### 2. Archivo JSON
`dork_scan_<dominio>_<timestamp>.json`

Contiene:
- Información del escaneo
- Lista de subdominios encontrados
- Todos los dorks probados
- Resultados exitosos con detalles completos

### 3. Archivo de Texto
`dork_scan_<dominio>_<timestamp>.txt`

Reporte legible con:
- Resumen del escaneo
- Resultados organizados por categoría
- URLs de Google con los dorks aplicados

## 🎯 Categorías de Dorks

El scanner incluye las siguientes categorías:

1. **Archivos Sensibles** - Configs, backups, logs, bases de datos
2. **Credenciales** - Passwords, API keys, tokens
3. **Directorios Expuestos** - Listados de directorios sin protección
4. **Paneles de Administración** - Login pages, admin panels
5. **Información de Servidor** - phpinfo, server status
6. **Errores** - Mensajes de error SQL, PHP, etc.
7. **Documentos** - PDFs, Office docs marcados como confidenciales
8. **CMS/Frameworks** - WordPress, Joomla, Django, Laravel
9. **Emails** - Direcciones de correo expuestas
10. **Upload** - Formularios de subida de archivos
11. **Git/SVN** - Repositorios expuestos
12. **Cloud Storage** - Buckets S3, storage expuesto
13. **Dispositivos** - Webcams, IoT devices
14. **CI/CD** - Jenkins, GitLab, CircleCI
15. **APIs** - Endpoints, Swagger, GraphQL

## 🛡️ Buenas Prácticas

1. **Rate Limiting**: Usa delays apropiados (3-10 segundos) para evitar ser bloqueado
2. **Autorización**: Siempre obtén permiso escrito antes de escanear
3. **Horarios**: Realiza escaneos en horarios de bajo tráfico si es posible
4. **Documentación**: Guarda los reportes como evidencia de hallazgos
5. **Responsabilidad**: Reporta vulnerabilidades de manera responsable

## 🔍 Interpretación de Resultados

### Resultados Positivos
Un resultado positivo significa que Google encontró páginas que coinciden con el dork. **No garantiza** una vulnerabilidad, pero indica áreas que requieren:
- Verificación manual
- Análisis de seguridad
- Posible remediación

### Falsos Positivos
Pueden ocurrir cuando:
- El contenido está protegido pero indexado
- Las páginas son públicas intencionalmente
- El resultado es histórico (ya no existe)

### Verificación Manual
Siempre verifica manualmente:
1. Abre la URL generada en el reporte
2. Revisa si el contenido es sensible
3. Verifica si está protegido adecuadamente
4. Documenta el hallazgo

## 🐛 Limitaciones

- **Rate Limiting**: Google puede bloquear temporalmente IPs con muchas búsquedas
- **CAPTCHA**: Puede aparecer si se detecta actividad automatizada
- **Resultados Parciales**: No todos los resultados pueden ser detectados automáticamente
- **Cambios en Google**: La estructura HTML de Google puede cambiar
- **APIs Externas**: La enumeración de subdominios depende de servicios de terceros

## 📡 Fuentes de Subdominios - Información Detallada

### ✅ Fuentes que NO requieren API Key

1. **crt.sh**
   - Fuente: Certificados SSL/TLS públicos
   - Confiabilidad: ⭐⭐⭐⭐⭐ (Muy alta)
   - Requiere: Nada
   - Si falla: El programa continúa con las otras fuentes

2. **AlienVault OTX**
   - Fuente: Passive DNS database
   - Confiabilidad: ⭐⭐⭐⭐ (Alta)
   - Requiere: Nada (sin autenticación)
   - Si falla: El programa continúa con las otras fuentes

3. **ThreatCrowd**
   - Fuente: Threat intelligence
   - Confiabilidad: ⭐⭐⭐ (Media)
   - Requiere: Nada (sin autenticación)
   - Si falla: El programa continúa con las otras fuentes

4. **HackerTarget**
   - Fuente: DNS database
   - Confiabilidad: ⭐⭐⭐ (Media - tiene rate limits)
   - Requiere: Nada (API gratuita sin key)
   - Limitación: 100 búsquedas por día por IP
   - Si alcanzas el límite: Muestra advertencia pero continúa

5. **Prefijos Comunes**
   - Fuente: Lista de 90+ prefijos comunes
   - Confiabilidad: ⭐⭐⭐⭐ (Alta - siempre disponible)
   - Requiere: Nada
   - Nunca falla: Genera subdominios localmente

### 🔄 Qué hace el programa si una fuente falla

El programa está diseñado para ser **robusto ante fallos**:

- ✅ Si **crt.sh** no está disponible → Muestra advertencia y continúa con las demás fuentes
- ✅ Si **HackerTarget** alcanzó el rate limit → Muestra advertencia y continúa
- ✅ Si **AlienVault** falla → Muestra advertencia y continúa
- ✅ Si **ThreatCrowd** falla → Muestra advertencia y continúa
- ✅ **Prefijos Comunes** → Siempre funciona (no depende de APIs externas)

**Resultado:** Siempre tendrás al menos la lista de prefijos comunes, asegurando que el programa **nunca falle completamente** en la enumeración de subdominios.

## 🔧 Troubleshooting

### "No se encontraron subdominios"
- Verifica la conectividad a internet
- El dominio puede no tener subdominios públicos
- Usa `--no-subdomain-enum` para escanear solo el dominio principal

### "Muchos errores de conexión"
- Reduce el número de threads: `--threads 1`
- Aumenta el delay: `--delay 10`
- Verifica tu conexión a internet

### "Google muestra CAPTCHA"
- Espera algunas horas antes de reintentar
- Usa una VPN o cambia tu IP
- Aumenta significativamente el delay

### "El script es muy lento"
- Es intencional para evitar detección
- Puedes reducir el delay pero aumentas el riesgo de bloqueo
- Considera escanear en múltiples sesiones

## 📚 Recursos Adicionales

- [Google Hacking Database (GHDB)](https://www.exploit-db.com/google-hacking-database)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bug Bounty Playbook](https://payhip.com/b/wAoh)

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
- Nuevos dorks
- Mejoras en la detección
- Optimizaciones de rendimiento
- Corrección de bugs

## 📝 Changelog

### v1.1 (2025-11-16)
- ✨ **Mejora mayor**: Sin dependencia de API keys
- ✨ Agregadas 2 nuevas fuentes de subdominios:
  - AlienVault OTX (Passive DNS)
  - ThreatCrowd (Threat Intelligence)
- ✨ Expandida lista de prefijos comunes de 30 a 90+
- ✨ Manejo robusto de errores - continúa aunque APIs fallen
- ✨ Mejores mensajes de error informativos
- ✨ Validación y limpieza mejorada de subdominios
- ✨ Indicadores visuales de estado por fuente (✓/⚠)
- 📖 Documentación expandida sobre fuentes de datos

### v1.0 (2025-11-16)
- Versión inicial
- 80+ Google Dorks
- Enumeración de subdominios múltiple (crt.sh, HackerTarget, Common)
- Reportes JSON y TXT
- Anti-detección básica

## 📄 Licencia

Esta herramienta se proporciona "tal cual" solo para fines educativos y de seguridad autorizada.

## 👤 Autor

Desarrollado para pruebas de seguridad autorizadas y reconocimiento ético.

---

**Recuerda**: Con gran poder viene gran responsabilidad. Usa esta herramienta éticamente.
