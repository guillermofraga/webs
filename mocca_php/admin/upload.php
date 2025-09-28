<?php
session_start();
require_once '../db.php';

if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES['image'])) {
    $file = $_FILES['image'];
    $targetDir = "../uploads/";
    $filename = basename($file["name"]);
    $targetFile = $targetDir . $filename;

    $allowed = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
    $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));

    if (!in_array($ext, $allowed)) {
        die("Tipo de archivo no permitido.");
    }

    if (move_uploaded_file($file["tmp_name"], $targetFile)) {
        // Guardar en la base de datos
        $stmt = $pdo->prepare("INSERT INTO gallery_images (filename) VALUES (?)");
        $stmt->execute([$filename]);
        header("Location: dashboard.php");
    } else {
        die("Error al subir la imagen.");
    }
}
?>
