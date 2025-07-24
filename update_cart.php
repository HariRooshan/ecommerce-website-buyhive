<?php
session_start();
include 'db.php';

$id = (int)$_POST['id'];
$qty = max(1, (int)$_POST['qty']);

$_SESSION['cart'][$id] = $qty;

$res = $conn->query("SELECT price FROM products WHERE id = $id");
$price = $res->fetch_assoc()['price'];
$lineTotal = $price * $qty;

$grandTotal = 0;
foreach ($_SESSION['cart'] as $pid => $pq) {
    $res = $conn->query("SELECT price FROM products WHERE id = $pid");
    if ($r = $res->fetch_assoc()) {
        $grandTotal += $r['price'] * $pq;
    }
}

echo json_encode([
    "qty" => $qty,
    "lineTotal" => $lineTotal,
    "grandTotal" => $grandTotal
]);
?>