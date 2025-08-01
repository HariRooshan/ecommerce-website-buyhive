<?php
session_start();
include 'db.php';

if (!isset($_SESSION['user']) || $_SESSION['role'] !== 'admin') {
    header('Location: login.php');
    exit();
}

// Handle add, edit, delete actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['add'])) {
        $name = $_POST['name'];
        $brand = $_POST['brand'];
        $price = (float)$_POST['price'];
        $quantity = (int)$_POST['quantity'];
        $image = '';
        if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
            $imgName = time() . '_' . basename($_FILES['image']['name']);
            $target = 'images/' . $imgName;
            if (move_uploaded_file($_FILES['image']['tmp_name'], $target)) {
                $image = $imgName;
            }
        }
        $conn->query("INSERT INTO products (name, brand, price, quantity, image) VALUES ('$name', '$brand', $price, $quantity, '$image')");
    }
    if (isset($_POST['edit'])) {
        $id = (int)$_POST['id'];
        $name = $_POST['name'];
        $brand = $_POST['brand'];
        $price = (float)$_POST['price'];
        $quantity = (int)$_POST['quantity'];
        $image = $_POST['current_image'];
        if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
            $imgName = time() . '_' . basename($_FILES['image']['name']);
            $target = 'images/' . $imgName;
            if (move_uploaded_file($_FILES['image']['tmp_name'], $target)) {
                $image = $imgName;
            }
        }
        $conn->query("UPDATE products SET name='$name', brand='$brand', price=$price, quantity=$quantity, image='$image' WHERE id=$id");
    }
    if (isset($_POST['delete'])) {
        $id = (int)$_POST['id'];
        $conn->query("DELETE FROM products WHERE id=$id");
    }
    header('Location: admin_products.php');
    exit();
}

$res = $conn->query("SELECT * FROM products");
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin - Manage Products</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5 position-relative">
    <a href="index.php" class="btn btn-warning position-absolute top-0 end-0 mt-2 me-2">Back to Shop</a>
    <h2 class="text-center mb-4">🛠️ Admin: Manage Products</h2>
    <div class="my-5 text-center">
        <button class="btn btn-success px-5 py-2" data-bs-toggle="modal" data-bs-target="#addProductModal">Add New Product</button>
    </div>

    <!-- Add Product Modal -->
    <div class="modal fade" id="addProductModal" tabindex="-1" aria-labelledby="addProductModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <form method="POST" enctype="multipart/form-data">
            <div class="modal-header">
              <h5 class="modal-title" id="addProductModalLabel">Add New Product</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Name <span class="text-danger">*</span></label>
                <input type="text" name="name" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Brand <span class="text-danger">*</span></label>
                <input type="text" name="brand" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Price <span class="text-danger">*</span></label>
                <input type="number" name="price" class="form-control" min="0" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Quantity <span class="text-danger">*</span></label>
                <input type="number" name="quantity" class="form-control" min="0" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Product Image <span class="text-danger">*</span></label>
                <input type="file" name="image" class="form-control" accept="image/*" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-success" name="add">Add</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Edit Product Modal (dynamic) -->
    <div class="modal fade" id="editProductModal" tabindex="-1" aria-labelledby="editProductModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <form method="POST" enctype="multipart/form-data" id="editProductForm">
            <div class="modal-header">
              <h5 class="modal-title" id="editProductModalLabel">Edit Product</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <input type="hidden" name="id" id="edit-id">
              <input type="hidden" name="current_image" id="edit-current-image">
              <div class="mb-3">
                <label class="form-label">Name <span class="text-danger">*</span></label>
                <input type="text" name="name" id="edit-name" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Brand <span class="text-danger">*</span></label>
                <input type="text" name="brand" id="edit-brand" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Price <span class="text-danger">*</span></label>
                <input type="number" name="price" id="edit-price" class="form-control" min="0" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Quantity <span class="text-danger">*</span></label>
                <input type="number" name="quantity" id="edit-quantity" class="form-control" min="0" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Product Image</label>
                <div id="edit-image-preview" class="mb-2"></div>
                <input type="file" name="image" class="form-control" accept="image/*">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Discard</button>
              <button type="submit" class="btn btn-success" name="edit">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <table class="table table-bordered align-middle text-center">
        <thead class="table-light">
            <tr>
                <th>Name</th>
                <th>Brand</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Image</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
        <?php while ($row = $res->fetch_assoc()): ?>
            <tr<?= ($row['quantity'] < 5 ? ' class="table-warning"' : '') ?>>
                <td><?= htmlspecialchars($row['name']) ?></td>
                <td><?= htmlspecialchars($row['brand']) ?></td>
                <td><?= $row['price'] ?></td>
                <td>
                    <?= $row['quantity'] ?>
                    <?php if ($row['quantity'] == 0): ?>
                        <span class="badge bg-danger mt-1">OUT OF STOCK!</span>
                    <?php elseif ($row['quantity'] < 10): ?>
                        <span class="badge bg-warning mt-1">Low Stock!</span>
                    <?php endif; ?>
                </td>
                <td>
                    <?php if (!empty($row['image'])): ?>
                        <img src="images/<?= htmlspecialchars($row['image']) ?>" alt="Product Image" style="width:50px;height:50px;object-fit:cover;" class="me-2 mb-1 rounded">
                    <?php endif; ?>
                </td>
                <td>
                    <button 
                        class="btn btn-primary btn-sm edit-btn"
                        data-bs-toggle="modal"
                        data-bs-target="#editProductModal"
                        data-id="<?= $row['id'] ?>"
                        data-name="<?= htmlspecialchars($row['name']) ?>"
                        data-brand="<?= htmlspecialchars($row['brand']) ?>"
                        data-price="<?= $row['price'] ?>"
                        data-quantity="<?= $row['quantity'] ?>"
                        data-image="<?= htmlspecialchars($row['image']) ?>"
                    >Edit</button>
                    <form method="POST" style="display:inline;">
                        <input type="hidden" name="id" value="<?= $row['id'] ?>">
                        <button class="btn btn-danger btn-sm" name="delete" onclick="return confirm('Delete this product?')">Remove</button>
                    </form>
                </td>
            </tr>
        <?php endwhile; ?>
        </tbody>
    </table>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
document.querySelectorAll('.edit-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        document.getElementById('edit-id').value = btn.getAttribute('data-id');
        document.getElementById('edit-name').value = btn.getAttribute('data-name');
        document.getElementById('edit-brand').value = btn.getAttribute('data-brand');
        document.getElementById('edit-price').value = btn.getAttribute('data-price');
        document.getElementById('edit-quantity').value = btn.getAttribute('data-quantity');
        document.getElementById('edit-current-image').value = btn.getAttribute('data-image');
        var img = btn.getAttribute('data-image');
        var preview = document.getElementById('edit-image-preview');
        preview.innerHTML = img ? '<img src="images/' + img + '" style="width:50px;height:50px;object-fit:cover;" class="rounded">' : '';
    });
});
</script>
</body>