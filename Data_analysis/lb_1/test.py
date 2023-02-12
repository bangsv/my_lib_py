from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter
import re


def ceck():
    text = 'Право правовой приправный право проправо правопривет Привет Андрей Леонидович' 
    print(text) 
    text = str(re.findall(r'\b(?:\w+ [право][а-я]+)+\b', text)).split()
    print(text) 
    print(len (text))


if __name__ == '__main__': 
    ceck() 
