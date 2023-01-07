from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from googletrans import Translator #pip install googletrans==4.0.0-rc1
import sqlite3
from sqlite3 import Error
from telegram import *
from telegram.ext import *
from CornerstoneChatbot import *
from ChatbotDB import ChatbotDB
import re
import random
import time


class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)
        self.translator = Translator()                  #번역 객체 생성
        self.driver = webdriver.Chrome("chromedriver")  #크롬 드라이버 객체 생성
        self.db_langs = ['kr_tb', 'eng_tb', 'ch_tb', 'jp_tb']
        self.db_label = ['info', 'keyword', 'region', 'area', 'number']
        self.db_types = ['TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT']
        self.Chatbot = ChatbotDB()              #ChatbotDB 객체 생성
        self.con = self.Chatbot.connection()    #데이터 베이스와 연결
        bot.chatbot_db.con = self.con           
        self.Chatbot.create_insert_table(self.con, self.db_langs, self.db_label, self.db_types, 1)  #테이블 생성
        #self.delete_table(self.con)
        self.post_num = self.Chatbot.post_number(self.con)  #데이터 베이스의 가장 최신 문자의 번호를 저장
        bot.post_num = self.post_num                        #챗봇의 post_num을 방금 db에 저장한 가장 최근 재난 문자의 번호로 초기화
        self.count = self.Chatbot.remove_old_data(self.con) #데이터 베이스의 데이터 갯수 저장
        
        self.insert_input_port("start")

    def ext_trans(self,port, msg):
        if port == "start":
            print("[Start]: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end = '\n\n')
            self._cur_state = "Generate"

    def output(self):
        bot.post_num = self.post_num                #챗봇의 post_num을 방금 db에 저장한 가장 최근 재난 문자의 번호로 초기화
        div, AREA, ID = self.message_Information()  #사이트 크롤링(문자 종류, 기관, 번호 반환)
        index = 9
        print("[OUT]: %s [ID]: "%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ID)
        if(ID[0] > self.post_num):                  #재난 문자가 업데이트 되었을 때
            while(index > -1):
                if(ID[index] <= self.post_num):     #이미 데이터 베이스에 저장된 재난 문자면 continue
                    index -= 1
                    continue
                message, local = self.message_collect(index)            #메시지와 지역 수집
                print(local)
                print(message)
                if(message != ''):
                    message, call, site = self.message_pre_processing(message)  #번역을 위한 메시지 전처리
                    messages = self.message_translate(message, call, site)      #메시지 번역
                    self.message_db_save(messages, div, local, AREA, ID, index) #메시지와 정보 데이터 베이스에 저장
                    self.message_send(ID, index)                                #메시지 보내기
                    self.count += len(local)                                    #데이터 베이스의 데이터의 갯수 추가
                    index -= 1
                    if(self.count >= 150):
                        self.count = self.Chatbot.remove_old_data(self.con)     #데이터가 150개 이상이면 10개 삭제
                else: 
                    continue    #메시지를 읽어 오는데 실패했으므로 continue
                print()
        elif(random.randint(0, 100) % 15 == 0):
            self.randmessage()  #랜덤 db 데이터 삽입 및 텔레그램 메시지 출력

    def message_Information(self):
        while(1):
            try:
                self.driver.implicitly_wait(20)
                self.driver.get("https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679")
                self.driver.implicitly_wait(20)
                self.boxs = self.driver.find_element(By.CLASS_NAME, 'boardList_boxWrap')
                break
            except:
                continue
        self.driver.implicitly_wait(20)
        self.box = self.boxs.find_element(By.ID, 'disasterSms_tr')
        ID = []
        div = [] 
        AREA = []

        for i in range(10):
            self.driver.implicitly_wait(20)
            new_id = self.box.find_elements(By.ID, 'disasterSms_tr_%c_MD101_SN'%str(i))                                  #재난 문자의 번호 저장
            div_id = self.box.find_elements(By.ID, 'disasterSms_tr_%c_DSSTR_SE_NM'%str(i))                               #재난 문자의 종류 저장
            area_id = self.box.find_elements(By.CSS_SELECTOR, '#disasterSms_tr_%c_apiData1 > td:nth-child(4)'%str(i))    #재난 문자의 기관 저장

            if(len(new_id) == 1):
                ID.append(new_id[0].text)
                div.append(div_id[0].text)  
                AREA.append(area_id[0].text)
        
        if(ID[0] > self.post_num):  #재난 문자가 업데이트 되었을 때
            self.titles = self.box.find_elements(By.TAG_NAME, "tr")
        
        return div, AREA, ID

    def message_collect(self, index):
        while(1):
            try:
                title = self.titles[index].find_element(By.TAG_NAME, 'a').click()    #링크 클릭하여 접속
                self.driver.implicitly_wait(20)
                location = self.driver.find_element(By.CSS_SELECTOR, '#bbsDetail_0_cdate').text #재난 문자 발송 지역 저장
                location = location.split(',')
                local = []
                if(len(location) > 1):  #여러 지역에 발송되었을 때
                    for i in location:
                        local.append(i.split()[0])
                    local = list(set(local))
                else:   #한 지역에만 발송되었을 때
                    local.append(location[0].split()[0])

                message = self.driver.find_element(By.CSS_SELECTOR, '#msg_cn').text #재난 문자 메시지 저장
                self.driver.back()
                break
            except:
                continue

        return message, local

    def message_pre_processing(self, message):
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

        message = '코로나 바이러스 '.join(message.split('코로나')) #코로나라는 문자열이 있을 때 코로나를 코로나 바이러스라는 문자열로 변경
        message = message.replace('▲', '\n').replace('▶', '\n').replace('△', '\n')  #해당 이모티콘 제거
        message = '\n'.join(message.split('\n\n'))
        return message, call, site

    def message_translate(self, message, call, site):
        messages = [message, "", "", ""]
        langs = ['ko', 'en', 'zh-cn', 'ja']

        for i in message.split('\n'):
            if(i == '' or i == ' ' or i == '\n'): continue  #문자열이 비어 있으면 continue
            if(i[0] == ' '): i = i[1:]
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
            elif(i.find(')') != -1 and i.find('(') != -1): #괄호안에 문자열이 있으나 짧을 경우
                s = i.find('(')
                e = i.find(')')
                for l in range(1, len(langs)):
                    messages[l] += self.translator.translate(i[:e+1], dest = langs[l], src = 'ko').text  #괄호 앞과 괄호 안에 있는 문자열을 같이 번역 및 저장

                    if(len(i) > e+1 and i[e+1:] != ' ' and i[e+1:] != '\n'):    #괄호가 맨 뒤에 있지 않을 경우
                        messages[l] += self.translator.translate(i[e+1:], dest = langs[l], src = 'ko').text + '. '  #괄호 뒤에 있는 문자열을 번역 및 저장
                    else: messages[l] += '. ' #괄호가 맨 뒤에 있을 경우
            else:   #괄호 안에 문자열이 없을 경우 == 괄호가 없을 경우
                for l in range(1, len(langs)):
                    messages[l] += self.translator.translate(i, dest = langs[l], src = 'ko').text + '. '

        #한국어 ko 영어 en 중국어(간체) zh-cn 중국어(번체) zh-tw 일본어 ja
        if(site != ""):
            for l in range(0, len(langs)):  #추출했던 사이트 이어 붙이기
                messages[l] += site + ' '
        if(call != ""):
            for l in range(0, len(langs)):  #추출했던 전화 번호 이어 붙이기
                messages[l] += call + ' '

        return messages

    def message_db_save(self, messages, div, local, AREA, ID, index):
        langs = ['ko', 'en', 'zh-cn', 'ja']
        for i in range(len(messages)):
            area = AREA[index]
            area = re.sub('[^ㄱ-힗]', '', area)
            keyword = div[index]
            area = self.translator.translate(area, dest = langs[i], src = 'ko').text        #문자의 기관을 번역
            keyword = self.translator.translate(keyword, dest = langs[i], src = 'ko').text  #문자의 종류를 번역
            for j in local:
                self.Chatbot.create_insert_table(self.con, self.db_langs, self.db_label, self.db_types, 1, [i, messages[i], keyword, j, area, ID[index]]) #데이터 베이스에 번역된 문자열 저장
            print(messages[i])

    def message_send(self, ID, index):
        bot.post_num = self.post_num    #챗봇의 post_num을 방금 db에 저장한 가장 최근 재난 문자의 번호 - 1로 초기화
        bot.sendMessageWithSim()        #챗봇에 메시지 출력
        self.post_num = ID[index]       #시뮬레이션의 post_num을 방금 db에 저장한 가장 최근 재난 문자의 번호로 초기화
        bot.post_num = self.post_num    #챗봇의 post_num을 방금 db에 저장한 가장 최근 재난 문자의 번호로 초기화

    def randmessage(self):
        print('send message')
        self.Chatbot.create_insert_table(self.con, self.db_langs, self.db_label, self.db_types, 1, [0, '%s.안녕하세요. 테스트 용 메시지 입니다.(한국어)'%str(int(self.post_num)+1), '병', '충청북도', '충청북도', str(int(self.post_num)+1)])
        self.Chatbot.create_insert_table(self.con, self.db_langs, self.db_label, self.db_types, 1, [1, '%s.안녕하세요. 테스트 용 메시지 입니다.(영어)'%str(int(self.post_num)+1), '병', '충청북도', '충청북도', str(int(self.post_num)+1)])
        self.Chatbot.create_insert_table(self.con, self.db_langs, self.db_label, self.db_types, 1, [2, '%s.안녕하세요. 테스트 용 메시지 입니다.(중국어)'%str(int(self.post_num)+1), '병', '충청북도', '충청북도', str(int(self.post_num)+1)])
        self.Chatbot.create_insert_table(self.con, self.db_langs, self.db_label, self.db_types, 1, [3, '%s.안녕하세요. 테스트 용 메시지 입니다.(일본어)'%str(int(self.post_num)+1), '병', '충청북도', '충청북도', str(int(self.post_num)+1)])
        
        bot.sendMessageWithSim()
        self.post_num = self.Chatbot.post_number(self.con)
        bot.post_num = self.post_num
        self.count += 1
        if(self.count >= 150):
            self.count = self.Chatbot.remove_old_data(self.con)
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


bot = CornerstoneChatbot()
bot.updater.dispatcher.add_handler(bot.mainHandler)
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


