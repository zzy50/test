import pymysql

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PW = 'password'
DB_NAME = "AVC_DB"
RAW_DATA_TABLE = "AVC_TABLE"

class DB(): 
    def __init__(self) -> None:
        self.DB_conn = pymysql.connect(
            host= DB_HOST, port = DB_PORT,
            user = DB_USER, passwd = DB_PW,
            db =DB_NAME)
        self.DB_cur = self.DB_conn.cursor()

    def fetch_table_data(self, table_name):
        # 테이블의 모든 데이터를 가져오는 쿼리
        query = f"SELECT * FROM {table_name}"
        self.DB_cur.execute(query)
        
        # 컬럼 이름 가져오기
        columns = [desc[0] for desc in self.DB_cur.description]
        
        # 데이터 가져오기
        data = self.DB_cur.fetchall()
        
        return columns, data

    def close(self):
        self.DB_cur.close()
        self.DB_conn.close()

db = DB()

# AVC_TABLE의 컬럼 및 데이터 가져오기
columns, data = db.fetch_table_data(RAW_DATA_TABLE)

# 컬럼 이름 출력
print("Columns:", columns)

# 데이터 출력
for row in data:
    print(row)

# DB 연결 종료
db.close()
