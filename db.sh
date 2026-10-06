#!/usr/bin/env bash
# Base PostgreSQL del proyecto en Docker (puerto local 5433). Uso: ./db.sh arrancar|parar|estado|psql
case "$1" in
  arrancar)
    docker start gestion-nodos-db 2>/dev/null || docker run -d --name gestion-nodos-db \
      -e POSTGRES_USER=nodos -e POSTGRES_PASSWORD=nodos -e POSTGRES_DB=nodos \
      -p 127.0.0.1:5433:5432 -v gestion-nodos-datos:/var/lib/postgresql/data \
      --restart unless-stopped postgres:16-alpine ;;
  parar)  docker stop gestion-nodos-db ;;
  estado) docker exec gestion-nodos-db pg_isready -U nodos ;;
  psql)   shift; docker exec -it gestion-nodos-db psql -U nodos "${@:-nodos}" ;;
  *) echo "uso: $0 arrancar|parar|estado|psql [base]"; exit 1 ;;
esac
