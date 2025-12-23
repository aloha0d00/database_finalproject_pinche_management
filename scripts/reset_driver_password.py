from config.database import get_connection, close_connection
from utils.auth_utils import hash_password

# 重置司机用户密码
def reset_driver_password():
    conn = get_connection()
    try:
        # 设置司机密码为 'driver123'
        new_password = 'driver123'
        hashed_password = hash_password(new_password)
        
        cursor = conn.cursor()
        # 更新司机用户的密码
        cursor.execute(
            'UPDATE users SET password = %s WHERE student_id = %s', 
            (hashed_password, '2021001')
        )
        
        conn.commit()
        print(f'司机用户密码已重置为: {new_password}')
        print(f'新密码哈希: {hashed_password}')
        print(f'密码哈希长度: {len(hashed_password)}')
        
    finally:
        close_connection(conn)

if __name__ == '__main__':
    reset_driver_password()