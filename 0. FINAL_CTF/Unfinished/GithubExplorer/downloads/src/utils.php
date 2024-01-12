<?php

  function listGitHubRepoFilesByURL($url) {
    $result = ['error' => null, 'data' => null];
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'User-Agent: PHP', 
        'authorization: Basic ' . API_TOKEN, 
    ]);
    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        $result['error'] = curl_error($ch);
        curl_close($ch);
        return $result;
    }
    curl_close($ch);
    $result['data'] = json_decode($response, true);
    return $result;
  }

  function parseAPIUrl($url) {
    $apiBaseUrl = 'https://api.github.com/';
    $result = ['error' => null, 'data' => null];
    $parsedUrl = parse_url($url);
    if (!isset($parsedUrl['scheme']) or $parsedUrl['scheme'] !== "https"){
      $result['error'] = 'Invalid schema. URL must start with \'https://\'';
      return $result;      
    }
    if (!isset($parsedUrl['host'])){
      $result['error'] = 'Invalid host';
      return $result;      
    } 
    if ($parsedUrl['host'] !== "api.github.com") {
      $result['error'] = 'URL does not start with https://api.github.com/';
      return $result;
    }
    $result['data'] = true;
    return $result;
  }

  function parseGitHubUrl($url) {
    $githubIoSuffix = '.github.io';
    $result = ['error' => null, 'data' => null];
    $parsedUrl = parse_url($url);
    if (!isset($parsedUrl['scheme']) or $parsedUrl['scheme'] !== "https"){
      $result['error'] = 'Invalid schema. URL must start with \'https://\'';
      return $result;      
    }
    if (!isset($parsedUrl['host'])){
      $result['error'] = 'Invalid host';
      return $result;      
    }   
    if ($parsedUrl['host'] === "github.com") {
      if (!isset($parsedUrl['path'])){
        $result['error'] = 'Invalid project path';
        return $result;      
      }   
      $parts = array_filter(explode('/', $parsedUrl['path']));
      if (count($parts) == 2) {
        $owner = $parts[1];
        $projectName = $parts[2];
        $result['data'] = array('owner' => $owner, 'projectName' => $projectName);
      } else
        $result['error'] = 'URL format is not valid for a GitHub repository';
    } elseif (substr($parsedUrl['host'], -strlen($githubIoSuffix)) === $githubIoSuffix) {
        $parsedUrl = parse_url($url);
        $hostParts = explode('.', $parsedUrl['host']);
        $owner = $hostParts[0];
        $projectName = $parsedUrl['host'];
        $result['data'] = array('owner' => $owner, 'projectName' => $projectName);
    } else 
      $result['error'] = 'URL does not start with https://github.com/ nor it ends with *.github.io';
    return $result;
  }

?>