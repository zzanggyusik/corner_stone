from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
from telegram import *
from telegram.ext import *
from TestChatbot import *
import random


class PEx(BehaviorModelExecutor):
    Queue = []
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)
        self.driver1 = webdriver.Chrome("chromedriver")  #크롬 드라이버 객체 생성
        self.driver2 = webdriver.Chrome("chromedriver")  #크롬 드라이버 객체 생성
        self.count = bot.chatbot_db.remove_old_data() #데이터 베이스의 데이터 갯수 저장
        self.languages = ['ko', 'en', 'zh-CN', 'ja', 'vi']
        
        self.insert_input_port("start")

    def ext_trans(self,port, msg):
        if port == "start":
            print("[Start]: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end = '\n\n')
            self._cur_state = "Generate"

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
                    self.message_send(local, ID, index)                         #메시지 보내기
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
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


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


