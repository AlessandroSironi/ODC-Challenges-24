<?php
  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $queryString = http_build_query($_POST);
    $encodedString = urlencode($queryString);
    $url = 'visitor:8000/submission';
    $postData = [
      'params' => $encodedString,
    ];
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($httpCode == 200)
      header('Location: /');
    else
      http_response_code(500);
  } else 
    http_response_code(405);
  exit();
?>