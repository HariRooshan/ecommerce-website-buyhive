<?php
session_start();
include 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    $confirm = trim($_POST['confirm_password']);
    $role = isset($_POST['role']) ? $_POST['role'] : 'user';

    if ($password !== $confirm) {
        header("Location: register.php?error=Passwords do not match");
        exit();
    }

    $hashed = hash('sha256', $password);

    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        header("Location: register.php?error=Username already exists");
        exit();
    }

    $stmt = $conn->prepare("INSERT INTO users (username, password, role) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $username, $hashed, $role);
    if ($stmt->execute()) {
        header("Location: register.php?success=1");
    } else {
        header("Location: register.php?error=Something went wrong");
    }
    exit();
}
?>