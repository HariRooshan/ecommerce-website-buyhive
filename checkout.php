<?php
session_start();
if (!isset($_SESSION['user'])) {
    header('Location: login.php');
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
<title>Checkout</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5 text-center">
    <h2>✅ Order Successful!</h2>
    <p>Thank you for shopping with us.</p>
    <a href="index.php" class="btn btn-primary">Continue Shopping</a>
</div>
<!-- Cart is cleared after successful payment in payment.php -->
</body>
</html>