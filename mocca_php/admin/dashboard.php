<?php
session_start();
require_once '../db.php';

if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

// Obtener imágenes de la base de datos
$stmt = $pdo->query("SELECT * FROM gallery_images ORDER BY uploaded_at DESC");
$images = $stmt->fetchAll();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>Panel - Galería</title>
    <link rel="stylesheet" href="https://cdn.tailwindcss.com">
</head>
<body class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-5xl mx-auto bg-white p-6 rounded shadow">
        <h1 class="text-2xl font-bold mb-4">Galería - Administrar imágenes</h1>

        <!-- Formulario de subida -->
        <form action="upload.php" method="POST" enctype="multipart/form-data" class="mb-8">
            <label class="block mb-2 font-medium">Subir nueva imagen:</label>
            <input type="file" name="image" required accept="image/*" class="mb-4">
            <button type="submit" class="bg-primary text-white px-4 py-2 rounded hover:bg-opacity-90">Subir</button>
        </form>

        <!-- Mostrar imágenes -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <?php foreach ($images as $img): ?>
                <div class="relative group">
                    <img src="../uploads/<?php echo htmlspecialchars($img['filename']); ?>" class="rounded shadow" style="width: 300px; height: auto;">
                    <form action="delete.php" method="POST" onsubmit="return confirm('¿Eliminar esta imagen?');" class="absolute top-2 right-2 hidden group-hover:block">
                        <input type="hidden" name="id" value="<?php echo $img['id']; ?>">
                        <button type="submit" class="bg-red-600 text-white px-2 py-1 rounded text-sm">Eliminar</button>
                    </form>
                </div>
            <?php endforeach; ?>
        </div>
                
        <a href="../logout.php" class="block mt-8 text-red-500 font-medium hover:underline">Cerrar sesión</a>
    </div>
</body>
</html>
