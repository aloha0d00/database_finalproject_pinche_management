from flask import Blueprint
from controllers.vehicle_controller import add_vehicle, get_driver_vehicles
from middleware.auth_middleware import auth_required

"""
车辆相关路由定义
"""

# 创建蓝图
vehicle_bp = Blueprint('vehicle', __name__)

# 车辆相关路由
vehicle_bp.route('/vehicles', methods=['POST'])(auth_required(add_vehicle))  # 添加车辆信息
vehicle_bp.route('/vehicles', methods=['GET'])(auth_required(get_driver_vehicles))  # 获取司机的车辆列表
