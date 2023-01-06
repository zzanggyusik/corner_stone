from sqlite3 import Error
import sqlite3

class ChatbotDB:
    def __init__(self) -> None:
        self.user_con = ''
        self.message_con = ''

    def conDB(self):
        self.user_con = self.user_connection()
        self.message_con = self.message_connection()
        self.create_table(self.user_con)

    def dbHandler(self, id, language, region):
        user_info = []                  
        langs = ['영어', '중국어', '일본어']
        user_info.extend([id, language, region])
        if(language in langs):
            self.insert_table(self.user_con, user_info[0], user_info[1], user_info[2])
            self.update_data(id)

    def user_connection(self):
        try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
            user_con = sqlite3.connect('user_db.db', check_same_thread=False)
            print("[DB] - user db file connect")
            return user_con
        except Error: # 에러 출력
            print(Error)

    def message_connection(self):
            try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
                message_con = sqlite3.connect('message_db.db', check_same_thread=False)
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
        if(self.check_data(con, id, language)):
            cursor_db.execute('INSERT INTO user_tb VALUES (?, ?, ?)', (id, language, region,))
            con.commit()
            print("[DB] - insert")
        else:
            print("[DB] - not_insert")

    def clear_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("DELETE FROM user_tb")
        con.commit()
        print("[DB] - clear")

    def disconnetion(self, con):
        con.close()
        print("[DB] - disconnet")

    def search_data(self, con, language, region, post_num, mode):
        serarch_data = []
        cursor_db = con.cursor()
        str_data = []
        print(language, region, 1)
        if language == '영어':
            cursor_db.execute("SELECT *FROM eng_tb WHERE region=? ORDER BY ROWID DESC LIMIT 1", (region,))
            str_data = cursor_db.fetchall()
            if len(str_data) == 0:
                serarch_data.append("Sorry, the latest disaster safety text does not exist.")
        elif language == '중국어':
            cursor_db.execute("SELECT *FROM ch_tb WHERE region=? ORDER BY ROWID DESC LIMIT 1", (region,))
            str_data = cursor_db.fetchall()
            if len(str_data) == 0:
                serarch_data.append("对不起，最近的灾难安全短信不存在。")
        elif language == '일본어':
            cursor_db.execute("SELECT *FROM jp_tb WHERE region=? ORDER BY ROWID DESC LIMIT 1", (region,))
            str_data = cursor_db.fetchall()
            if len(str_data) == 0:
                serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
        else:
            serarch_data.append("Sorry, This language is not serviced.")

        if(len(str_data) != 0):
            if(mode == 0):
                serarch_data.append(str_data[len(str_data)-1][0])
            elif(mode == 1):
                for i in range(0, len(str_data)):
                    if(str_data[i][2] > post_num):
                        serarch_data.append(str_data[i][0])
        print(str_data)
        print(serarch_data)
        print("[DB] - send complete")
        return serarch_data

    def visited_user(self, con, id):
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

    def check_data(self, con, id, language):
        cursor_db = con.cursor()
        cursor_db.execute("SELECT *FROM user_tb WHERE id=? AND language=?", (id,language,))
        check_data = cursor_db.fetchall()
        print(check_data)
        con.commit()
        if len(check_data) != 0:
            print("[DB] - check_data -> True")
            return False
        else:
            print("[DB] - check_data -> False")
            return True

    def user_language(self, con, id):
        use_language = []
        cursor_db = con.cursor()
        cursor_db.execute("select *from user_tb where id=?", (id,))
        user_data = cursor_db.fetchall()
        for i in range(0, len(user_data)):
            use_language.append(user_data[i][1])
        con.commit()
        print(f"[DB] - {id} -> {use_language}")
        return use_language
    
    def user_location(self, con, id):
        use_location = ''
        cursor_db = con.cursor()
        cursor_db.execute("select *from user_tb where id=?", (id,))
        user_data = cursor_db.fetchall()
        if(len(user_data) != 0):
            use_location = user_data[0][2]
        con.commit()
        print(f"[DB] - {id} -> {use_location}")
        return use_location
