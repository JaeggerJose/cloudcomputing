<?php
// getJobs.php
$jobFile = '/share/job.txt';
if (file_exists($jobFile)) {
    echo file_get_contents($jobFile);
} else {
    echo "Job file not found.";
}
?>