from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
<<<<<<< HEAD
from googletrans import Translator #pip install googletrans==4.0.0-rc1
import sqlite3
from sqlite3 import Error


class PEx(BehaviorModelExecutor):
=======
from selenium.webdriver.common.keys import Keys
import pyperclip
from telegram import *
from telegram.ext import *
from TestChatbot import *
import random
import time


class PEx(BehaviorModelExecutor):
    Queue = []
>>>>>>> feature/JunHyuk
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)
<<<<<<< HEAD
        self.translator = Translator()
        self.post_num = '-1'
        self.count = 0
        self.driver = webdriver.Chrome("chromedriver")


=======
        self.driver1 = webdriver.Chrome("chromedriver")  #크롬 드라이버 객체 생성
        self.driver2 = webdriver.Chrome("chromedriver")  #크롬 드라이버 객체 생성
        self.count = bot.chatbot_db.remove_old_data() #데이터 베이스의 데이터 갯수 저장
        self.languages = ['ko', 'en', 'zh-CN', 'ja', 'vi']
        
>>>>>>> feature/JunHyuk
        self.insert_input_port("start")

    def ext_trans(self,port, msg):
        if port == "start":
            print("[Start]: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end = '\n\n')
            self._cur_state = "Generate"
<<<<<<< HEAD
        self.con = self.connection()
        self.create_table(self.con)
        self.delete_table(self.con)


    def output(self):
        self.driver.implicitly_wait(20)
        self.driver.get("https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679")
        self.driver.implicitly_wait(20)
        boxs = self.driver.find_element(By.CLASS_NAME, 'boardList_boxWrap')
        self.driver.implicitly_wait(20)
        box = boxs.find_element(By.ID, 'disasterSms_tr')
        ID = []
        for i in range(10):
            self.driver.implicitly_wait(20)
            new_id = box.find_elements(By.ID, 'disasterSms_tr_%c_MD101_SN'%str(i))
            if(len(new_id) == 1):
                ID.append(new_id[0].text)
        index = 0
        print("[OUT]: %s [ID]: "%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ID)
        if(ID[0] != self.post_num):
            titles = box.find_elements(By.TAG_NAME, "tr")
            while(index < 10):
                if(ID[index] == self.post_num):
                    break
                title = titles[index].find_element(By.TAG_NAME, 'a').click()
                self.driver.implicitly_wait(20)
                message = self.driver.find_element(By.CSS_SELECTOR, '#msg_cn').text
                self.driver.back()
                #self.driver.implicitly_wait(20)
                if(message != ''):
                    if(message[0] == ' '): message = message[1:]
                    call = ""
                    site = ""
                    print(message)
                    if(message.find('bit') != -1):
                        bit = message.find('bit.ly')
                        site = message[bit:message[bit:].find(' ')+bit]
                        message = message[:bit] + message[message[bit:].find(' ')+bit:]
                    if(message.find('ncvr') != -1):
                        ncvr = message.find('ncvr')
                        if(message[ncvr-1] == '('):
                            site = message[ncvr-1:]
                            #message = message[:ncvr-1] + ' ' +message[ncvr + 16:]
                            message = message[:ncvr-1]
                        else:
                            site = message[ncvr:]
                            #message = message[:ncvr] + ' ' +message[ncvr + 15:]
                            message = message[:ncvr]
                    if(message.find('☎') != -1):
                        call = message[message.find('☎'):]
                        message = message[:message.find('☎')]
                    messages = [message, "", "", ""]
                    langs = ['ko', 'en', 'zh-cn', 'ja']
                    for i in message.split('▲'):
                        if(i.find(')') - i.find('(') > 4):
                            s = i.find('(')
                            e = i.find(')')
                            for l in range(1, len(langs)):
                                if(s > 0):
                                    messages[l] += self.translator.translate(i[:s], dest = langs[l], src = 'ko').text + '('
                                else: messages[l] += '('
                                messages[l] += self.translator.translate(i[s+1:e], dest = langs[l], src = 'ko').text + ')'
                                if(len(i) > e+1 and i[e+1:] != ' '):
                                    messages[l] += self.translator.translate(i[e+1:], dest = langs[l], src = 'ko').text + '. '
                                else: messages[l] += '. '
                        else:
                            for l in range(1, len(langs)):
                                messages[l] += self.translator.translate(i, dest = langs[l], src = 'ko').text + '. '
                    #한국어 ko 영어 en 중국어(간체) zh-cn 중국어(번체) zh-tw 일본어 ja
                    if(site != ""):
                        for l in range(0, len(langs)):
                            messages[l] += site
                    if(call != ""):
                        for l in range(0, len(langs)):
                            messages[l] += call
                    for i in range(len(messages)):
                        self.insert_table(self.con, i, messages[i])
                        print(messages[i])
                    index += 1
                else: 
                    continue
                print()
            self.post_num = ID[0]
=======

    def output(self):
        div, AREA, ID = self.message_Information()  #사이트 크롤링(문자 종류, 기관, 번호 반환)
        index = 9
        print("[OUT]: %s [ID]: "%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ID)
        if(ID[0] > bot.chatbot_db.post_num):                  #재난 문자가 업데이트 되었을 때
            while(index > -1):
                if(ID[index] <= bot.chatbot_db.post_num):     #이미 데이터 베이스에 저장된 재난 문자면 continue
                    index -= 1
                    continue
                message, local = self.message_collect(index)    #메시지와 지역 수집
                print(local)
                print(message)
                if(message != ''):
                    self.message_db_save(message, div, local, AREA, ID, index)  #메시지와 정보 데이터 베이스에 저장
                    self.message_send(ID, local, index)                         #메시지 보내기
                    self.count += len(local)                                    #데이터 베이스의 데이터의 갯수 추가
                    index -= 1
                    if(self.count >= 150):
                        self.count = bot.chatbot_db.remove_old_data()           #데이터가 150개 이상이면 10개 삭제
                else: 
                    continue    #메시지를 읽어 오는데 실패했으므로 continue
                print()
        elif(random.randint(0, 100) % 15 == 0):
            self.randmessage()  #랜덤 db 데이터 삽입 및 텔레그램 메시지 출력

    def message_Information(self):
        while(1):
            try:
                self.driver1.implicitly_wait(20)
                self.driver1.get("https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679")
                self.driver1.implicitly_wait(20)
                self.boxs = self.driver1.find_element(By.CLASS_NAME, 'boardList_boxWrap')
                break
            except:
                continue
        self.driver1.implicitly_wait(20)
        self.box = self.boxs.find_element(By.ID, 'disasterSms_tr')
        ID = []
        div = [] 
        AREA = []

        for i in range(10):
            self.driver1.implicitly_wait(20)
            new_id = self.box.find_elements(By.ID, 'disasterSms_tr_%c_MD101_SN'%str(i))                                  #재난 문자의 번호 저장
            div_id = self.box.find_elements(By.ID, 'disasterSms_tr_%c_DSSTR_SE_NM'%str(i))                               #재난 문자의 종류 저장
            area_id = self.box.find_elements(By.CSS_SELECTOR, '#disasterSms_tr_%c_apiData1 > td:nth-child(4)'%str(i))    #재난 문자의 기관 저장

            if(len(new_id) == 1):
                ID.append(new_id[0].text)
                div.append(div_id[0].text)  
                AREA.append(area_id[0].text)
        
        if(ID[0] > bot.chatbot_db.post_num):  #재난 문자가 업데이트 되었을 때
            self.titles = self.box.find_elements(By.TAG_NAME, "tr")
        
        return div, AREA, ID

    def message_collect(self, index):
        while(1):
            try:
                title = self.titles[index].find_element(By.TAG_NAME, 'a').click()    #링크 클릭하여 접속
                self.driver1.implicitly_wait(20)
                location = self.driver1.find_element(By.CSS_SELECTOR, '#bbsDetail_0_cdate').text #재난 문자 발송 지역 저장
                location = location.split(',')
                local = []
                if(len(location) > 1):  #여러 지역에 발송되었을 때
                    for i in location:
                        local.append(i.split()[0])
                    local = list(set(local))
                else:   #한 지역에만 발송되었을 때
                    local.append(location[0].split()[0])

                message = self.driver1.find_element(By.CSS_SELECTOR, '#msg_cn').text #재난 문자 메시지 저장
                self.driver1.back()
                break
            except:
                continue

        return message, local

    def clipboard_input(driver, user_input="", default_delay=1):
        temp_copy = pyperclip.paste()
        pyperclip.copy(user_input)  #번역할 내용 클립보드에 저장
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()   #ctrl+v 명령어 수행
        pyperclip.copy(temp_copy)   #클립보드 비우기
        return
    
    def TransMessage(message, src='ko', dest='en'):
        driver = webdriver.Chrome("chromedriver")
        while(1):
            try:
                url = "https://papago.naver.com/?sk=%s&tk=%s"%(src, dest)
                if(dest in "krja"): #한국어랑 일본어는 높임말이 있어 예외처리
                    url += "&hn=1"
                driver.get(url)
                driver.implicitly_wait(20)

                input_content = driver.find_element(By.XPATH, '//*[@id="txtSource"]')     #번역할 내용을 넣는 공간
                process_Btn = driver.find_element(By.XPATH, '//*[@id="btnTranslate"]')    #번역하기 버튼
                output_content = driver.find_element(By.XPATH, '//*[@id="txtTarget"]')    #번역된 내용이 있는 공간

                input_content.clear()   #공간 비우기
                driver.implicitly_wait(20)
                input_content.click()   #공간 클릭
                PEx.clipboard_input(driver, message)   #공간에 번역할 내용 복사하기
                process_Btn.click()             #번역하기 버튼 클릭
                driver.implicitly_wait(20)    #번역 대기 시간
                while output_content.text == "":    #아직 번역이 되지 않았을 때
                    driver.implicitly_wait(20)
                print(output_content.text)
                break
            except:
                continue
        
        return output_content.text

    def message_db_save(self, message, div, local, AREA, ID, index):
        date_time, area = AREA[index].split(' [')
        area = area[:len(area)-1]
        keyword = div[index]
        for j in local:
            bot.chatbot_db.insert_table(1, [message, keyword, j, area, ID[index], date_time]) #메시지, 종류, 지역, 기관, 번호 순으로 저장

    def message_send(self, local, ID, index):
        for loc in local:
            bot.sendMessageFromSim(loc)        #챗봇에 메시지 출력
        bot.chatbot_db.post_num = ID[index]       #시뮬레이션의 post_num을 방금 db에 저장한 가장 최근 재난 문자의 번호로 초기화

    def randmessage(self):
        print('send message')
        bot.chatbot_db.insert_table(1, ['%s.안녕하세요. 테스트 용 메시지 입니다.(한국어)'%str(int(bot.chatbot_db.post_num)+1), '병', '충청북도', '충청북도', str(int(bot.chatbot_db.post_num)+1), '2023-01-18'])
        bot.sendMessageFromSim('충청북도')
        bot.chatbot_db.post_num = bot.chatbot_db.post_number()
        self.count += 1
        if(self.count >= 150):
            self.count = bot.chatbot_db.remove_old_data()
>>>>>>> feature/JunHyuk
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

<<<<<<< HEAD
    def connection(self):
        try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
            con = sqlite3.connect('message_db.db')
            print("[DB] - connect")
            return con
        except Error: # 에러 출력
            print(Error)

    def create_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("CREATE TABLE IF NOT EXISTS kr_tb(info TEXT)")
        cursor_db.execute("CREATE TABLE IF NOT EXISTS eng_tb(info TEXT)")
        cursor_db.execute("CREATE TABLE IF NOT EXISTS ch_tb(info TEXT)")
        cursor_db.execute("CREATE TABLE IF NOT EXISTS jp_tb(info TEXT)")
        con.commit()

    def insert_table(self, con, index, str_data):
        cursor_db = con.cursor()
        if(index == 0):
            cursor_db.execute('INSERT INTO kr_tb VALUES (?)', (str_data,))
        elif(index == 1):
            cursor_db.execute('INSERT INTO eng_tb VALUES (?)', (str_data,))
        elif(index == 2):
            cursor_db.execute('INSERT INTO ch_tb VALUES (?)', (str_data,))
        elif(index == 3):
            cursor_db.execute('INSERT INTO jp_tb VALUES (?)', (str_data,))
        con.commit()

    def delete_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("DELETE FROM kr_tb")
        cursor_db.execute("DELETE FROM eng_tb")
        cursor_db.execute("DELETE FROM ch_tb")
        cursor_db.execute("DELETE FROM jp_tb")
        con.commit()

    def disconnetion(self, con):
        con.close()
        print("[DB] - disconnet")




ss = SystemSimulator()

ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("start")
gen = PEx(0, Infinite, "Gen", "first")
ss.get_engine("first").register_entity(gen)

ss.get_engine("first").coupling_relation(None, "start", gen, "start")

ss.get_engine("first").insert_external_event("start", None)

ss.get_engine("first").simulate()
=======

if __name__ == "__main__":
    bot = TestChatbot()
    bot.updater.dispatcher.add_handler(bot.mainHandler_conv)
    bot.updater.start_polling()
    # bot.updater.idle()

    ss = SystemSimulator()

    ss.register_engine("first", "REAL_TIME", 1)
    ss.get_engine("first").insert_input_port("start")
    gen = PEx(0, Infinite, "Gen", "first")
    ss.get_engine("first").register_entity(gen)

    ss.get_engine("first").coupling_relation(None, "start", gen, "start")

    ss.get_engine("first").insert_external_event("start", None)

    ss.get_engine("first").simulate()


>>>>>>> feature/JunHyuk
