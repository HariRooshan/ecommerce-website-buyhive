<?php
session_start();

$max_users = 3;
$file = "active_users.txt";

// Initialize file if it doesn’t exist
if (!file_exists($file)) {
    file_put_contents($file, 0);
}

// Read current user count
$count = (int)file_get_contents($file);

// If user not already counted
if (!isset($_SESSION['active'])) {
    if ($count > $max_users) {
        die("Maximum user limit reached. Try again later.");
    } else {
        $_SESSION['active'] = true;
        $count++;
        file_put_contents($file, $count);
    }
}

// When session ends, decrease counter
register_shutdown_function(function() use ($file) {
    if (isset($_SESSION['active']) && $_SESSION['active']) {
        $count = (int)file_get_contents($file);
        $count = max(0, $count - 1);
        file_put_contents($file, $count);
        $_SESSION['active'] = false;
    }
});
