# kpi-web-labs

## How to run
1. Create .env files in `users_service/` and root folders (see `env.example`).
2. Create services.yaml in `api_gateway/` (see `services.yaml.example`).
3. Run via docker compose:
   ```bash
   docker compose up -d
   ```
4. Run migrations:
   ```bash
   docker exec -it users-api bash
   poetry run alembic upgrade head
   ```
