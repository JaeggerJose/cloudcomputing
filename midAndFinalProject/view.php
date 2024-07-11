<?php
ini_set('display_errors','1');
error_reporting(E_ALL);
//header('refresh: 3;');
$nodeInfo_line = file('/share/job_info.txt');
$node_table='';
function DeletJob($job_id) {
	$dirPath="/share/".$job_id;
	if (!empty($dirPath) && is_dir($dirPath)) {
		$escapedDirPath = escapeshellarg($dirPath);
		$cmd = "rm -rf $escapedDirPath";
		$output = shell_exec($cmd);
		$file_path = '/share/job_info.txt';
		$content_to_delete ="$job_id Queueing";
		$file_lines = file($file_path);
		$deleted = false;
		foreach ($file_lines as $line_number => $line_content) {
        		if (strpos($line_content, $content_to_delete) !== false) {
				unset($file_lines[$line_number]);
				$deleted = true;
        			break;	
			}
		}
	       	if ($deleted) {
			file_put_contents($file_path, implode('', $file_lines));
			header("Location: view.php");
			exit();
		}	
	}	
}
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["myButton"])) {
	$job_id=$_POST["myButton"];	
	DeletJob($job_id);
}

foreach ($nodeInfo_line as $line) {
	$node_table.='<div class="table-row">';
	$words = explode(' ', $line);
	foreach ($words as $word) {	
        	$node_table.='<div class="table-data">'.$word.'</div>';
	}
	$output = "/share/".$words[0]."/output.txt";
	if(file_exists($output)){
		$fp = fopen($output,"r");
		while($line=fgets($fp)){
			$node_table.='<div class="table-data">'.$line.'</div>';
		}
		$node_table .= '<div class="table-data"></div>';
		fclose($fp);
	}
	else{
		$node_table .= '<div class="table-data">';
		$node_table .= '<form method="post" action="' . htmlspecialchars($_SERVER["PHP_SELF"]) . '">';
		$node_table .= '<button class="button" name="myButton" value="' . $words[0] . '" type="submit">DELETE</button>';
		$node_table .= '</form></div>';
		
	}
	$node_table.='</div>';
}

/*$output = "/share/".$_GET["jobId"]."/output.txt";
if(file_exists($output)){
	$fp = fopen($output,"r");
	while($line=fgets($fp)){
		echo $line;
	}
	fclose($fp);
}
else{
	echo "Queueing.."
	
}*/
?>
<!DOCTYPE html>
<html>
	<head>
        	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<link rel="stylesheet" href="view_css.css"/>
		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        	<script src="view.js"></script>
        	<title>Job_view</title>
    	</head>
	<body>
		<div class="container">
	
			<div class="table">
				<div class="table-header">
					<div class="header__item"><a id="name" class="filter__link" href="#">JobName</a></div> 
					<div class="header__item"><a id="wins" class="filter__link filter__link--number" href="#">status</a></div>
					<div class="header__item"><a id="draws" class="filter__link filter__link--number" href="#">output</a></div>
					<div class="header__item"><a id="losses" class="filter__link filter__link--number" href="#">delete</a></div>
				</div>
				<div class="table-content">	
					
					<?php echo $node_table; ?>
				</div>	
			</div>
		</div>
	</body>
</html>
