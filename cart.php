<?php
session_start();
include 'db.php';

if (!isset($_SESSION['cart'])) $_SESSION['cart'] = [];

function fetchCartItems($conn) {
    $items = [];
    foreach ($_SESSION['cart'] as $id => $qty) {
        $res = $conn->query("SELECT * FROM products WHERE id = $id");
        if ($row = $res->fetch_assoc()) {
            $row['qty'] = $qty;
            $items[] = $row;
        }
    }
    return $items;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Your Cart</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <style>
        .qty-btn {
            width: 35px;
            height: 35px;
            font-weight: bold;
        }
    </style>
</head>
<body>
<div class="container mt-4">
    <h2 class="text-center">🛒 Shopping Cart</h2>
    <?php if (isset($_GET['error'])): ?>
        <div class="alert alert-danger text-center"><?= htmlspecialchars($_GET['error']) ?></div>
    <?php endif; ?>
    <?php if (empty($_SESSION['cart'])): ?>
        <div class="alert alert-info">Your cart is empty.</div>
        <div class="text-center mt-3">
            <a href="index.php" class="btn btn-primary py-2">Go Back to Shopping</a>
        </div>
    <?php else: ?>
        <table class="table table-bordered align-middle text-center">
            <thead>
            <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
                <th>Action</th>
            </tr>
            </thead>
            <tbody id="cartBody">
            <?php
            $grandTotal = 0;
            foreach (fetchCartItems($conn) as $item):
                $total = $item['price'] * $item['qty'];
                $grandTotal += $total;
            ?>
                <tr data-id="<?= $item['id'] ?>">
                    <td><?= $item['name'] ?></td>
                    <td class="d-flex justify-content-center align-items-center gap-2">
                        <button class="btn btn-secondary qty-btn minus">–</button>
                        <input type="text" value="<?= $item['qty'] ?>" readonly class="form-control text-center" style="width: 60px;">
                        <button class="btn btn-secondary qty-btn plus">+</button>
                    </td>
                    <td>₹<?= $item['price'] ?></td>
                    <td class="line-total">₹<?= $total ?></td>
                    <td>
                        <button class="btn btn-danger remove-item">Remove</button>
                    </td>
                </tr>
            <?php endforeach; ?>
            </tbody>
        </table>
        <h4 id="grandTotal">Total: ₹<?= $grandTotal ?></h4>
        <div class="d-flex justify-content-between align-items-center mt-4">
            <a href="index.php" class="btn btn-primary py-2 d-flex align-items-center gap-2">
                &#x2B05; Go Back to Shopping
            </a>
            <a href="payment.php" class="btn btn-success py-2 d-flex align-items-center gap-2">
                Checkout &#x27A1;
            </a>
        </div>
    <?php endif; ?>
</div>

<script>
document.querySelectorAll(".qty-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const row = btn.closest("tr");
        const id = row.dataset.id;
        const qtyInput = row.querySelector("input");
        let qty = parseInt(qtyInput.value);

        if (btn.classList.contains("plus")) qty++;
        if (btn.classList.contains("minus")) qty = Math.max(1, qty - 1);

        fetch("update_cart.php", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `id=${id}&qty=${qty}`
        })
        .then(res => res.json())
        .then(data => {
            qtyInput.value = data.qty;
            row.querySelector(".line-total").textContent = "₹" + data.lineTotal;
            document.getElementById("grandTotal").textContent = "Total: ₹" + data.grandTotal;
        });
    });
});

document.querySelectorAll(".remove-item").forEach(btn => {
    btn.addEventListener("click", () => {
        const row = btn.closest("tr");
        const id = row.dataset.id;

        fetch("remove_item.php", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `id=${id}`
        })
        .then(() => location.reload());
    });
});
</script>
</body>
</html>