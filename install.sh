#!/bin/bash

echo "🚀 Instalando dependencias..."

sudo apt update && sudo apt upgrade -y

# Instalar dependencias de Python
sudo apt install -y python3-pip python3-flask python3-picamera2 python3-opencv

# Reiniciar módulos de cámara si es necesario
sudo modprobe bcm2835-v4l2

# Crear directorio para el proyecto
mkdir -p ~/rover-control
cd ~/rover-control || exit

echo "✅ Configuración completada."
echo ""
echo "🔧 Para iniciar:"
echo "1. Asegúrate de tener las cámaras configuradas."
echo "2. Ejecuta: python3 web_interface.py"