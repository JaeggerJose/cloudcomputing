<?php
if (isset($_GET['jobName'])) {
    $jobName = $_GET['jobName'];
    // 实现删除逻辑，例如删除文件或数据库条目
    // echo "删除成功：" . $jobName;
    $directoryPath = "/share/input/" . $jobName;
    $directoryPathOut = "/share/output/" . $jobName;
    if (is_dir($directoryPath)) {
        array_map('unlink', glob("$directoryPath/*.*"));
        rmdir($directoryPath);
        array_map('unlink', glob("$directoryPathOut/*.*"));
        rmdir($directoryPathOut);
        echo "已删除: " . $jobName;
    } else {
        echo "找不到: " . $jobName;
    }
}
?>
