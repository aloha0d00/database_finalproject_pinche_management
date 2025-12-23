import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_connection, close_connection

def alter_participants_index():
    """修改participants表的索引，使其包含participant_status字段"""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # 先添加单独的trip_id和user_id索引
        cursor.execute("ALTER TABLE participants ADD INDEX idx_trip_id (trip_id)")
        cursor.execute("ALTER TABLE participants ADD INDEX idx_user_id (user_id)")
        
        # 然后删除旧的unique_participant索引
        cursor.execute("ALTER TABLE participants DROP INDEX unique_participant")
        
        # 创建新的unique_participant索引，包含participant_status字段
        cursor.execute("ALTER TABLE participants ADD UNIQUE KEY unique_participant (trip_id, user_id, participant_status)")
        
        connection.commit()
        print("成功修改participants表的unique_participant索引，现在包含participant_status字段")
        return True
        
    except Exception as e:
        print(f"修改participants表索引失败: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)

if __name__ == "__main__":
    alter_participants_index()