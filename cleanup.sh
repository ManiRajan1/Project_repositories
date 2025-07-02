#!/bin/bash

# cleanup.sh — manage n8n docker-compose project
# Usage: ./cleanup.sh [option]
# Options:
#   stop    — stops the containers (keeps state)
#   down    — stops and removes containers (keeps volumes)
#   reset   — full cleanup: removes containers + volumes

set -e

COMPOSE_FILE="docker-compose.yml"

# Helper function
function usage() {
  echo "Usage: $0 [stop | down | reset]"
  echo "  stop   = docker-compose stop"
  echo "  down   = docker-compose down"
  echo "  reset  = docker-compose down -v (remove volumes too)"
  exit 1
}

# Validate argument
if [ $# -ne 1 ]; then
  usage
fi

case "$1" in
  stop)
    echo "⏸️  Stopping Docker containers..."
    docker-compose -f "$COMPOSE_FILE" stop
    ;;
  down)
    echo "🧹 Bringing down Docker containers (keeping volumes)..."
    docker-compose -f "$COMPOSE_FILE" down
    ;;
  reset)
    echo "🔥 Full cleanup: containers + volumes"
    docker-compose -f "$COMPOSE_FILE" down -v
    echo "🧽 Removing named volumes (if any left dangling)..."
    docker volume prune -f
    docker system prune -f
    ;;
  *)
    usage
    ;;
esac