<?php
session_start();

// concurrent_users.php logic for decrement
$file = "active_users.txt";
if (isset($_SESSION['active'])) {
    $count = (int)file_get_contents($file);
    $count = max(0, $count - 1);
    file_put_contents($file, $count);
    unset($_SESSION['active']);
}

session_destroy();
header("Location: login.php");
exit();
?>
