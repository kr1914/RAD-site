import sqlite3
import os
from datetime import datetime

# 데이터베이스 경로 설정
db_folder = 'store/DB/storage'
db_file = 'local_database.db'
db_path = os.path.join(db_folder, db_file)

# 폴더가 존재하지 않으면 생성
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# 데이터베이스 연결 및 테이블 생성
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 테이블이 존재하지 않으면 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        ID TEXT PRIMARY KEY,
        category TEXT,
        content TEXT,
        creator TEXT,
        created_at TEXT,
        modifier TEXT,
        modified_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

# 데이터 저장 함수
def insert_log(log_id, category, content, creator, created_at, modifier, modified_at):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO logs (ID, category, content, creator, created_at, modifier, modified_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (log_id, category, content, creator, created_at, modifier, modified_at))
    
    conn.commit()
    conn.close()

# 데이터 조회 함수
def select_logs():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM logs')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

# 데이터 업데이트 함수
def update_log(log_id, category=None, content=None, modifier=None, modified_at=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if not modified_at:
        modified_at = datetime.now().strftime('%Y%m%d%H%M%S')
    
    update_fields = []
    update_values = []
    
    if category:
        update_fields.append('category = ?')
        update_values.append(category)
    if content:
        update_fields.append('content = ?')
        update_values.append(content)
    if modifier:
        update_fields.append('modifier = ?')
        update_values.append(modifier)
    update_fields.append('modified_at = ?')
    update_values.append(modified_at)
    update_values.append(log_id)
    
    set_clause = ', '.join(update_fields)
    cursor.execute(f'UPDATE logs SET {set_clause} WHERE ID = ?', update_values)
    
    conn.commit()
    conn.close()

# 데이터 삭제 함수
def delete_log(log_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM logs WHERE ID = ?', (log_id,))
    
    conn.commit()
    conn.close()

# 로그 데이터 추가 예시
if __name__ == "__main__":
    init_db()
    log_id = "202407271505000001"
    category = "로그"
    content = "최초등록"
    creator = "System"
    created_at = datetime.now().strftime('%Y%m%d%H%M%S')
    modifier = "System"
    modified_at = created_at
    
    insert_log(log_id, category, content, creator, created_at, modifier, modified_at)
    
    # 데이터 조회 예시
    logs = select_logs()
    for log in logs:
        print(log)
    
    # 데이터 업데이트 예시
    update_log(log_id, content="업데이트된 내용", modifier="Updater")
    
    # 데이터 삭제 예시
    delete_log(log_id)
