from flask import Blueprint
from controllers.user_controller import register, login, get_user_profile, update_user_profile
from middleware.auth_middleware import auth_required

"""
用户相关路由定义
"""

# 创建蓝图
user_bp = Blueprint('user', __name__)

# 公共路由
user_bp.route('/register', methods=['POST'])(register)  # 用户注册
user_bp.route('/login', methods=['POST'])(login)  # 用户登录

# 需要认证的路由
user_bp.route(
    '/<int:user_id>', methods=['GET'], endpoint='get_user_by_id'
)(auth_required(get_user_profile))  # 获取用户信息
user_bp.route(
    '/me', methods=['GET'], endpoint='get_current_user'
)(auth_required(get_user_profile))  # 获取当前用户信息
user_bp.route(
    '/<int:user_id>', methods=['PUT']
)(auth_required(update_user_profile))  # 更新用户信息
