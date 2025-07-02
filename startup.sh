#!/bin/bash
set -x
sudo docker compose up -d
chown -R 1000:1000 n8n/data