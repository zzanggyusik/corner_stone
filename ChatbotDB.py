from sqlite3 import Error
import sqlite3
from pytrans import PEx

class ChatbotDB:
    def __init__(self) -> None:
        self.user_id = ''
        self.user_region = ''
        self.user_language_code = ''
        self.con = self.connection()

        self.user_table = ['user_tb']
        self.user_cols = ['id', 'language', 'region']
        self.user_types = ['INT', 'TEXT', 'TEXT']
        
        self.message_table = ['kr_tb']
        self.message_cols = ['info', 'keyword', 'region', 'area', 'number']
        self.message_types = ['TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT']

        self.langs = [None, '영어', '중국어', '일본어']
        self.langs_code = ['', 'en', 'zh-CN', 'ja']
        self.create_table()
        self.post_num = self.post_number()
        self.count_ = 0

    def connection(self):
            try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
                con = sqlite3.connect('corner_db.db', check_same_thread=False)
                print("[DB] - corner_db file connect")
                return con
            except Error: # 에러 출력
                print(Error)

    def create_table(self): #테이블 생성
        tables = [self.user_table, self.message_table]
        cols = [self.user_cols, self.message_cols]
        types = [self.user_types, self.message_types]

        cursor_db = self.con.cursor()
        for num in range(len(tables)):
            tb_table = []
            for i in range(len(cols[num])):
                tb_table.append(cols[num][i] + " " +  types[num][i]) 

            table = ",".join(tb_table)
            for i in tables[num]:
                cursor_db.execute(f"CREATE TABLE IF NOT EXISTS {i}({table})")
            print(f"[DB] - create {tables[num]}")
        self.con.commit()

    def insert_table(self, mode=0, value=None): #테이블에 데이터 추가
        cursor_db = self.con.cursor()
        if(mode == 0): #챗봇 모드
            col_name = ",".join(self.user_cols)
            if(self.check_data()):
                pass
            else:
                self.remove_data()
            values = ','.join(["'" + str(i) + "'" for i in [self.user_id, self.user_language_code, self.user_region]])
            cursor_db.execute(f'INSERT INTO {self.user_table[0]}({col_name}) VALUES({values})')
        elif(mode == 1): #시뮬 모드
            col_name = ",".join(self.message_cols)
            value[0] = "\'\'".join(value[0].split("\'"))
            value[0] = "\"\"".join(value[0].split("\""))
            values = ','.join(["\'" + str(i) + "\'" for i in value])
            cursor_db.execute(f'INSERT INTO {self.message_table[0]}({col_name}) VALUES({values})')
        print("[DB] - insert")
        self.con.commit()

    def clear_table(self):
        cursor_db = self.con.cursor()
        cursor_db.execute("DELETE FROM user_tb")
        self.con.commit()
        print("[DB] - clear")

    def delete_table(self, tb_name):
        cursor_db = self.con.cursor()
        for lang in tb_name:
            cursor_db.execute("DELETE FROM %s_tb"%lang)
        self.con.commit()

    def disconnetion(self):
        self.con.close()
        print("[DB] - disconnet")

    def search_data(self, mode):
        serarch_data = []
        cursor_db = self.con.cursor()
        str_data = []
        cursor_db.execute("SELECT *FROM kr_tb WHERE region=? ORDER BY ROWID DESC LIMIT 1", (self.user_region,))
        str_data = cursor_db.fetchall()

        if(len(str_data) != 0):
            if(mode == 0):
                message = PEx.TransMessage([str_data[0][0]], 'ko', self.user_language_code)
                serarch_data.append(message[0])
            elif(mode == 1):
                for i in range(0, len(str_data)):
                    if(str_data[i][4] > self.post_num):
                        message = PEx.TransMessage(str_data[i][0], 'ko', self.user_language_code)
                        serarch_data.append(message[0])
        else:
            serarch_data.append("Sorry, the latest disaster safety text does not exist.")

        print("[DB] - send complete")
        return serarch_data

    def visited_user(self):
        cursor_db = self.con.cursor()
        cursor_db.execute("SELECT *FROM user_tb WHERE id=?", (self.user_id,))
        data = cursor_db.fetchall()
        if len(data) != 0:
            print("[DB] - ID exist")
            return True
        else:
            print("[DB] - ID not exist")
            return False

    def update_data(self):
        cusor_db = self.con.cursor()
        cusor_db.execute("SELECT *FROM user_tb WHERE id=?", (self.user_id,))
        find_data = cusor_db.fetchone()
        region_data = find_data[2]
        cusor_db.execute("update user_tb set region=? where region=?", (region_data, '',))
        self.con.commit()
        print(f"[DB] - update {id} -> {region_data}")

    def check_data(self):
        cursor_db = self.con.cursor()
        cursor_db.execute("SELECT *FROM user_tb WHERE id=?", (self.user_id,))
        check_data = cursor_db.fetchall()
        print(check_data)
        self.con.commit()
        if len(check_data) != 0:
            print("[DB] - check_data -> True")
            return False
        else:
            print("[DB] - check_data -> False")
            return True

    def get_user_language(self):
        user_language = ''
        cursor_db = self.con.cursor()
        cursor_db.execute("select *from user_tb where id=?", (self.user_id,))
        user_data = cursor_db.fetchall()
        if(len(user_data) != 0):
            user_language = user_data[0][1]
        self.con.commit()
        print(f"[DB] - {id} -> {user_language}")
        self.user_language_code = user_language
    
    def get_user_location(self):
        user_location = ''
        cursor_db = self.con.cursor()
        cursor_db.execute("select *from user_tb where id=?", (self.user_id,))
        user_data = cursor_db.fetchall()
        if(len(user_data) != 0):
            user_location = user_data[0][2]
        self.con.commit()
        print(f"[DB] - {id} -> {user_location}")
        self.user_region = user_location

    def post_number(self): #db에 저장된 재난 문자 중 가장 최근 문자의 번호를 반환
        cursor_db = self.con.cursor()
        cursor_db.execute("SELECT *FROM kr_tb ORDER BY ROWID DESC LIMIT 1")
        first_number = cursor_db.fetchall()
        if(len(first_number) == 0):   #만약 저장된 데이터가 없다면 '-1'을 반환
            return '-1'
        return first_number[0][4]

    def remove_old_data(self):
        cursor_db = self.con.cursor()
        cursor_db.execute("SELECT count(*) from kr_tb")
        count = cursor_db.fetchone()
        count = count[0]
        
        if count >= 150:
            command = "DELETE FROM kr_tb where number<%s"%(str(int(self.post_num)-140))
            cursor_db.execute(command)
            count -= 10
        self.con.commit()
        return count

    def remove_data(self):
        cursor_db = self.con.cursor()
        cursor_db.execute("delete FROM user_tb WHERE id = ?", (self.user_id,))
        self.con.commit()
        print(f"[DB] - remove {self.user_id}")