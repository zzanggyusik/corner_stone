from sqlite3 import Error
import sqlite3

'''
2023-01-07 00:55 변경사항.
    1. check_data() 추가
        챗봇에서 '/option' 기능을 통해 언어를 변경할 경우, DB에 저장하는 과정에서
        기존에 있는 언어임에도 새롭게 추가되는 현상 해결을 위해
        ex) user_id     language        location
            1234        일본어          대전광역시
            1234        영어            대전광역시
            1234        일본어          대전광역시  <--- 일본어가 이미 있음에도 중복돼서 들어감
    2. check_data() 내부 조건 변경
        기존 : if len(check_data) != 0:
        변경 : if check_data != None:
        변경 이유 : check_data = cursor_db.fetchone() 과정에서, 중복되는 언어가 존재하지 않으면
                    cursor_db.fetchone()이 None을 반환하여 check_data는 None 상태가 됨.
                    따라서, 기존 코드는 중복된 언어가 존재하지 않을 경우에 lne(None) != 0을 의미하기 때문에
                    문법적 오류가 있기 때문임
    3. dbHandler() 내부 변경
        if self.check_data(self.user_con, id, language) == False: 추가
        추가 이유 : 기존에는 전달받은 언어가 DB에 저장 여부에 상관없이 무조건 추가하도록 함.
                    따라서, 위 조건을 추가하여 전달 받은 언어가 DB에 이미 저장되어 있는지를 판단하고,
                    존재하지 않을 경우에만(self.check_data()가 False를 반환) DB에 저장하도록 하기 위함
'''

class ChatbotDB:
    def __init__(self) -> None:
        self.user_con = ''
        self.message_con = ''

    def conDB(self):
        self.user_con = self.user_connection()
        self.message_con = self.message_connection()
        self.create_table(self.user_con)

    def dbHandler(self, id, language, region):
        if self.check_data(self.user_con, id, language) == False:
            user_info = []                
            user_info.extend([id, language, region])
            self.insert_table(self.user_con, user_info[0], user_info[1], user_info[2])
            self.update_data(id)

    def user_connection(self):
        try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
            user_con = sqlite3.connect('user_db.db')
            print("[DB] - user db file connect")
            return user_con
        except Error: # 에러 출력
            print(Error)

    def message_connection(self):
            try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
                message_con = sqlite3.connect('message_db.db')
                print("[DB] - message db file connect")
                return message_con
            except Error: # 에러 출력
                print(Error)

    def create_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("CREATE TABLE IF NOT EXISTS user_tb(id INT, language TEXT, region TEXT)")
        con.commit()
        print("[DB] - create")

    def insert_table(self, con, id, language, region):
        cursor_db = con.cursor()
        cursor_db.execute('INSERT INTO user_tb VALUES (?, ?, ?)', (id, language, region,))
        con.commit()
        print("[DB] - insert")

    def clear_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("DELETE FROM user_tb")
        con.commit()
        print("[DB] - clear")

    def disconnetion(self, con):
        con.close()
        print("[DB] - disconnet")

    def search_data(self, con, language, region):
        serarch_data = []
        cursor_db = con.cursor()
        print(language, region)
        if region == "대전광역시":
            if language == "영어":
                cursor_db.execute("SELECT *FROM eng_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("Sorry, the latest disaster safety text does not exist.")
            elif language == "일본어":
                cursor_db.execute("SELECT *FROM jp_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
            elif language == "중국어":
                cursor_db.execute("SELECT *FROM ch_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("对不起，最近的灾难安全短信不存在。")

        elif region == "충청북도":
            if language == "영어":
                cursor_db.execute("SELECT *FROM eng_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("Sorry, the latest disaster safety text does not exist.")
            elif language == "일본어":
                cursor_db.execute("SELECT *FROM jp_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
            elif language == "중국어":
                cursor_db.execute("SELECT *FROM ch_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("对不起，最近的灾难安全短信不存在。")
        else:
            if language == "영어":
                serarch_data.append("Sorry, the latest disaster safety text does not exist.")
            elif language == "일본어":
                serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
            else: # 중국어
                serarch_data.append("对不起，最近的灾难安全短信不存在。")
        print("[DB] - send complete")
        return serarch_data

    def visited_user(self, con, id):
        print('visited_user')
        cursor_db = con.cursor()
        cursor_db.execute("SELECT *FROM user_tb WHERE id=?", (id,))
        data = cursor_db.fetchall()
        if len(data) != 0:
            print("[DB] - ID exist")
            return True
        else:
            print("[DB] - ID not exist")
            return False

    def update_data(self, id):
        cusor_db = self.user_con.cursor()
        cusor_db.execute("SELECT *FROM user_tb WHERE id=?", (id,))
        find_data = cusor_db.fetchone()
        region_data = find_data[2]
        cusor_db.execute("update user_tb set region=? where region=?", (region_data, '',))
        self.user_con.commit()
        print(f"[DB] - update {id} -> {region_data}")

    def remove_data(self, con, id, language):
        cursor_db = con.cursor()
        cursor_db.execute("delete FROM user_tb WHERE id = ? AND language = ?", (id, language,))
        con.commit()
        print(f"[DB] - remove {id}:{language}")

    def check_data(self, con, id, language):
        print('Enter check_data')
        cursor_db = con.cursor()
        cursor_db.execute("SELECT *FROM user_tb WHERE id=? AND language=?", (id,language,))
        check_data = cursor_db.fetchone()
        print(check_data)
        con.commit()
        if check_data != None:  # DB에 동일한 언어를 갖는 테이블이 있음
            print("[DB] - check_data -> True")
            return True
        else:   # DB에 동일한 언어를 갖는 테이블이 없음
            print("[DB] - check_data -> False")
            return False