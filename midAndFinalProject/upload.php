<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <script src="script.js" defer></script>
    <title>Super High Class AI Voice Generator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel&display=swap" rel="stylesheet">
</head>
<body>

<header style="
    display: flex;
    justify-content: center;
    align-items: center;">
    <h1 style="font-family: cursive; font-size: -webkit-xxx-large;">Super High Class AI Voice Generator</h1>
	<img src="icon.webp" alt="Site Icon" style="height: 75px; padding: 15px; border-radius: 50%;">
</header>

<nav>
    <a href="#" onclick="showPage('upload')">音檔上傳</a>
    <a href="#" onclick="showPage('progress')">進度處理</a>
    <a href="#" onclick="showPage('admin')">系統管理</a>
</nav>

<div class="container" id="uploadPage">
    <h2>音檔上傳專區</h2>
    <form action="exe.php" method="post" enctype="multipart/form-data" onsubmit="return checkFiles();">
        <input type="file" id="fileElem" name="file" accept=".wav" multiple accept="audio/*" style="display:none" onchange="handleFiles(this.files)">
        <button type="button" onclick="document.getElementById('fileElem').click()" class="button">選擇檔案</button>
        <div id="drop-area">
            <p id="fileInfo">或將檔案拖到這裡</p>
        </div>
        <select id="modelSelect" name="model" class="model-select" onfocus="this.size=5;" onblur="this.size=1;" onchange="this.size=1; this.blur();">
            <option disabled selected>模型選擇</option>
            <?php
            $models = scandir('/share/model');
            foreach ($models as $model) {
                if ($model != "." && $model != "..") {
                    echo "<option value='$model'>$model</option>";
                }
            }
            ?>
        </select>
        <button type="submit" class="button submit-button">上傳音檔</button>
    </form>
</div>

<div class="container hidden" id="progressPage">
    <h2>進度處理 lis</h2>
    <h3>每分鐘更新一次</h3>
    <?php
        $jobFile = '/share/job.txt';
        echo "<div class='scrollTableContainer'><table >
        <tr>
            <th>檔案名稱</th>
            <th>進度</th>
            <th>下載</th>
            <th>操作</th>
        </tr>";
        if (file_exists($jobFile)) {
            $jobs = file($jobFile);
            foreach ($jobs as $job) {
                $jobInfo = explode(" ", trim($job)); // 確保去掉行尾的換行符
                echo "<tr>";
                if (file_exists('/share/output/'.$jobInfo[0])){
                    echo "<td>" . htmlspecialchars($jobInfo[0]) . "</td>"; // 避免XSS攻擊
                    echo "<td>" . htmlspecialchars($jobInfo[1]) . "</td>";
                    if (strpos($jobInfo[1], 'complete') !== false){
                        $audioFile = '/share/output/'.$jobInfo[0]. "/output.wav";
                        echo "<td><audio controls><source src=\"$audioFile\" type=\"audio/wav\">Your browser does not support the audio element.</audio></td>";
                        echo "<td>已完成</td>";
                    } 
                    else {
                        echo "<td>計算等待中</td>";
                        echo "<td><button onclick=\"deleteJob('". htmlspecialchars($jobInfo[0]) ."')\">刪除</button></td>";
                    }
                }
                echo "</tr>";
            }
        }
        echo "</table></div>";
    ?>
</div>

<div class="container hidden" id="adminPage">
    <!-- info from /share/resource and in this folder have cmp1.txt cmp2.txt cmp3.txt have to show sepraterate and its info is from cmd top -bn 1 -i -c
have to show all of them-->
    <h2>節點資源</h2>
    <div class="task-box">
        <table>
            <tr>
                <th>節點</th>
                <!-- <th>數值</th> -->
                <th>任務數</th>
                <th>cpu使用</th>
                <th>記憶體使用</th>
            </tr>
            <?php
            $resourceDir = '/share/resource';
            if (is_dir($resourceDir)) {
                $files = scandir($resourceDir);
                foreach ($files as $file) {
                    if ($file != '.' && $file != '..') {
                        $content = file_get_contents($resourceDir . '/' . $file);
                        $lines = explode("\n", $content);
                        echo "<tr>";
                        echo "<td>" . pathinfo($file, PATHINFO_FILENAME) . "</td>";
                        // echo "<td>" . $lines[0] . "</td>";
                        echo "<td>" . $lines[1] . "</td>";
                        echo "<td>" . $lines[2] . "</td>";
                        echo "<td>" . $lines[3] . "</td>";
                        echo "</tr>";
                    }
                }
            }
            ?>
        </table>
        
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const status = urlParams.get('status');
    if (status) {
        let message = '';
        if (status === 'success') {
            message = '音檔上傳成功！';
        } else if (status === 'failure') {
            message = '文件上傳失敗，請重式。';
        } else if (status === 'nofile') {
            message = '没有上傳音檔或是模型。';
        }
        alert(message);
    }
    history.pushState(null, '', location.href.split('?')[0]);
});
function showPage(page) {
    var pages = ['upload', 'progress', 'admin'];
    pages.forEach(function(item) {
        var pageElement = document.getElementById(item + 'Page');
        if (item === page) {
            pageElement.classList.remove('hidden');
        } else {
            pageElement.classList.add('hidden');
        }
    });
}

function deleteJob(jobName) {
    fetch(`deleteJob.php?jobName=${jobName}`)
    .then(response => response.text())
    .then(data => {
        alert(data);
        location.reload(); // 刷新页面以更新列表
    })
    .catch(error => console.error('Error:', error));
}
</script>
<div class="footer-dark">
        <footer>
            <div class="container">
                <div class="row">
                    <div class="col-md-6 item text">
                        <h3>GENERATORE VOCALE AI DI ALTISSIMA CLASSE</h3>
			<p>This system provide a plateform for voice trasformation with online and private pre-trained model</p>
		<uniquifier>Svc-Develop-Team, “SVC-develop-team/so-vits-SVC: Softvc vits singing voice conversion,” GitHub, https://github.com/svc-develop-team/so-vits-svc (accessed May 10, 2024).</uniquifier>
                    </div>
                </div>
		<uniquifier class="copyright">
			<weight value=400>
			Service powered by GENERATORE VOCALE AI DI ALTISSIMA CLASSE ©204
			</weight>
		</uniquifier>
            </div>
        </footer>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/js/bootstrap.bundle.min.js"></script>
<style>
.footer-dark {
  padding:50px 0;
  color:#f0f9ff;
  background-color:#282d32;
  position: absolute;  
bottom: 0;
  width: 100vw;
}

.footer-dark h3 {
  margin-top:0;
  margin-bottom:12px;
  font-weight:bold;
  font-size:16px;
}

.footer-dark ul {
  padding:0;
  list-style:none;
  line-height:1.6;
  font-size:14px;
  margin-bottom:0;
}

.footer-dark ul a {
  color:inherit;
  text-decoration:none;
  opacity:0.6;
}

.footer-dark ul a:hover {
  opacity:0.8;
}

@media (max-width:767px) {
  .footer-dark .item:not(.social) {
    text-align:center;
    padding-bottom:12px;
  }
}

.footer-dark .item.text {
  margin-bottom:36px;
}

@media (max-width:767px) {
  .footer-dark .item.text {
    margin-bottom:0;
  }
}

.footer-dark .item.text p {
  opacity:0.6;
  margin-bottom:0;
}

.footer-dark .item.social {
  text-align:center;
}

.alegreya-<uniquifier> {
  font-family: "Alegreya", serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
}


@media (max-width:991px) {
  .footer-dark .item.social {
    text-align:center;
    margin-top:20px;
  }
}

.footer-dark .item.social > a {
  font-size:20px;
  width:36px;
  height:36px;
  line-height:36px;
  display:inline-block;
  text-align:center;
  border-radius:50%;
  box-shadow:0 0 0 1px rgba(255,255,255,0.4);
  margin:0 8px;
  color:#fff;
  opacity:0.75;
}

.footer-dark .item.social > a:hover {
  opacity:0.9;
}

.footer-dark .copyright {
  text-align:center;
  padding-top:24px;
  opacity:0.3;
  font-size:13px;
  margin-bottom:0;
}

</style>
</body>
</html>
