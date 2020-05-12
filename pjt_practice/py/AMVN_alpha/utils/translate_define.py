

from selenium import webdriver
import urllib.request
import time
from bs4 import BeautifulSoup
import json

from AMVN_alpha.utils.option import Options

opt = Options()


def translate(text, useType='api_papago') :
    if useType.lower() == 'api_papago' :
        return translate_by_papago_api(text)
    elif useType.lower() == 'selenium_papago' :
        return translate_by_selenium_naver(text)
    elif useType.lower() == 'selenium_google' :
        return translate_by_selenium(text)
    else :
        raise print('Error : use collect type')


def translate_by_selenium_naver(text):

    driver = webdriver.Chrome(opt.webdriver_path)

    driver.get("https://papago.naver.com/")
    driver.implicitly_wait(3)
    driver.find_element_by_id('txtSource').send_keys(text)

    # waitting_load
    time.sleep(1)
    output_ = driver.find_element_by_id('txtTarget').text
    driver.close()

    return output_


def translate_by_selenium(text):

    driver = webdriver.Chrome(opt.webdriver_path)

    driver.get("https://translate.google.com/")

    driver.find_element_by_id('sugg-item-en').click()
    driver.find_element_by_id('sugg-item-ko').click()

    driver.find_element_by_id('source').send_keys(text)

    time.sleep(1)
    source = driver.page_source
    soupData = BeautifulSoup(source, 'html.parser')

    driver.close()

    return soupData.find('span', class_='tlid-translation translation').text


def translate_by_papago_api(text):

    with open(opt.papago_api,'r',encoding='utf8') as f :
        api_data = f.readlines()

        client_id = api_data[0].strip()
        client_secret = api_data[1].strip()

    output_ = ''
    encText = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        str2dict = json.loads(response_body.decode('utf-8'))
        output_ = str2dict['message']['result']['translatedText']
    else:
        output_ = "Error Code:" + rescode

    return output_


# definition_dictionary crawling
def define_word(text):

    driver = webdriver.Chrome(opt.webdriver_path)

    driver.get("https://ko.dict.naver.com/#/main")

    driver.find_element_by_id('ac_input').send_keys(text)

    driver.find_element_by_xpath("//button[@class='btn_search']").click()

    time.sleep(1)
    driver.find_element_by_xpath(
        "//div[@class='component_keyword has-saving-function']/div[@class='row']/div[@class='origin']/a").click()
    time.sleep(1)

    try:
        output_ = driver.find_element_by_xpath("//ul[@class='mean_list my_mean_list']").text
    except:
        output_ = driver.find_element_by_xpath("//li[@class='mean_item']/div[@class='mean_desc']/p[@class='cont']").text
    finally:
        driver.close()

    return output_
