.PHONY: build up down logs shell user-add user-list dev

# ── Docker ────────────────────────────────────────────
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f pizarra

shell:
	docker-compose exec pizarra bash

restart:
	docker-compose restart pizarra

# ── Usuarios ──────────────────────────────────────────
# Uso: make user-add USER=nombre PASS=contraseña
user-add:
	docker-compose exec pizarra python manage_users.py add $(USER) $(PASS)

user-list:
	docker-compose exec pizarra python manage_users.py list

# Uso: make user-deactivate USER=nombre
user-deactivate:
	docker-compose exec pizarra python manage_users.py deactivate $(USER)

# ── Desarrollo local (sin Docker) ────────────────────
dev:
	FLASK_ENV=development python run.py
