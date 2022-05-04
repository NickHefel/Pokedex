from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap


def getdata(url):
    r = requests.get(url)
    return r.text

#taking user input
print("What do you want to download?")
download = input()
site = 'https://www.google.com/search?tbm=isch&q='+download

htmldata = getdata(site)
soup = BeautifulSoup(htmldata, 'html.parser')
List = []
i = 0
for item in soup.find_all('img'):
    List.append(item['src'])
    #print(item['src'])

print(List[1])
url_image = List[1]

app = QApplication([])
image = QImage()
image.loadFromData(requests.get(url_image).content)

image_label = QLabel()
image_label.setPixmap(QPixmap(image))
image_label.show()

app.exec_()