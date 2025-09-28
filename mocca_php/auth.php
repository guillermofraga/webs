<?php
session_start();
require 'db.php';

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user'] = $user['username'];
        header('Location: admin/dashboard.php');
        exit;
    } else {
        echo "<p style='color:red; text-align:center;'>Usuario o contraseña incorrectos</p>";
        echo "<p style='text-align:center;'><a href='login.php'>Volver</a></p>";
    }
}
?>
