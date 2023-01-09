from sqlite3 import Error
import sqlite3

class ChatbotDB:
    def __init__(self) -> None:
        self.con = ''
        self.user_table = ['user_tb']
        self.lavel = ['id', 'language', 'region']
        self.types = ['INT', 'TEXT', 'TEXT']
        self.langs = ['영어', '중국어', '일본어']
        self.count_ = 0

    def dbHandler(self, id, language, region):
        user_info = []
        user_info.extend([id, language, region])
        if(language in self.langs):
            self.create_insert_table(self.con, self.user_table, self.lavel, self.types, 0, [user_info[0], user_info[1], user_info[2]])
            self.update_data(id)

    def connection(self):
            try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
                con = sqlite3.connect('corner_db.db', check_same_thread=False)
                print("[DB] - corner_db file connect")
                return con
            except Error: # 에러 출력
                print(Error)

    def create_insert_table(self, con, tb_name, tb_cols, tb_type, mode, value=None):
        if(self.count_ == 0):
            self.count_ = 1
            self.create_insert_table(con, self.user_table, self.lavel, self.types, 0)
            
        cursor_db = con.cursor()
        tb_table = []
        for i in range(len(tb_cols)):
            tb_table.append(tb_cols[i] + " " +  tb_type[i]) 

        table = ",".join(tb_table)
        for i in tb_name:
            cursor_db.execute(f"CREATE TABLE IF NOT EXISTS {i}({table})")
        print(f"[DB] - create {tb_name}")

        if(value == None):
            return
        col_name = ",".join(tb_cols)
        if(mode == 0):
            if(self.check_data(con, value[0], value[1])):
                values = ','.join(["'" + str(i) + "'" for i in value])
                cursor_db.execute(f'INSERT INTO {tb_name[0]}({col_name}) VALUES({values})')
        elif(mode == 1):
            value[1] = "\'\'".join(value[1].split("\'"))
            value[1] = "\"\"".join(value[1].split("\""))
            values = ','.join(["\'" + str(i) + "\'" for i in value[1:]])
            cursor_db.execute(f'INSERT INTO {tb_name[value[0]]}({col_name}) VALUES({values})')
        con.commit()
        print("[DB] - insert")

    def clear_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("DELETE FROM user_tb")
        con.commit()
        print("[DB] - clear")

    def delete_table(self, con, tb_name):
        cursor_db = con.cursor()
        for lang in tb_name:
            cursor_db.execute("DELETE FROM %s_tb"%lang)
        con.commit()

    ########
    #해당 언어 지우기
    def remove_data(self, con, id, language):
        cursor_db = con.cursor()
        cursor_db.execute("delete FROM user_tb WHERE id = ? AND language = ?", (id, language,))
        con.commit()
        print(f"[DB] - remove {id}:{language}")

    #수정 : id 해당 항 지우기
    def remove_id(self, con, id):
        cursor_db = con.cursor()
        cursor_db.execute("delete FROM user_tb WHERE id = ?", (id,))
        con.commit()
        print(f"[DB] - remove {id}")
    ########

    def disconnetion(self, con):
        con.close()
        print("[DB] - disconnet")

    def search_data(self, con, language, region, post_num, mode):
        serarch_data = []
        cursor_db = con.cursor()
        str_data = []
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
                    if(str_data[i][4] > post_num):
                        serarch_data.append(str_data[i][0])
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
        cusor_db = self.con.cursor()
        cusor_db.execute("SELECT *FROM user_tb WHERE id=?", (id,))
        find_data = cusor_db.fetchone()
        region_data = find_data[2]
        cusor_db.execute("update user_tb set region=? where region=?", (region_data, '',))
        self.con.commit()
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

    def post_number(self, con): #db에 저장된 재난 문자 중 가장 최근 문자의 번호를 반환
        cursor_db = con.cursor()
        cursor_db.execute("SELECT *FROM kr_tb ORDER BY ROWID DESC LIMIT 1")
        first_number = cursor_db.fetchall()
        if(len(first_number) == 0):   #만약 저장된 데이터가 없다면 '-1'을 반환
            return '-1'
        return first_number[0][4]

    def remove_old_data(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("SELECT count(*) from kr_tb")
        count = cursor_db.fetchone()
        count = count[0]
        
        if count >= 150:
            for i in range(4):
                command = "DELETE FROM %s_tb where number<%s"%(self.langs[i], str(int(self.post_num)-140))
                cursor_db.execute(command)
            count -= 10
        con.commit()
        return count