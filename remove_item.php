<?php
session_start();
$id = (int)$_POST['id'];
unset($_SESSION['cart'][$id]);
echo "removed";
?>