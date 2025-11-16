@echo off
setlocal

:: Ruta al ejecutable de 7-Zip
set ZIP="C:\Program Files\7-Zip\7z.exe"

:: Comprobar si 7-Zip está instalado
if not exist %ZIP% (
    echo ERROR: No se encontró 7-Zip en %ZIP%
    echo Por favor instala 7-Zip o ajusta la ruta en el script.
    pause
    exit /b
)

:: Nombre del archivo ZIP
set ZIPFILE=dunamar.zip

:: Archivos y carpetas a comprimir
set FILES=app.py config.py models.py requirements.txt templates static dockerfile .dockerignore Procfile

:: Comprimir usando 7-Zip
%ZIP% a %ZIPFILE% %FILES%

echo Archivos comprimidos en %ZIPFILE%
pause

del dunamar.zip
