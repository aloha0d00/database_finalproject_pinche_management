import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='carpool_db'
)

try:
    with conn.cursor() as cursor:
        # 查询最新的5条行程记录
        cursor.execute('SELECT * FROM trips ORDER BY created_at DESC LIMIT 5')
        results = cursor.fetchall()
        
        print('最新的行程记录:')
        for row in results:
            print(row)
            
        # 检查行程数量
        cursor.execute('SELECT COUNT(*) FROM trips')
        total = cursor.fetchone()[0]
        print(f'\n总行程数: {total}')
        
finally:
    conn.close()