<?php
  require_once 'config.php';
  include 'utils.php';

  // Only GET method
  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      http_response_code(405);
      exit;
  }
  $errorMsg = '';
  $repoFiles = '';
  $apiURL = '';
  if (isset($_GET['git_url'])) {
      $parsedUrl = parseGitHubUrl($_GET['git_url']);
      if ($parsedUrl['error'])
        $errorMsg = "Error: " . $parsedUrl['error'];
      else {
        $owner = $parsedUrl['data']['owner'];
        $projectName = $parsedUrl['data']['projectName'];
        $apiURL = "https://api.github.com/repos/$owner/$projectName/contents/";
        $repoFiles = listGitHubRepoFilesByURL($apiURL);
        if ($repoFiles['error'])
          $errorMsg = "Error: " . $repoFiles['error'];
        else
          $repoFiles = $repoFiles['data'];
      }
  } elseif (isset($_GET['api_url'])) {
      $parsedUrl = parseAPIUrl($_GET['api_url']);
      if ($parsedUrl['error'])
        $errorMsg = "Error: " . $parsedUrl['error'];
      else {
        $apiURL = $_GET['api_url'];
        $repoFiles = listGitHubRepoFilesByURL($apiURL);
        if ($repoFiles['error'])
          $errorMsg = "Error: " . $repoFiles['error'];
        else
          $repoFiles = $repoFiles['data'];
      }
  }

  include 'header.php';
?>

  <body>
    <header>
        <div class="header-content">
            <h1>GitHub Explorer</h1>
        </div>
    </header>
    <div class="main-container">
      <form id="git-form" class="needs-validation" novalidate>
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">GitHub URL:</span>
          </div>
          <input type="text" class="form-control" id="git-url" placeholder="https://github.com/JinBlack/libdebug" required>
          <div class="invalid-feedback">
            Please provide a GitHub URL
          </div>
        </div>
      </form>
      <div class="container mb-5">
        <div class="row justify-content-between">
          <div class="col-auto">
            <button id="explore-button" class="btn btn-primary">Explore</button>
          </div>
          <div class="col-auto">
            <button id="bug-report-button" type="button" class="btn btn-danger">Report a bug</button>
          </div>
        </div>
      </div>
      <?php if ($errorMsg): ?>
        <div id="error-container" class="alert alert-danger" role="alert">
          <?php echo $errorMsg; ?>
        </div>
      <?php elseif ($repoFiles):  ?>
        <div id="repo-container" class="container">
          <div class="alert alert-primary break-word" role="alert">
            <?php echo "API URL: " . $apiURL; ?>
          </div>
          <ul class="list-group">
            <?php 
              foreach ($repoFiles as $item) {
                if ($item['type'] === "dir") 
                  echo "<li class=\"list-group-item d-flex justify-content-between align-items-center\"><div class=\"d-flex align-items-center\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"currentColor\" class=\"bi bi-folder\" viewBox=\"0 0 16 16\"><path d=\"M.54 3.87.5 3a2 2 0 0 1 2-2h3.672a2 2 0 0 1 1.414.586l.828.828A2 2 0 0 0 9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.826a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31zM2.19 4a1 1 0 0 0-.996 1.09l.637 7a1 1 0 0 0 .995.91h10.348a1 1 0 0 0 .995-.91l.637-7A1 1 0 0 0 13.81 4H2.19zm4.69-1.707A1 1 0 0 0 6.172 2H2.5a1 1 0 0 0-1 .981l.006.139C1.72 3.042 1.95 3 2.19   3h5.396l-.707-.707z\"/></svg><span class=\"ml-4\"><a href=\"/?api_url=" . urlencode($item['url']) . "\">" . $item['name'] . "</a></span></div></li>";
              }
              foreach ($repoFiles as $item) 
                if ($item['type'] === "file") 
                  echo "<li class=\"list-group-item d-flex justify-content-between align-items-center\"><div class=\"d-flex align-items-center\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"currentColor\" class=\"bi bi-file\" viewBox=\"0 0 16 16\"><path d=\"M4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm0 1h8a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1\"/></svg><span class=\"ml-4\"><a href=\"" . $item['download_url'] . "\">" . $item['name'] . "</a></span></div></li>";
            ?>
          </ul>
        </div>
      <?php endif; ?>
        


    </div>
    <script type="text/javascript" src="html/js/scripts.js"></script>
  </body>
</html>