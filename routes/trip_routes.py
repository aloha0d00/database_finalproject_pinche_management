from flask import Blueprint
from controllers.trip_controller import (
    get_trips, get_trip, create_trip, delete_trip, get_driver_trips
)
from middleware.auth_middleware import auth_required

"""
行程相关路由定义
"""

# 创建蓝图
trip_bp = Blueprint('trip', __name__)

# 行程相关路由
trip_bp.route('/trips', methods=['GET'])(get_trips)  # 获取行程列表
trip_bp.route('/trips/<int:trip_id>', methods=['GET'])(get_trip)  # 获取单个行程信息
trip_bp.route('/trips', methods=['POST'])(auth_required(create_trip))  # 创建行程
trip_bp.route('/trips/<int:trip_id>', methods=['DELETE'])(auth_required(delete_trip))  # 删除行程
trip_bp.route('/trips/driver', methods=['GET'])(auth_required(get_driver_trips))  # 获取司机的行程列表
