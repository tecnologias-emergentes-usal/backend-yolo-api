#!/bin/bash

echo "Esperando a que Kafka esté disponible..."

# Esperar hasta que Kafka esté disponible
until nc -z kafka 9092; do
  echo "Esperando a Kafka..."
  sleep 1
done

echo "Kafka está disponible. Iniciando la aplicación..."
