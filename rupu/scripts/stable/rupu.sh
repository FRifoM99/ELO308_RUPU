#!/bin/bash
# Activar el entorno virtual
source rupu/bin/activate

# Navegar al directorio de scripts
cd rupu/scripts/stable

# Iniciar el demonio pigpiod
sudo pigpiod

# Ejecutar el script de Python
python main.py
