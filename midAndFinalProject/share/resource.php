<?php

// Function to parse CPU and memory usage
function parseSystemUsage($output) {
    $data = [];

    // Regex to find CPU usage
    if (preg_match('/%Cpu\(s\):\s+(\d+.\d+)\s+us,\s+(\d+.\d+)\s+sy/', $output, $cpuMatches)) {
        $data['CPU Usage'] = [
            'User' => $cpuMatches[1],
            'System' => $cpuMatches[2]
        ];
    }

    // Regex to find Memory usage
    if (preg_match('/MiB Mem :\s+[\d.]+ total,\s+[\d.]+ free,\s+([\d.]+) used/', $output, $memMatches)) {
        $data['Memory Used'] = $memMatches[1] . ' MiB';
    }

    return $data;
}

// File paths
$files = [
    '/share/resource/cmp1.txt',
    '/share/resource/cmp2.txt',
    '/share/resource/cmp3.txt'
];

// Loop through each file and parse the contents
foreach ($files as $file) {
    if (file_exists($file)) {
        // Read the contents of the file
        $output = file_get_contents($file);
        // Parse the output
        $parsedData = parseSystemUsage($output);
        echo "Data from $file:\n";
        print_r($parsedData);
        echo "\n";
    } else {
        echo "File $file does not exist.\n";
    }
}

?>
