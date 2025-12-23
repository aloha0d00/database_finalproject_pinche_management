#!/usr/bin/env python3
"""
校园拼车平台快速部署脚本
支持在任何安装了Python和MySQL的计算机上部署
MySQL密码固定为：123123
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'carpool_user',
    'password': '123123',
    'name': 'carpool_db'
}

# 检查Python版本
def check_python_version():
    logger.info("检查Python版本...")
    if sys.version_info < (3, 10):
        logger.error("需要Python 3.10或更高版本")
        sys.exit(1)
    logger.info(f"Python版本: {platform.python_version()} ✓")
    return True

# 安装依赖
def install_dependencies():
    logger.info("安装项目依赖...")
    requirements_file = PROJECT_ROOT / "requirements.txt"
    
    if not requirements_file.exists():
        logger.error("requirements.txt文件不存在")
        sys.exit(1)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=PROJECT_ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.info("依赖安装成功 ✓")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"依赖安装失败: {e.stderr}")
        sys.exit(1)

# 检查MySQL连接
def check_mysql_connection():
    logger.info("检查MySQL连接...")
    try:
        import pymysql
        
        # 尝试连接到MySQL服务器
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user='root',  # 使用root用户连接
            password=DB_CONFIG['password'],  # 用户指定的固定密码
            charset='utf8mb4',
            connect_timeout=5
        )
        connection.close()
        logger.info("MySQL连接成功 ✓")
        return True
    except pymysql.MySQLError as e:
        logger.error(f"MySQL连接失败: {e}")
        logger.error("请确保MySQL服务正在运行，且密码为123123")
        sys.exit(1)

# 设置数据库
def setup_database():
    logger.info("设置数据库...")
    import pymysql
    
    try:
        # 连接到MySQL服务器
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user='root',
            password=DB_CONFIG['password'],
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 创建数据库用户
        cursor.execute(f"CREATE USER IF NOT EXISTS '{DB_CONFIG['user']}'@'localhost' IDENTIFIED BY '{DB_CONFIG['password']}'")
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['name']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # 授予权限
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_CONFIG['name']}.* TO '{DB_CONFIG['user']}'@'localhost'")
        
        # 刷新权限
        cursor.execute("FLUSH PRIVILEGES")
        
        cursor.close()
        connection.close()
        logger.info("数据库设置成功 ✓")
        return True
    except pymysql.MySQLError as e:
        logger.error(f"数据库设置失败: {e}")
        sys.exit(1)

# 配置环境变量
def configure_environment():
    logger.info("配置环境变量...")
    env_file = PROJECT_ROOT / ".env"
    
    env_content = f"""
DB_HOST={DB_CONFIG['host']}
DB_USER={DB_CONFIG['user']}
DB_PASSWORD={DB_CONFIG['password']}
DB_NAME={DB_CONFIG['name']}

# JWT配置
JWT_SECRET=carpool_secret_key_2025
JWT_EXPIRES_IN=24h

# 服务器配置
PORT=3000
DEBUG=True
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        logger.info("环境变量配置成功 ✓")
        return True
    except IOError as e:
        logger.error(f"环境变量配置失败: {e}")
        sys.exit(1)

# 初始化数据库表
def init_database_tables():
    logger.info("初始化数据库表...")
    
    try:
        # 导入数据库初始化函数
        sys.path.append(str(PROJECT_ROOT))
        from config.database import ensure_tables_exist, test_connection
        
        # 测试应用数据库连接
        if not test_connection():
            logger.error("应用数据库连接失败")
            sys.exit(1)
        
        # 确保表存在
        if ensure_tables_exist():
            logger.info("数据库表初始化成功 ✓")
            return True
        else:
            logger.error("数据库表初始化失败")
            sys.exit(1)
    except Exception as e:
        logger.error(f"数据库表初始化失败: {e}")
        logger.error("请检查数据库配置和权限")
        sys.exit(1)

# 创建默认管理员账户
def create_default_admin():
    logger.info("创建默认管理员账户...")
    
    try:
        import pymysql
        from utils.auth_utils import hash_password
        
        # 连接到应用数据库
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['name'],
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 检查管理员账户是否已存在
        cursor.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
        if cursor.fetchone():
            logger.info("默认管理员账户已存在，跳过创建")
            cursor.close()
            connection.close()
            return True
        
        # 创建默认管理员账户
        hashed_password = hash_password("admin123")
        cursor.execute("""
            INSERT INTO users (name, phone, password, role, status) 
            VALUES (%s, %s, %s, %s, %s)
        """, ("管理员", "13800138000", hashed_password, "admin", "active"))
        
        connection.commit()
        cursor.close()
        connection.close()
        logger.info("默认管理员账户创建成功 ✓")
        logger.info("管理员账户: 13800138000, 密码: admin123")
        return True
    except Exception as e:
        logger.error(f"默认管理员账户创建失败: {e}")
        logger.error("跳过管理员账户创建")
        return False

# 启动应用
def start_application():
    logger.info("启动应用...")
    logger.info("=" * 50)
    logger.info("校园拼车平台部署完成!")
    logger.info(f"访问地址: http://localhost:{os.getenv('PORT', '3000')}")
    logger.info("管理员账户: 13800138000, 密码: admin123")
    logger.info("按 Ctrl+C 停止应用")
    logger.info("=" * 50)
    
    try:
        # 使用Flask内置服务器启动应用
        subprocess.run(
            [sys.executable, "main.py"],
            cwd=PROJECT_ROOT,
            check=True
        )
    except KeyboardInterrupt:
        logger.info("应用已停止")
    except subprocess.CalledProcessError as e:
        logger.error(f"应用启动失败: {e}")
        sys.exit(1)

# 主部署函数
def main():
    logger.info("=" * 50)
    logger.info("校园拼车平台快速部署脚本")
    logger.info("=" * 50)
    
    # 执行部署步骤
    check_python_version()
    install_dependencies()
    check_mysql_connection()
    setup_database()
    configure_environment()
    init_database_tables()
    create_default_admin()
    
    # 启动应用
    start_application()

if __name__ == "__main__":
    main()
