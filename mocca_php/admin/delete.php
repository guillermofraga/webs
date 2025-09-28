<?php
session_start();
require_once '../db.php';

if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST['id'])) {
    $id = (int)$_POST['id'];

    // Obtener filename
    $stmt = $pdo->prepare("SELECT filename FROM gallery_images WHERE id = ?");
    $stmt->execute([$id]);
    $img = $stmt->fetch();

    if ($img) {
        // Borrar archivo físico
        $filepath = "../uploads/" . $img['filename'];
        if (file_exists($filepath)) {
            unlink($filepath);
        }

        // Borrar de la base de datos
        $stmt = $pdo->prepare("DELETE FROM gallery_images WHERE id = ?");
        $stmt->execute([$id]);
    }

    header("Location: dashboard.php");
}
?>
