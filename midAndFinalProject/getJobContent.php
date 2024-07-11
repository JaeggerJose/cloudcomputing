<?php

$filePath = '/share/123124job.txt';

if (file_exists($filePath)) {
    echo file_get_contents($filePath);
} else {
    echo "File not found.";
}

?>