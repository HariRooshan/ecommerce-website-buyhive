<?php
session_start();
include 'db.php';

if (!isset($_SESSION['cart'])) {
    $_SESSION['cart'] = [];
}

$loginMessage = false;
if (isset($_SESSION['login_success'])) {
    $loginMessage = true;
    unset($_SESSION['login_success']);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['product_id'])) {
    $id = (int)$_POST['product_id'];
    $qty = max(1, (int)$_POST['quantity']);

    if (isset($_SESSION['cart'][$id])) {
        $_SESSION['cart'][$id] += $qty;
    } else {
        $_SESSION['cart'][$id] = $qty;
    }

    header("Location: index.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
  <title>Product Catalog</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-4">
  <?php if ($loginMessage): ?>
    <div class="alert alert-success alert-dismissible fade show" role="alert">
      ✅ Login successful. Welcome back!
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
  <?php endif; ?>

  <div class="d-flex justify-content-between align-items-center mb-3">
    <h2>🛍️ Product Catalog</h2>
    <div class="d-flex gap-2">
      <a href="cart.php" class="btn btn-outline-primary">View Cart (<?= array_sum($_SESSION['cart']) ?>)</a>
      <?php if (isset($_SESSION['role']) && $_SESSION['role'] === 'admin'): ?>
        <a href="admin_products.php" class="btn btn-warning">Go to Admin Dashboard</a>
      <?php endif; ?>
      <a href="logout.php" class="btn btn-outline-danger">Logout</a>
    </div>
  </div>
  <div class="row">
    <?php
    $res = $conn->query("SELECT * FROM products");
    while ($row = $res->fetch_assoc()):
        $isOutOfStock = ($row['quantity'] <= 0);
    ?>
    <div class="col-md-3 mb-4">
      <div class="card h-100">
        <img src="images/<?= $row['image'] ?>" class="card-img-top" style="height: 350px; object-fit: cover;">
        <div class="card-body">
          <h5 class="card-title"><?= $row['name'] ?></h5>
          <p class="card-text">
            Brand: <?= $row['brand'] ?><br>
            Price: ₹<?= $row['price'] ?><br>
            <strong>Available: <?= $row['quantity'] ?></strong>
            <?php if ($isOutOfStock): ?>
              <span class="badge bg-danger ms-2">Out of Stock</span>
            <?php endif; ?>
          </p>
          <form action="index.php" method="POST">
            <input type="hidden" name="product_id" value="<?= $row['id'] ?>">
            <div class="input-group">
              <input type="number" name="quantity" value="1" min="1" max="<?= $row['quantity'] ?>" class="form-control" <?= $isOutOfStock ? 'disabled' : '' ?>>
              <button class="btn btn-primary" <?= $isOutOfStock ? 'disabled' : '' ?>>Add to Cart</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <?php endwhile; ?>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>