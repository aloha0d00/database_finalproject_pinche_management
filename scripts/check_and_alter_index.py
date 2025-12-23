import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_connection, close_connection

def check_and_alter_index():
    """检查并修改participants表的索引"""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # 检查当前索引状态
        print("当前participants表的索引:")
        cursor.execute("SHOW INDEXES FROM participants")
        indexes = cursor.fetchall()
        for index in indexes:
            print(f"  索引名: {index['Key_name']}, 列: {index['Column_name']}, 唯一: {index['Non_unique'] == 0}")
        
        # 检查是否存在旧的unique_participant索引
        has_old_index = any(index['Key_name'] == 'unique_participant' for index in indexes)
        
        if has_old_index:
            # 直接删除旧索引
            cursor.execute("ALTER TABLE participants DROP INDEX unique_participant")
            print("已删除旧的unique_participant索引")
        
        # 创建新的索引
        cursor.execute("ALTER TABLE participants ADD UNIQUE KEY unique_participant (trip_id, user_id, participant_status)")
        print("已创建新的unique_participant索引，包含participant_status字段")
        
        # 再次检查索引状态
        print("\n修改后的participants表索引:")
        cursor.execute("SHOW INDEXES FROM participants")
        indexes = cursor.fetchall()
        for index in indexes:
            print(f"  索引名: {index['Key_name']}, 列: {index['Column_name']}, 唯一: {index['Non_unique'] == 0}")
        
        connection.commit()
        return True
        
    except Exception as e:
        print(f"操作失败: {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)

if __name__ == "__main__":
    check_and_alter_index()