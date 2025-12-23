from config.database import get_connection, close_connection

# 使用应用程序的数据库连接函数
try:
    connection = get_connection()
    with connection.cursor() as cursor:
        # 查询最新的5条行程记录
        cursor.execute('SELECT * FROM trips ORDER BY created_at DESC LIMIT 5')
        results = cursor.fetchall()
        
        print('最新的行程记录:')
        for row in results:
            print(row)
            
        # 检查行程数量
        cursor.execute('SELECT COUNT(*) AS total FROM trips')
        total = cursor.fetchone()['total']
        print(f'\n总行程数: {total}')
        
        # 检查司机的车辆信息
        cursor.execute('SELECT * FROM vehicles WHERE user_id = (SELECT id FROM users WHERE phone = "13800138001")')
        vehicles = cursor.fetchall()
        print(f'\n司机13800138001的车辆信息:')
        for vehicle in vehicles:
            print(vehicle)
            
finally:
    close_connection(connection)