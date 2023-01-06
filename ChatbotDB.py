from sqlite3 import Error
import sqlite3

class ChatbotDB:
    def __init__(self) -> None:
        self.user_con = ''
        self.message_con = ''
        self.user_info = []  

    def conDB(self):
        self.user_con = self.user_connection()
        self.message_con = self.message_connection()
        #self.create_table(self.user_con)
        self.create_table(self.user_con, 'test_tb', ['info', 'feature', 'type', 'age'], ['TEXT', 'INT', "TEXT", "INT"])

    def dbHandler(self, id, language, region):                 
        self.user_info.extend([id, language, region])
        self.insert_table(self.user_con, self.user_info[0], self.user_info[1], self.user_info[2])

    # def dbdelHandler(self, id, lanuage, region):
    #     if not self.user_info:
    #         self.remove_data(self.user_con, self.user_info[0], self.user_info[1], self.user_info[2])

    # def dbdelHandler(self, id, language, region): 
    #     if region == None:
            

        # if not self.user_info:
        #     self.clear_row(self.user_con, self.user_info[0], self.user_info[1], self.user_info[2])

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

    # def create_table(self, con):
    #     cursor_db = con.cursor()
    #     cursor_db.execute("CREATE TABLE IF NOT EXISTS user_tb(id INT, language TEXT, region TEXT)")
    #     con.commit()
    #     print("[DB] - create")

    def create_table(self, con, tb_name, tb_cols, tb_types):
        cursor_db = con.cursor()
        tb_list = []
        for i in range(len(tb_cols)):
            tb_list.append(tb_cols[i] + ' ' + tb_types[i])
        table = ",".join(tb_list)
        cursor_db.execute(f"CREATE TABLE IF NOT EXISTS {tb_name}({table})")
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

    #원하는 행 삭제
    def clear_row(self, con, id, language, region):
        cursor_db = con.cursor()
        cursor_db.excute('DLETE FROM stock WHERE data (?, ?, ?)',(id, language, region,))
        cursor_db.excute('SELECT *From stock')
        cursor.fetchall()
        con.commit()
    ###

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
        cursor_db = con.cursor()
        cursor_db.execute("SELECT *FROM user_tb WHERE id=?", (id,))
        data = cursor_db.fetchall()
        if len(data) != 0:
            print("[DB] - ID exist")
            return True
        else:
            print("[DB] - ID not exist")
            return False

    def remove_data(self, con, id, language):
        cursor_db = con.cursor()
        cursor_db.execute("delete FROM user_tb WHERE id = ? AND language = ?", (id, language,))
        con.commit()
        print(f"[DB] - remove {id}:{language}")