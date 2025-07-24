<?php
session_start();
include 'db.php';

// if (!isset($_SESSION['user']) || $_SESSION['role'] !== 'user') {
//     header('Location: login.php');
//     exit();
// }

if (empty($_SESSION['cart'])) {
    header('Location: cart.php');
    exit();
}

// Fetch cart items and check stock
$cartItems = [];
$insufficient = [];
foreach ($_SESSION['cart'] as $id => $qty) {
    $res = $conn->query("SELECT * FROM products WHERE id = $id");
    if ($row = $res->fetch_assoc()) {
        if ($qty > $row['quantity']) {
            $insufficient[] = $row['name'] . " (Available: " . $row['quantity'] . ")";
        }
        $cartItems[] = $row + ['qty' => $qty];
    }
}

if (!empty($insufficient)) {
    $msg = "Insufficient stock for: " . implode(', ', $insufficient);
    header("Location: cart.php?error=" . urlencode($msg));
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['pay'])) {
    // Dummy payment logic
    // Update product quantities
    foreach ($cartItems as $item) {
        $newQty = $item['quantity'] - $item['qty'];
        $conn->query("UPDATE products SET quantity = $newQty WHERE id = {$item['id']}");
    }
    $_SESSION['cart'] = [];
    header('Location: checkout.php');
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Payment</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-7">
            <div class="card shadow-lg border-0 mb-4">
                <div class="card-header bg-gradient bg-primary text-white text-center">
                    <h2 class="mb-0">💳 Payment Summary</h2>
                </div>
                <div class="card-body">
                    <table class="table table-striped table-bordered align-middle text-center mb-4">
                        <thead class="table-light">
                            <tr>
                                <th>Product</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                        <?php
                        $grandTotal = 0;
                        foreach ($cartItems as $item):
                            $lineTotal = $item['price'] * $item['qty'];
                            $grandTotal += $lineTotal;
                        ?>
                            <tr>
                                <td><?= htmlspecialchars($item['name']) ?></td>
                                <td><?= $item['qty'] ?></td>
                                <td>₹<?= $item['price'] ?></td>
                                <td>₹<?= $lineTotal ?></td>
                            </tr>
                        <?php endforeach; ?>
                        </tbody>
                    </table>
                    <div class="text-end mb-4">
                        <span class="fs-4 fw-bold text-success">Total Amount: ₹<?= $grandTotal ?></span>
                    </div>
                    <form method="POST" class="d-flex flex-column gap-3 align-items-center">
                        <button class="btn btn-success w-100 py-2 fs-5" name="pay">Pay & Complete Order</button>
                        <a href="cart.php" class="btn btn-secondary w-100 py-2 fs-5">Go Back to Cart</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
