# Ejemplos de Uso - Google Dork Scanner

## Escenarios Comunes

### 1. Escaneo Básico de un Dominio Propio

```bash
python3 dork_scanner.py -d midominio.com
```

**Qué hace:**
- Enumera subdominios automáticamente
- Prueba todos los dorks contra cada subdominio
- Genera reportes JSON y TXT
- Tiempo estimado: 30-60 minutos dependiendo del número de subdominios

### 2. Escaneo Rápido (Solo Dominio Principal)

```bash
python3 dork_scanner.py -d midominio.com --no-subdomain-enum
```

**Qué hace:**
- Omite la enumeración de subdominios
- Solo escanea el dominio principal
- Mucho más rápido (5-10 minutos)
- Útil para pruebas rápidas

### 3. Escaneo Sigiloso (Evitar Detección)

```bash
python3 dork_scanner.py -d midominio.com --delay 10 --threads 1
```

**Qué hace:**
- Espera 10 segundos entre cada petición
- Usa solo 1 thread (secuencial)
- Minimiza el riesgo de ser bloqueado por Google
- Muy lento pero más seguro

### 4. Escaneo Balanceado (Recomendado)

```bash
python3 dork_scanner.py -d midominio.com --delay 5 --threads 2
```

**Qué hace:**
- Balance entre velocidad y precaución
- Delay moderado de 5 segundos
- 2 threads para mayor eficiencia
- Configuración recomendada para la mayoría de casos

## Flujo de Trabajo Típico

### Paso 1: Reconocimiento Inicial
```bash
# Escaneo rápido para ver qué subdominios existen
python3 dork_scanner.py -d target.com --delay 3
```

### Paso 2: Análisis de Resultados
```bash
# Revisar el archivo JSON generado
cat dork_scan_target.com_*.json | jq '.successful_dorks'

# O revisar el archivo de texto
less dork_scan_target.com_*.txt
```

### Paso 3: Verificación Manual
```bash
# Tomar las URLs del reporte y verificarlas manualmente en el navegador
# Ejemplo: abrir en navegador las URLs marcadas como "ENCONTRADO"
```

## Interpretando los Resultados

### Ejemplo de Salida en Consola

```
[+] Total subdominios encontrados: 15

[*] Escaneando: www.example.com
  [1/80] (1.3%) Archivos Sensibles: ✓ ENCONTRADO
  [2/80] (2.5%) Credenciales: ✗
  [3/80] (3.8%) Directorios Expuestos: ✓ ENCONTRADO
  ...
```

**Interpretación:**
- ✓ ENCONTRADO = Google tiene resultados para ese dork
- ✗ = No se encontraron resultados

### Ejemplo de Resultado Positivo

```json
{
  "category": "Archivos Sensibles",
  "dork": "site:example.com ext:log",
  "target": "www.example.com",
  "url": "https://www.google.com/search?q=site%3Aexample.com+ext%3Alog",
  "has_results": true,
  "result_count": "About 45 results"
}
```

**Qué hacer:**
1. Abrir la URL en un navegador
2. Revisar cada resultado de Google
3. Determinar si hay información sensible
4. Documentar el hallazgo
5. Remediar si es necesario

## Casos de Uso Específicos

### Auditoría de Seguridad Pre-Lanzamiento

```bash
# Antes de lanzar un sitio web, verificar qué información está indexada
python3 dork_scanner.py -d nuevositio.com --no-subdomain-enum --delay 5
```

**Buscar específicamente:**
- Archivos de configuración expuestos
- Directorios de desarrollo/testing
- Información de staging

### Bug Bounty / Pentest

```bash
# Reconocimiento completo para programa de bug bounty
python3 dork_scanner.py -d target.com --delay 5 --threads 2
```

**Priorizar:**
- Paneles de administración
- APIs expuestas
- Credenciales en código fuente
- Backups de bases de datos

### Monitoreo Continuo

```bash
# Ejecutar mensualmente para detectar nuevas exposiciones
python3 dork_scanner.py -d miempresa.com --delay 7
```

**Comparar:**
- Resultados del mes anterior
- Nuevos subdominios indexados
- Nuevos archivos sensibles

## Ejemplos de Hallazgos Comunes

### 1. Archivo .env Expuesto

**Dork que lo detecta:**
```
site:example.com filetype:env "DB_PASSWORD"
```

**Impacto:** CRÍTICO
- Contraseñas de base de datos
- API keys
- Secretos de aplicación

**Remediación:**
- Eliminar el archivo del servidor web
- Rotar todas las credenciales expuestas
- Configurar robots.txt y .htaccess
- Solicitar a Google eliminación del cache

### 2. Directorio de Backups Abierto

**Dork que lo detecta:**
```
site:example.com intitle:"index of" "backup"
```

**Impacto:** ALTO
- Código fuente
- Bases de datos
- Configuraciones

**Remediación:**
- Desactivar listado de directorios
- Mover backups fuera del webroot
- Proteger con autenticación

### 3. Panel de Administración Sin Protección

**Dork que lo detecta:**
```
site:example.com inurl:admin
```

**Impacto:** ALTO
- Acceso potencial a funciones administrativas
- Superficie de ataque aumentada

**Remediación:**
- Implementar autenticación fuerte
- Usar 2FA
- Restringir por IP si es posible
- Usar URLs no predecibles

### 4. phpinfo() Expuesto

**Dork que lo detecta:**
```
site:example.com ext:php intitle:phpinfo "published by the PHP Group"
```

**Impacto:** MEDIO
- Información del servidor
- Configuración PHP
- Variables de entorno

**Remediación:**
- Eliminar archivos phpinfo
- Deshabilitar en producción

## Tips y Trucos

### Reducir Falsos Positivos

1. **Verificar manualmente** cada resultado
2. **Revisar el cache de Google** usando `cache:url`
3. **Comprobar si el contenido sigue existiendo**

### Evitar Bloqueos de Google

1. **Usar delays largos** (5-10 segundos)
2. **Escanear en horarios de bajo uso** (noche/madrugada)
3. **Dividir escaneos grandes** en múltiples sesiones
4. **Cambiar IP** si es necesario (VPN)

### Maximizar Efectividad

1. **Escanear después de deploys** para detectar nuevas exposiciones
2. **Combinar con otras herramientas** (Shodan, Censys)
3. **Documentar bien los hallazgos** para tracking
4. **Automatizar escaneos regulares** (cron jobs)

## Automatización con Cron

### Escaneo Semanal

```bash
# Editar crontab
crontab -e

# Agregar línea para escaneo cada domingo a las 2 AM
0 2 * * 0 cd /path/to/dorks && python3 dork_scanner.py -d midominio.com --delay 10 >> /var/log/dork_scanner.log 2>&1
```

### Script de Comparación de Resultados

```bash
#!/bin/bash
# compare_scans.sh - Compara resultados entre escaneos

OLD_SCAN="dork_scan_example.com_20250101_120000.json"
NEW_SCAN="dork_scan_example.com_20250201_120000.json"

echo "Nuevos hallazgos:"
jq -r '.successful_dorks[].dork' $NEW_SCAN | \
  grep -vFf <(jq -r '.successful_dorks[].dork' $OLD_SCAN)
```

## Preguntas Frecuentes

**P: ¿Cuánto tiempo toma un escaneo completo?**
R: Depende del número de subdominios. Con delay de 3 segundos y 80 dorks:
- 1 subdominio: ~10 minutos
- 10 subdominios: ~100 minutos
- 50 subdominios: ~8 horas

**P: ¿Google me puede bloquear?**
R: Sí, si haces demasiadas peticiones muy rápido. Usa delays apropiados (5+ segundos).

**P: ¿Los resultados son 100% precisos?**
R: No. Siempre verifica manualmente. Puede haber falsos positivos y negativos.

**P: ¿Puedo usar esto en programas de bug bounty?**
R: Sí, siempre que esté dentro del scope del programa y sigas sus reglas.

**P: ¿Qué hago si encuentro algo crítico?**
R:
1. Documentar el hallazgo
2. No explotarlo más allá de la verificación
3. Reportarlo responsablemente al propietario
4. Seguir el proceso de divulgación responsable

## Recursos Adicionales

- **Google Hacking Database**: https://www.exploit-db.com/google-hacking-database
- **GHDB GitHub**: https://github.com/topics/google-dorks
- **Bug Bounty Platforms**: HackerOne, Bugcrowd, YesWeHack
- **OSINT Framework**: https://osintframework.com/

---

**Recuerda**: Esta herramienta es para uso ético y autorizado únicamente.
