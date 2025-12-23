from flask import Blueprint
from controllers.participant_controller import (
    join_trip, get_trip_applications, handle_application,
    get_student_applications, cancel_application, get_trip_passengers_and_income
)
from middleware.auth_middleware import auth_required

"""
参与者相关路由定义
"""

# 创建蓝图
participant_bp = Blueprint('participant', __name__)

# 参与者相关路由
participant_bp.route(
    '/participants/trip/<int:trip_id>', methods=['POST']
)(auth_required(join_trip))  # 申请加入行程
participant_bp.route(
    '/participants/trips/<int:trip_id>/applications', methods=['GET']
)(auth_required(get_trip_applications))  # 获取行程的加入申请
participant_bp.route(
    '/participants/<int:application_id>/status', methods=['PUT']
)(auth_required(handle_application))  # 处理加入申请
participant_bp.route(
    '/participants/student', methods=['GET']
)(auth_required(get_student_applications))  # 获取学生的申请列表
participant_bp.route(
    '/participants/<int:application_id>', methods=['DELETE']
)(auth_required(cancel_application))  # 取消申请
participant_bp.route(
    '/participants/trips/<int:trip_id>/passengers', methods=['GET']
)(auth_required(get_trip_passengers_and_income))  # 获取行程乘客和收入信息

# 测试路由：获取行程乘客和收入信息（绕过身份验证）
participant_bp.route(
    '/test/participants/trips/<int:trip_id>/passengers', methods=['GET'], endpoint='get_trip_passengers_and_income_test'
)(get_trip_passengers_and_income)
