import os
import logging
import time
import pymysql
from pymysql import cursors
from dotenv import load_dotenv

"""
数据库配置和连接池管理模块
"""

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'carpool_db'),
    'charset': 'utf8mb4',
    'cursorclass': cursors.DictCursor,
    'autocommit': True,
    'init_command': "SET time_zone = '+8:00'"
}

# 连接池配置
POOL_CONFIG = {
    'pool_name': 'carpool_pool',
    'pool_size': 5,
    'max_overflow': 10,
    'pool_pre_ping': True
}

class ConnectionPool:
    """简单的数据库连接池实现"""
    def __init__(self):
        self.pool = []
        self.pool_size = POOL_CONFIG['pool_size']
        self.max_overflow = POOL_CONFIG['max_overflow']
        self.current_size = 0
        self.lock = False
        self._init_pool()
    
    def _init_pool(self):
        """初始化连接池"""
        for _ in range(self.pool_size):
            try:
                conn = self._create_connection()
                self.pool.append(conn)
                self.current_size += 1
            except Exception as e:
                logger.error(f"初始化连接池失败: {e}")
    
    def _create_connection(self):
        """创建数据库连接"""
        return pymysql.connect(**DB_CONFIG)
    
    def get_connection(self):
        """从连接池获取连接"""
        while self.lock:
            time.sleep(0.01)
        
        self.lock = True
        try:
            if self.pool:
                return self.pool.pop()
            elif self.current_size < self.pool_size + self.max_overflow:
                conn = self._create_connection()
                self.current_size += 1
                return conn
            else:
                raise Exception("连接池已满")
        finally:
            self.lock = False
    
    def return_connection(self, conn):
        """将连接返回连接池"""
        if conn and conn.open:
            try:
                conn.ping()
                self.pool.append(conn)
            except Exception:
                conn.close()
                self.current_size -= 1
        elif conn:
            conn.close()
            self.current_size -= 1

# 全局连接池实例
db_pool = ConnectionPool()

def get_connection():
    """获取数据库连接"""
    return db_pool.get_connection()

def close_connection(conn):
    """关闭数据库连接（返回连接池）"""
    db_pool.return_connection(conn)

def test_connection():
    """测试数据库连接"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        close_connection(conn)
        return result['1'] == 1
    except Exception as e:
        logger.error(f"数据库连接测试失败: {e}")
        return False

def ensure_tables_exist():
    """确保所有必要的表存在"""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # 创建用户表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(20) NULL UNIQUE,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(100),
            password VARCHAR(255) NOT NULL,
            avatar VARCHAR(255),
            role ENUM('student', 'driver', 'admin') NOT NULL DEFAULT 'student',
            rating FLOAT DEFAULT 5.0,
            total_ratings INT DEFAULT 0,
            status ENUM('active', 'inactive', 'banned') NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 创建车辆表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            plate_number VARCHAR(20) NOT NULL UNIQUE,
            brand VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            color VARCHAR(20) NOT NULL,
            seats INT NOT NULL DEFAULT 5,
            year INT,
            status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 创建行程表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            driver_id INT NOT NULL,
            vehicle_id INT NOT NULL,
            departure_location VARCHAR(255) NOT NULL,
            arrival_location VARCHAR(255) NOT NULL,
            departure_time DATETIME NOT NULL,
            available_seats INT NOT NULL,
            price_per_seat DECIMAL(10, 2) NOT NULL,
            trip_status ENUM('pending', 'ongoing', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
            description TEXT,
            departure_latitude FLOAT,
            departure_longitude FLOAT,
            arrival_latitude FLOAT,
            arrival_longitude FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 创建参与者表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_id INT NOT NULL,
            user_id INT NOT NULL,
            seats_booked INT NOT NULL DEFAULT 1,
            participant_status ENUM('pending', 'accepted', 'rejected', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
            payment_status ENUM('unpaid', 'paid', 'refunded') NOT NULL DEFAULT 'unpaid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_participant (trip_id, user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 提交事务
        connection.commit()
        logger.info("所有表已创建或确认存在")
        return True
        
    except pymysql.Error as err:
        logger.error(f"创建表失败: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)
