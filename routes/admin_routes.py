from flask import Blueprint
from controllers.admin_controller import (
    get_all_users,
    get_user,
    create_user,
    update_user,
    delete_user,
    get_all_vehicles,
    create_vehicle,
    update_vehicle,
    delete_vehicle,
    get_all_trips,
    update_trip,
    delete_trip,
    get_stats
)
from middleware.auth_middleware import auth_required

"""
管理员相关路由定义
"""

# 创建蓝图
admin_bp = Blueprint('admin', __name__)

# 所有管理员路由都需要认证
admin_bp.route('/users', methods=['GET'])(auth_required(get_all_users))  # 获取所有用户
admin_bp.route('/users/<int:user_id>', methods=['GET'])(auth_required(get_user))  # 获取单个用户
admin_bp.route('/users', methods=['POST'])(auth_required(create_user))  # 创建用户
admin_bp.route('/users/<int:user_id>', methods=['PUT'])(auth_required(update_user))  # 更新用户信息
admin_bp.route('/users/<int:user_id>', methods=['DELETE'])(auth_required(delete_user))  # 删除用户

admin_bp.route('/vehicles', methods=['GET'])(auth_required(get_all_vehicles))  # 获取所有车辆
admin_bp.route('/vehicles', methods=['POST'])(auth_required(create_vehicle))  # 创建车辆
admin_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])(auth_required(update_vehicle))  # 更新车辆信息
admin_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])(auth_required(delete_vehicle))  # 删除车辆

admin_bp.route('/trips', methods=['GET'])(auth_required(get_all_trips))  # 获取所有行程
admin_bp.route('/trips/<int:trip_id>', methods=['PUT'])(auth_required(update_trip))  # 更新行程信息
admin_bp.route('/trips/<int:trip_id>', methods=['DELETE'])(auth_required(delete_trip))  # 删除行程
admin_bp.route('/stats', methods=['GET'])(auth_required(get_stats))  # 获取仪表盘统计数据
