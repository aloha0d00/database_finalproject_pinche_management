from flask import request, jsonify
from config.database import get_connection, close_connection
from utils.naming_utils import snake_to_camel_dict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加车辆
def add_vehicle():
    """添加车辆信息"""
    connection = None
    try:
        user_id = request.user_id  # From auth middleware
        # 使用与其他控制器一致的方式获取JSON数据，确保在各种情况下都能正确解析
        data = request.get_json(force=True, silent=True) or {}
        
        # Validate required fields
        required_fields = ['plateNumber', 'brand', 'model', 'color', 'seats']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'缺少必填字段: {field}'}), 400
        
        # Check if user is a driver
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user or user['role'] != 'driver':
                return jsonify({'message': '只有司机可以添加车辆信息'}), 403
        
        # Check if plate number already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM vehicles WHERE plate_number = %s", (data['plateNumber'],))
            existing_vehicle = cursor.fetchone()
            if existing_vehicle:
                return jsonify({'message': '该车牌号已被添加'}), 400
        
        # Insert vehicle
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO vehicles (user_id, plate_number, brand, model, 
                                  color, seats, year, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                data['plateNumber'],
                data['brand'],
                data['model'],
                data['color'],
                data['seats'],
                data.get('year'),
                data.get('description')
            ))
        connection.commit()
        
        return jsonify({'message': '车辆信息添加成功'}), 201
    except Exception as e:
        logger.error(f"添加车辆失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500
    finally:
        if connection:
            close_connection(connection)

# 获取司机的车辆列表
def get_driver_vehicles():
    """获取司机的车辆列表"""
    try:
        user_id = request.user_id  # From auth middleware
        
        # Get vehicles
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles WHERE user_id = %s", (user_id,))
            vehicles = cursor.fetchall()
        close_connection(connection)
        
        # Format response
        formatted_vehicles = [snake_to_camel_dict(vehicle) for vehicle in vehicles]
        
        return jsonify(formatted_vehicles), 200
    except Exception as e:
        logger.error(f"获取车辆列表失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500