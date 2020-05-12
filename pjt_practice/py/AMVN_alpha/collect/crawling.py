

from selenium import webdriver
import os
import shutil
from AMVN_alpha.utils.util import mkdirs_
from AMVN_alpha.utils.option import Options

opt = Options()


def move_txt(input_, output_) :
    dir_list =  [txt for txt in os.listdir(input_) if txt.endswith(".txt")]
    mkdirs_(output_)
    for txt in dir_list :
        shutil.move(input_ +txt, output_ +txt)


def check_login(driver) :
    tmp_header = driver.find_element_by_xpath("//div[@id='header']/div[@class='top_menu']/ul/li")

    with open(opt.papago_api,'r',encoding='utf8') as f :
        api_data = f.readlines()

        id_ = api_data[2].strip()
        password_ = api_data[3].strip()

    # need to log-in
    if tmp_header.text == '들어가기' :
        tmp_header.click()

        login_id = driver.find_element_by_xpath("//input[@id='loginId']")
        login_id.clear()
        login_id.send_keys(id_)

        login_id = driver.find_element_by_xpath("//input[@id='password']")
        login_id.clear()
        login_id.send_keys(password_)

        driver.find_element_by_xpath("//div[@class='t_c mt30']/a").click()


def crwaling_posData() :
    driver = webdriver.chrome(opt.webdriver_path)

    driver.get('https://ithub.korean.go.kr/user/total/database/corpusManager.do')
    check_login(driver)

    driver.get('https://ithub.korean.go.kr/user/total/database/corpusManager.do')

    # waitting_load
    driver.implicitly_wait(3)
    # data_length
    cur_no = int(driver.find_element_by_xpath("//div[@id='corpusList']/div[@class='result_wrap']/table[@class='tbl_list']/tbody/tr/td").text)

    # select last_index_contents
    driver.find_element_by_xpath(
        "//div[@id='corpusList']/div[@class='result_wrap']/table[@class='tbl_list']/tbody/tr/td[@class='lf']/a").click()
    # waitting_load
    driver.implicitly_wait(3)

    for _ in range(cur_no, 0, -1):
        # 형태소 분석된 파일만 확인해서 긁어오기
        try:
            ch_box = driver.find_element_by_xpath("//input[@name='posFileSeq']")
            ch_box.click()

            driver.find_element_by_xpath("//label[@for='posFileSeq']/following-sibling::a").click()

            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//input[@id='agreementYn']").click()
            driver.find_element_by_xpath("//div[@id='agreementDownloadLayer']/div[@class='c_t mt15']/a").click()

        except:
            print("Don't have pos :", _)
            pass
        finally:
            driver.find_element_by_xpath(
                "//div[@id='corpusSubList']/div/div[@class='fl']/a/following-sibling::a/following-sibling::a").click()


def crwaling_trainData() :
    driver = webdriver.chrome(opt.webdriver_path)

    # waitting_load
    driver.implicitly_wait(3)
    # 총 데이터 갯수
    cur_no = int(driver.find_element_by_xpath("//div[@id='corpusList']/div[@class='result_wrap']/table[@class='tbl_list']/tbody/tr/td").text)

    # select last_index_contents
    driver.find_element_by_xpath("//div[@id='corpusList']/div[@class='result_wrap']/table[@class='tbl_list']/tbody/tr/td[@class='lf']/a").click()
    # waitting_load
    driver.implicitly_wait(3)

    # 어느정도 정돈된 데이터의 마지막숫자
    last_no = 1295

    for _ in range(cur_no,last_no,-1) :
        # 형태소 분석된 파일만 확인해서 긁어오기
        try :
            ch_box = driver.find_element_by_xpath("//input[@name='orgFileSeq']")
            ch_box.click()

            driver.find_element_by_xpath("//label[@for='posFileSeq']/following-sibling::a").click()

            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//input[@id='agreementYn']").click()
            driver.find_element_by_xpath("//div[@id='agreementDownloadLayer']/div[@class='c_t mt15']/a").click()

        except :
            print("Don't have pos :", _)
            pass
        finally :
            driver.find_element_by_xpath("//div[@id='corpusSubList']/div/div[@class='fl']/a/following-sibling::a/following-sibling::a").click()

    driver.close()