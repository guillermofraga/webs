<?php
session_start();
if (isset($_SESSION['user'])) {
    header('Location: admin/dashboard.php');
    exit;
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login - Mocca</title>
    <link rel="stylesheet" href="https://cdn.tailwindcss.com">
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <form action="auth.php" method="POST" class="bg-white p-6 rounded-lg shadow-md w-full max-w-sm">
        <h2 class="text-2xl font-bold mb-4 text-center text-primary">Iniciar sesión</h2>
        <label class="block mb-2">Usuario</label>
        <input type="text" name="username" required class="w-full px-3 py-2 mb-4 border rounded">
        <label class="block mb-2">Contraseña</label>
        <input type="password" name="password" required class="w-full px-3 py-2 mb-4 border rounded">
        <button type="submit" class="bg-primary text-white py-2 px-4 rounded w-full hover:bg-opacity-90">Entrar</button>
    </form>
</body>
</html>
