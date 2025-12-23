import os
import logging
import pymysql
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from routes.user_routes import user_bp
from routes.trip_routes import trip_bp
from routes.participant_routes import participant_bp
from routes.vehicle_routes import vehicle_bp
from routes.admin_routes import admin_bp
from config.database import ensure_tables_exist, test_connection, DB_CONFIG
from utils.auth_utils import hash_password

"""
Carpool API 主应用入口
"""

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 配置CORS
CORS(app)

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(trip_bp, url_prefix='/api')
app.register_blueprint(participant_bp, url_prefix='/api')
app.register_blueprint(vehicle_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# 测试数据库连接
def test_db_connection():
    logger.info("正在测试数据库连接...")
    if test_connection():
        logger.info("数据库连接测试成功!")
        return True
    else:
        logger.error("数据库连接测试失败!")
        return False

# 初始化数据库表
def init_database():
    logger.info("正在初始化数据库表...")
    if ensure_tables_exist():
        logger.info("数据库表初始化成功!")
        return True
    else:
        logger.error("数据库表初始化失败!")
        return False

# 创建默认管理员账户
def ensure_admin_exists():
    logger.info("检查默认管理员账户...")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
        if cursor.fetchone():
            logger.info("默认管理员账户已存在，跳过创建")
            return True
        hashed_password = hash_password("admin123")
        cursor.execute("""
            INSERT INTO users (name, phone, password, role, status)
            VALUES (%s, %s, %s, %s, %s)
        """, ("管理员", "13800138000", hashed_password, "admin", "active"))
        connection.commit()
        logger.info("默认管理员账户创建成功")
        return True
    except Exception as e:
        logger.error(f"创建默认管理员账户失败: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# 健康检查路由
@app.route('/health', methods=['GET'])
def health_check():
    return {
        "status": "ok",
        "message": "Carpool API is running!"
    }

# 提供首页
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    # 启动应用前进行数据库检查和初始化
    test_db_connection()
    init_database()
    ensure_admin_exists()
    
    # 启动Flask应用
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"启动Carpool API服务，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
