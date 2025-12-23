import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'carpool_db'),
    'charset': 'utf8mb4'
}

def main():
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 修改users表，将student_id字段改为允许为空
        alter_query = "ALTER TABLE users MODIFY COLUMN student_id VARCHAR(20) NULL UNIQUE;"
        cursor.execute(alter_query)
        connection.commit()
        
        print("表结构修改成功：users表的student_id字段已改为允许为空")
        
    except Exception as e:
        print(f"修改表结构失败：{e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    main()