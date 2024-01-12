<?php
  $token = getenv('TOKEN');
  $userid = getenv('USERID');
  $encodedToken = base64_encode($userid . ":" . $token);
  define('API_TOKEN', $encodedToken);          
?>