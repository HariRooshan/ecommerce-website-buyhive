<?php
session_start();
include 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    $role = isset($_POST['role']) ? $_POST['role'] : 'user';

    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND role = ?");
    $stmt->bind_param("ss", $username, $role);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        if (hash('sha256', $password) === $row['password']) {
            $_SESSION['user'] = $row['username'];
            $_SESSION['role'] = $row['role'];
            $_SESSION['login_success'] = true;
            if ($row['role'] === 'admin') {
                header("Location: admin_products.php");
            } else {
                header("Location: index.php");
            }
            exit();
        }
    }

    header("Location: login.php?error=Invalid username or password");
    exit();
}
?>