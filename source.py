import urllib.request
import urllib.parse
import sys
import re
from bs4 import BeautifulSoup
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

film_name = ""
def get_movie_ftp(target_name):
    global film_name
    path = 'chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path)
    browser.get('http://www.dy2018.com/')

    elem = browser.find_element_by_name("keyboard")
    elem.send_keys(target_name)
    elem.send_keys(Keys.RETURN)

    browser.switch_to_window(browser.window_handles[1])
    base_url = browser.current_url
    browser.quit()

    if base_url == "https://www.dy2018.com/e/search/index.php": #没有结果
        return None

    films = []
    for i in range(10):
        url = base_url[:len(base_url) - 5] + "-page-" + str(i) + base_url[len(base_url) - 5:]
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        if not soup.find_all("a", class_="ulink"):
            break
        for each_title in soup.find_all("a", class_="ulink"):
            print(each_title.text)
            if re.match("(.*)《(.*)》(.*)", each_title.text):
                movie_name = re.match("(.*)《(.*)》(.*)", each_title.text).group(2)
                if re.match(target_name, movie_name):
                    films.append({"name": movie_name, "href": each_title["href"]})
    download_url = None
    for each in films:
        if each["name"] == target_name:
            download_url = 'http://www.dy2018.com/' + each["href"]
            film_name = each["name"]
            break
    if download_url == None:
        for each in films:
            if re.match(target_name, each["name"]):
                download_url = 'http://www.dy2018.com/' + each["href"]
                film_name = each["name"]
                break
    if download_url == None:
        return None

    response = urllib.request.urlopen(download_url)
    html = response.read().decode('gbk')
    soup = BeautifulSoup(html, "html.parser")

    ftp_urls = []
    for each in soup.find_all("td",bgcolor="#fdfddf"):
        url = each.text.replace("\n","")
        if url[:4] == "ftp:":
            ftp_urls.append(url)
    return ftp_urls

if __name__ == "__main__":
    urls = get_movie_ftp(input(":->"))
    if urls == None:
        print("暂时无法找到" + '"' + sys.argv[2] + '"的资源！ ')
        exit(0)

    for each in urls:
        tmp = each.split("/")
        print("正在为您下载：" + tmp[len(tmp) - 1])
        os.system('"C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe" ' + each)
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)
        pyautogui.press("enter")
