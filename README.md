# demo-bet-app

## docker

dev:

docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

docker compose -f docker-compose.yml -f docker-compose.dev.yml down

---

prod:

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

docker compose -f docker-compose.yml -f docker-compose.prod.yml down
