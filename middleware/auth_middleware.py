import logging
from flask import request, jsonify
from utils.auth_utils import verify_token

"""
认证中间件模块，提供JWT令牌验证功能
"""

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def auth_required(f):
    """认证中间件装饰器"""
    def decorated(*args, **kwargs):
        token = None

        # 从请求头获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': '未提供认证令牌'}), 401

        # 验证令牌
        payload = verify_token(token)
        if not payload:
            return jsonify({'message': '无效或过期的令牌'}), 401

        # 将用户信息添加到请求对象
        request.user_id = payload['user_id']
        request.student_id = payload['student_id']

        return f(*args, **kwargs)

    decorated.__name__ = f.__name__
    return decorated
