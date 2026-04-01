# Configuración del Envío de Correos

## Requisitos

1. Instalar las nuevas dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de Variables de Entorno

1. Crear un archivo `.env` en la carpeta `src/` copiando de `.env.example`:
```bash
cp .env.example .env
```

2. Editar el archivo `.env` con tus credenciales:

### Usando Gmail

Si usas Gmail, sigue estos pasos:

1. **Habilitar autenticación de dos factores** en tu cuenta de Google
2. **Generar contraseña de aplicación**:
   - Ir a https://myaccount.google.com/apppasswords
   - Seleccionar "Correo" y "Windows"
   - Gmail generará una contraseña de 16 caracteres
   - Copiar esa contraseña en `MAIL_PASSWORD`

3. Configurar en `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-16-caracteres
MAIL_DEFAULT_SENDER=tu-email@gmail.com
```

### Usando otro servidor SMTP

Si usas otro proveedor, consulta su documentación SMTP y actualiza correspondientemente:
- MAIL_SERVER: servidor SMTP del proveedor
- MAIL_PORT: puerto SMTP (típicamente 587 o 465)
- MAIL_USE_TLS: True para port 587, False para port 465
- MAIL_USERNAME: tu usuario/email
- MAIL_PASSWORD: tu contraseña

## Verificar que funcione

1. Instalar python-dotenv (opcional pero recomendado):
```bash
pip install python-dotenv
```

2. En la carpeta `src/`, ejecutar:
```bash
python app.py
```

3. Abre http://localhost:5000 y prueba el formulario

## Notas de Seguridad

- **NUNCA** commits el archivo `.env` con credenciales reales
- El archivo `.env` está generalmente listado en `.gitignore`
- Usa variables de entorno en producción en lugar de archivos locales
- Para Gmail, no uses tu contraseña real, usa la contraseña de aplicación
