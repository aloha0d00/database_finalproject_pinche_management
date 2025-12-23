from config.database import get_connection, close_connection

# 查询现有用户
def check_users():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, student_id, name, role FROM users')
        users = cursor.fetchall()
        print('现有用户：')
        for user in users:
            print(f'ID: {user["id"]}, 学号: {user["student_id"]}, 姓名: {user["name"]}, 角色: {user["role"]}')
    finally:
        close_connection(conn)

if __name__ == '__main__':
    check_users()