#!/bin/bash

# Verificar que Docker esté disponible
if ! command -v docker &> /dev/null; then
    echo "Docker no está instalado. Instálalo desde https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "Construyendo imagen de Docker..."
docker build -t py2exe .

echo "Ejecutando contenedor para generar el .exe..."
docker run --rm -v "$(pwd)":/src py2exe

echo "El ejecutable está en: dist/main.exe"