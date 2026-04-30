from flask import Blueprint, request

uploads_bp = Blueprint('uploads', __name__, url_prefix='/uploads')

@uploads_bp.route("/image", methods=['POST'])
def image():
    try:
        if 'image' not in request.files:
            return "No se ha proporcionado una imagen", 400
        
        image = request.files['image']
        # Aquí puedes guardar la imagen en el servidor o en un servicio de almacenamiento
        # Por ejemplo, podrías usar Amazon S3, Google Cloud Storage, etc.
        
        # Para este ejemplo, simplemente devolveremos un mensaje de éxito
        return "Imagen subida exitosamente", 200
    except Exception as e:
        return f"Error al subir la imagen: {str(e)}", 500