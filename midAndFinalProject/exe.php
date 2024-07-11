<?php
// 確保模型名稱
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['file']) && isset($_POST['model'])) {
    // 目錄
    $uploadRoot = '/share/input/';

    $fileName = $_FILES['file']['name'];
    $fileTmpPath = $_FILES['file']['tmp_name'];

    $baseName = pathinfo($fileName, PATHINFO_FILENAME);

    // 處理
    $safeBaseName = preg_replace('/[^a-zA-Z0-9_-]/', '_', $baseName);
    $timestamp = time();
    $fileName = $safeBaseName . '_' . $timestamp . '.' . pathinfo($fileName, PATHINFO_EXTENSION);
    // echo $fileName;
    // 文件夾
    $targetDir = $uploadRoot . $safeBaseName . '_' . $timestamp;

    // 如果沒有 創建
    if (!file_exists($targetDir)) {
        mkdir($targetDir, 0777, true);
    }


    $targetFilePath = $targetDir . '/' . $fileName;

 
    if (move_uploaded_file($fileTmpPath, $targetFilePath)) {
    
        $model = $_POST['model'];


        $infoContent = $fileName . " " . $model;
        file_put_contents($targetDir . '/info.txt', $infoContent);

        // echo "上傳成功";
        header('Location: upload.php?status=success'); 
    } else {
        header('Location: upload.php?status=failure');
        // echo "上傳失敗。";
    }
} else {
    header('Location: upload.php?status=nofile');
    // echo "必須上傳模型和音檔";
}
?>
