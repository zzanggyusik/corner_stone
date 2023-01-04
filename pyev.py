from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from googletrans import Translator #pip install googletrans==4.0.0-rc1
import sqlite3
from sqlite3 import Error


class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)
        self.translator = Translator()
        self.post_num = '-1'
        self.count = 0
        self.driver = webdriver.Chrome("chromedriver")


        self.insert_input_port("start")

    def ext_trans(self,port, msg):
        if port == "start":
            print("[Start]: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end = '\n\n')
            self._cur_state = "Generate"
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
                    #번역을 위한 전 처리 과정
                    if(message.find('bit') != -1):  #사이트 추출
                        bit = message.find('bit.ly')
                        site = message[bit:message[bit:].find(' ')+bit]
                        message = message[:bit] + message[message[bit:].find(' ')+bit:]
                    if(message.find('ncvr') != -1):
                        ncvr = message.find('ncvr')
                        if(message[ncvr-1] == '('): #사이트가 괄호 안에 있다면 괄호를 포함하여 추출
                            site = message[ncvr-1:ncvr+16]
                            message = message[:ncvr-1] + message[ncvr+16:]
                        else:
                            site = message[ncvr:ncvr+15]
                            message = message[:ncvr] + message[ncvr+15:]
                    if(message.find('http') != -1):
                        http = message.find('http')
                        site = message[http:]
                        message = message[:http]
                    if(message.find('☎') != -1):   #전화 번호 추출
                        ca = message.find('☎')
                        if(message[ca-1] == '('):   #전화 번호가 괄호 안에 있다면 괄호를 포함하여 추출
                            call = message[ca-1:]
                            message = message[:ca-1]
                        else:
                            call = message[ca:]
                            message = message[:ca]
                    if(message.find('☏') != -1):
                        ca = message.find('☏')
                        if(message[ca-1] == '('):
                            call = message[ca-1:]
                            message = message[:ca-1]
                        else:
                            call = message[ca:]
                            message = message[:ca]

                    messages = [message, "", "", ""]
                    langs = ['ko', 'en', 'zh-cn', 'ja']
                    covid = -10
                    while(message[covid+10:].find('코로나') != -1):
                        covid = message[covid+10:].find('코로나') + covid + 10
                        if(covid != -1):
                            message = message[:covid] + '코로나 바이러스 ' + message[covid+3:]
                    message = message.replace('▲', '\n').replace('▶', '\n').replace('△', '\n')
                    message = '\n'.join(message.split('\n\n'))
                    for i in message.split('\n'):
                        if(i.find(')') - i.find('(') > 4):  #괄호 안에 문자열이 있을 경우
                            s = i.find('(') #괄호 안 문자열을 따로 번역하기 위한 전처리 과정
                            e = i.find(')')
                            for l in range(1, len(langs)):
                                if(s > 0):  #괄호가 맨 앞에 있지 않을 경우
                                    messages[l] += self.translator.translate(i[:s], dest = langs[l], src = 'ko').text + '(' #괄호 앞에 있는 문자열을 번역 및 저장
                                else: messages[l] += '(' #괄호가 맨 앞에 있을 경우

                                messages[l] += self.translator.translate(i[s+1:e], dest = langs[l], src = 'ko').text + ')'  #괄호 안에 있는 문자열을 번역 및 저장

                                if(len(i) > e+1 and i[e+1:] != ' ' and i[e+1:] != '\n'):    #괄호가 맨 뒤에 있지 않을 경우
                                    messages[l] += self.translator.translate(i[e+1:], dest = langs[l], src = 'ko').text + '. '  #괄호 뒤에 있는 문자열을 번역 및 저장
                                else: messages[l] += '. ' #괄호가 맨 뒤에 있을 경우
                        else:   #괄호 안에 문자열이 없을 경우
                            for l in range(1, len(langs)):
                                messages[l] += self.translator.translate(i, dest = langs[l], src = 'ko').text + '. '

                    #한국어 ko 영어 en 중국어(간체) zh-cn 중국어(번체) zh-tw 일본어 ja
                    if(site != ""):
                        for l in range(0, len(langs)):  #추출했던 사이트 이어 붙이기
                            messages[l] += site
                    if(call != ""):
                        for l in range(0, len(langs)):  #추출했던 전화 번호 이어 붙이기
                            messages[l] += call
                    for i in range(len(messages)):
                        self.insert_table(self.con, i, messages[i]) #데이터 베이스에 번역된 문자열 저장
                        print(messages[i])
                    index += 1
                else: 
                    continue
                print()
            self.post_num = ID[0]
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

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