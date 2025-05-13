# Imagen base con PyInstaller + Wine (para generar .exe desde Linux/macOS)
FROM --platform=linux/amd64 cdrx/pyinstaller-windows

# Define el directorio de trabajo dentro del contenedor
WORKDIR /src

# Copiar todo el contenido del proyecto (main.py, inc/, raw_data/, etc.)
COPY . /src

# Instalar dependencias del proyecto si hay requirements.txt
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir -r requirements.txt; \
    fi

# Compilar el ejecutable .exe incluyendo la carpeta raw_data
RUN pyinstaller --onefile --add-data "Raw data;Raw data" main.py