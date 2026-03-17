# 🛒 iPizarra

Lista de la compra web con catálogo de Mercadona.  
Desplegada en `pizarra.mcanadas29dev.com` vía Cloudflare Tunnel.

## Stack

- **Backend**: Python 3.12 · Flask · flask-login · Gunicorn
- **Frontend**: Jinja2 · HTML/CSS/JS puro
- **BD datos**: SQLite (`ipizarra.db`) — solo lectura para catálogo, escritura para `lista_compra`
- **BD auth**: SQLite (`users.db`) — gestión de usuarios
- **Infraestructura**: Docker · Cloudflare Tunnel · Debian server local

## Inicio rápido

### 1. Clonar y configurar entorno

```bash
git clone <repo> pizarra
cd pizarra
cp .env.example .env
# Editar .env con tu SECRET_KEY segura
```

### 2. Colocar la base de datos

```bash
cp /ruta/a/ipizarra.db data/ipizarra.db
```

### 3. Construir y arrancar

```bash
make build
make up
```

### 4. Crear el primer usuario

```bash
make user-add USER=admin PASS=tu_contraseña_segura
```

### 5. Acceder

- Local: `http://localhost:8001`
- Producción: `https://pizarra.mcanadas29dev.com`

## Comandos útiles

| Comando | Descripción |
|---|---|
| `make up` | Arrancar contenedor |
| `make down` | Parar contenedor |
| `make logs` | Ver logs en tiempo real |
| `make shell` | Shell dentro del contenedor |
| `make user-add USER=x PASS=y` | Crear usuario |
| `make user-list` | Listar usuarios |
| `make dev` | Desarrollo local sin Docker |

## Cloudflare Tunnel

En el fichero de configuración del tunnel en Debian (`~/.cloudflared/config.yml`):

```yaml
tunnel: <tu-tunnel-id>
credentials-file: /home/usuario/.cloudflared/<tu-tunnel-id>.json

ingress:
  - hostname: pizarra.mcanadas29dev.com
    service: http://localhost:8001
  # ... otras reglas existentes
  - service: http_status:404
```

Reiniciar el tunnel tras el cambio:

```bash
sudo systemctl restart cloudflared
```

## Estructura del proyecto

```
pizarra/
├── app/
│   ├── __init__.py        # create_app (factory pattern)
│   ├── config.py          # Config por entorno
│   ├── extensions.py      # flask-login
│   ├── database.py        # Conexiones SQLite
│   ├── auth/              # Blueprint auth (/auth/login, /auth/logout)
│   ├── main/              # Blueprint main (/, /toggle, /catalogo, /api/productos)
│   ├── models/            # User model
│   ├── static/            # CSS, JS, imágenes
│   └── templates/         # Jinja2 templates
├── data/                  # BDs (NO versionadas en git)
├── tests/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── manage_users.py        # CLI de gestión de usuarios
├── requirements.txt
└── run.py
```
