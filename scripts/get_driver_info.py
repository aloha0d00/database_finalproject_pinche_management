from config.database import get_connection, close_connection

# 获取司机用户信息
def get_driver_info():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # 查询司机用户的详细信息
        cursor.execute('SELECT id, student_id, name, password, role FROM users WHERE student_id = %s', ('2021001',))
        user = cursor.fetchone()
        
        if user:
            print(f'司机用户信息：')
            print(f'ID: {user["id"]}')
            print(f'学号: {user["student_id"]}')
            print(f'姓名: {user["name"]}')
            print(f'角色: {user["role"]}')
            print(f'密码哈希: {user["password"]}')
            print(f'密码长度: {len(user["password"])}')
        else:
            print('未找到司机用户')
            
    finally:
        close_connection(conn)

if __name__ == '__main__':
    get_driver_info()