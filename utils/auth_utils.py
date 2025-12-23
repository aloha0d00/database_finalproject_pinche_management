import os
import logging
from datetime import datetime, timedelta
import bcrypt
import jwt
from dotenv import load_dotenv

"""
认证工具模块，包含密码加密、验证和JWT令牌生成、验证功能
"""

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT配置
JWT_SECRET = os.getenv('JWT_SECRET', 'your_jwt_secret_key')
JWT_EXPIRES_IN = os.getenv('JWT_EXPIRES_IN', '24h')

# 解析JWT过期时间
def _parse_expires_in(expires_in_str):
    """将过期时间字符串解析为timedelta对象"""
    try:
        if expires_in_str.endswith('h'):
            return timedelta(hours=int(expires_in_str[:-1]))
        if expires_in_str.endswith('d'):
            return timedelta(days=int(expires_in_str[:-1]))
        if expires_in_str.endswith('m'):
            return timedelta(minutes=int(expires_in_str[:-1]))
        if expires_in_str.endswith('s'):
            return timedelta(seconds=int(expires_in_str[:-1]))
        return timedelta(hours=24)  # 默认24小时
    except (ValueError, TypeError):
        return timedelta(hours=24)  # 默认24小时

def hash_password(password):
    """密码加密"""
    try:
        # 生成盐值
        salt = bcrypt.gensalt()
        # 加密密码
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error("密码加密失败: %s", e)
        raise

def verify_password(password, hashed_password):
    """密码验证"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error("密码验证失败: %s", e)
        return False

def generate_token(user_id, student_id):
    """生成JWT令牌"""
    try:
        # 计算过期时间
        expires_delta = _parse_expires_in(JWT_EXPIRES_IN)
        expires_at = datetime.utcnow() + expires_delta
        
        # 构建payload
        payload = {
            'user_id': user_id,
            'student_id': student_id,
            'exp': expires_at,
            'iat': datetime.utcnow()
        }
        
        # 生成令牌
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return token
    except Exception as e:
        logger.error("生成JWT令牌失败: %s", e)
        raise

def verify_token(token):
    """验证JWT令牌"""
    try:
        # 解码令牌
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("JWT令牌已过期")
        return None
    except jwt.InvalidTokenError:
        logger.error("JWT令牌无效")
        return None
    except Exception as e:
        logger.error("验证JWT令牌失败: %s", e)
        return None
