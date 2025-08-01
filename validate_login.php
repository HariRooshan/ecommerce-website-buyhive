<?php
session_start();
include 'db.php';

// Restrict login attempts
if (!isset($_SESSION['login_attempts'])) {
    $_SESSION['login_attempts'] = 0;
}
$max_attempts = 5;

// Check for lockout timer
if (isset($_SESSION['lockout_time']) && time() < $_SESSION['lockout_time']) {
    $remaining = $_SESSION['lockout_time'] - time();
    header("Location: login.php?error=Too many failed attempts. Please wait {$remaining} seconds before trying again.");
    exit();
}

if ($_SESSION['login_attempts'] >= $max_attempts) {
    $_SESSION['lockout_time'] = time() + 60; // 1 minute lockout
    $_SESSION['login_attempts'] = 0;
    $remaining = 60;
    header("Location: login.php?error=Too many failed attempts. Please wait {$remaining} seconds before trying again.");
    exit();
}

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

    $_SESSION['login_attempts'] += 1; // Increment on failure
    if ($_SESSION['login_attempts'] >= $max_attempts) {
        $_SESSION['lockout_time'] = time() + 60;
        $_SESSION['login_attempts'] = 0;
        header("Location: login.php?error=Too many failed attempts. Please try again later.");
    } else {
        header("Location: login.php?error=Invalid username or password");
    }
    exit();
}
?>