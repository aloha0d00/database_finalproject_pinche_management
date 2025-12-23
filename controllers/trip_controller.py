from flask import request, jsonify
from config.database import get_connection, close_connection
from utils.naming_utils import snake_to_camel_dict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取行程列表
def get_trips():
    """获取行程列表"""
    try:
        # 获取查询参数
        departure_location = request.args.get('departureLocation')
        arrival_location = request.args.get('arrivalLocation')
        departure_date = request.args.get('departureDate')
        
        # 构建查询条件
        query = """
            SELECT 
                trips.*, 
                users.name as driver_name,
                vehicles.brand as vehicle_brand,
                vehicles.model as vehicle_model
            FROM trips 
            JOIN users ON trips.driver_id = users.id 
            JOIN vehicles ON trips.vehicle_id = vehicles.id
            WHERE trip_status = 'pending'
        """
        params = []
        
        if departure_location:
            query += " AND departure_location LIKE %s"
            params.append(f"%{departure_location}%")
        
        if arrival_location:
            query += " AND arrival_location LIKE %s"
            params.append(f"%{arrival_location}%")
        
        if departure_date:
            query += " AND DATE(departure_time) = %s"
            params.append(departure_date)
        
        # 执行查询
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            trips_db = cursor.fetchall()
        
        close_connection(connection)
        
        # 转换为前端期望的格式
        trips = []
        for trip in trips_db:
            # 转换为驼峰命名
            camel_trip = snake_to_camel_dict(trip)
            # 特殊处理浮点数转换
            camel_trip['pricePerSeat'] = float(trip['price_per_seat'])
            # 整理driver和vehicle对象
            camel_trip['driver'] = {
                'id': trip['driver_id'],
                'name': trip['driver_name']
            }
            camel_trip['vehicle'] = {
                'id': trip['vehicle_id'],
                'brand': trip['vehicle_brand'],
                'model': trip['vehicle_model']
            }
            # 移除不需要的字段
            del camel_trip['driverId']
            del camel_trip['vehicleId']
            del camel_trip['driverName']
            del camel_trip['vehicleBrand']
            del camel_trip['vehicleModel']
            trips.append(camel_trip)
        
        # 返回结果
        return jsonify(trips), 200
        
    except Exception as e:
        logger.error(f"获取行程列表失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取单个行程
def get_trip(trip_id):
    """获取单个行程信息"""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT 
                        trips.*, 
                        users.name as driver_name,
                        vehicles.brand as vehicle_brand,
                        vehicles.model as vehicle_model
                    FROM trips 
                    JOIN users ON trips.driver_id = users.id 
                    JOIN vehicles ON trips.vehicle_id = vehicles.id
                    WHERE trips.id = %s
                """,
                (trip_id,)
            )
            trip_db = cursor.fetchone()
        
        close_connection(connection)
        
        if not trip_db:
            return jsonify({'message': '行程不存在'}), 404
        
        # 转换为前端期望的格式
        trip = {
            'id': trip_db['id'],
            'driverId': trip_db['driver_id'],
            'vehicleId': trip_db['vehicle_id'],
            'departureLocation': trip_db['departure_location'],
            'arrivalLocation': trip_db['arrival_location'],
            'departureTime': trip_db['departure_time'],
            'availableSeats': trip_db['available_seats'],
            'pricePerSeat': float(trip_db['price_per_seat']),
            'tripStatus': trip_db['trip_status'],
            'driver': {
                'id': trip_db['driver_id'],
                'name': trip_db['driver_name']
            },
            'vehicle': {
                'id': trip_db['vehicle_id'],
                'brand': trip_db['vehicle_brand'],
                'model': trip_db['vehicle_model']
            }
        }
        
        return jsonify(trip), 200
        
    except Exception as e:
        logger.error(f"获取行程信息失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 创建行程
def create_trip():
    """创建新行程"""
    connection = None
    try:
        user_id = request.user_id  # From auth middleware
        data = request.get_json(force=True, silent=True) or {}
        
        # Validate required fields
        required_fields = ['departureLocation', 'arrivalLocation', 'departureTime', 'availableSeats', 'pricePerSeat', 'vehicleId']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'缺少必填字段: {field}'}), 400
        
        # Check if user is a driver
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user or user['role'] != 'driver':
                return jsonify({'message': '只有司机可以发布行程'}), 403
        
        # Validate that the selected vehicle belongs to the driver
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM vehicles WHERE user_id = %s AND id = %s", (user_id, data['vehicleId']))
            vehicle = cursor.fetchone()
            if not vehicle:
                return jsonify({'message': '所选车辆不存在或不属于该司机'}), 400
        
        # Insert trip
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO trips (driver_id, vehicle_id, departure_location, arrival_location, 
                                  departure_time, available_seats, price_per_seat)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                data['vehicleId'],
                data['departureLocation'],
                data['arrivalLocation'],
                data['departureTime'],
                data['availableSeats'],
                data['pricePerSeat']
            ))
        connection.commit()
        
        return jsonify({'message': '行程创建成功'}), 201
    except Exception as e:
        logger.error(f"创建行程失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500
    finally:
        if connection:
            close_connection(connection)

# 获取司机行程
def get_driver_trips():
    """获取司机的行程列表"""
    try:
        user_id = request.user_id  # From auth middleware
        
        # 获取查询参数
        departure_location = request.args.get('departureLocation')
        arrival_location = request.args.get('arrivalLocation')
        departure_date = request.args.get('departureDate')
        
        # 构建查询条件
        query = """
            SELECT 
                trips.*, 
                users.name as driver_name,
                vehicles.brand as vehicle_brand,
                vehicles.model as vehicle_model
            FROM trips 
            JOIN users ON trips.driver_id = users.id 
            JOIN vehicles ON trips.vehicle_id = vehicles.id
            WHERE trips.driver_id = %s
        """
        params = [user_id]
        
        if departure_location:
            query += " AND departure_location LIKE %s"
            params.append(f"%{departure_location}%")
        
        if arrival_location:
            query += " AND arrival_location LIKE %s"
            params.append(f"%{arrival_location}%")
        
        if departure_date:
            query += " AND DATE(departure_time) = %s"
            params.append(departure_date)
        
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            trips_db = cursor.fetchall()
        
        close_connection(connection)
        
        # 转换为前端期望的格式
        trips = []
        for trip in trips_db:
            trips.append({
                'id': trip['id'],
                'driverId': trip['driver_id'],
                'vehicleId': trip['vehicle_id'],
                'departureLocation': trip['departure_location'],
                'arrivalLocation': trip['arrival_location'],
                'departureTime': trip['departure_time'],
                'availableSeats': trip['available_seats'],
                'pricePerSeat': float(trip['price_per_seat']),
                'tripStatus': trip['trip_status'],
                'driver': {
                    'id': trip['driver_id'],
                    'name': trip['driver_name']
                },
                'vehicle': {
                    'id': trip['vehicle_id'],
                    'brand': trip['vehicle_brand'],
                    'model': trip['vehicle_model']
                }
            })
        
        return jsonify(trips), 200
        
    except Exception as e:
        logger.error(f"获取司机行程失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 删除行程
def delete_trip(trip_id):
    """司机删除行程"""
    try:
        connection = get_connection()
        
        # 验证行程是否存在且当前用户是司机
        with connection.cursor() as cursor:
            cursor.execute("SELECT driver_id, trip_status FROM trips WHERE id = %s", (trip_id,))
            trip = cursor.fetchone()
            
            if not trip:
                close_connection(connection)
                return jsonify({'message': '行程不存在'}), 404
            
            if trip['driver_id'] != request.user_id:
                close_connection(connection)
                return jsonify({'message': '只有行程司机可以删除行程'}), 403
            
            # 可以添加业务规则，比如已开始或已完成的行程不能删除
            if trip['trip_status'] == 'ongoing' or trip['trip_status'] == 'completed':
                close_connection(connection)
                return jsonify({'message': '进行中或已完成的行程无法删除'}), 400
        
        # 删除行程（相关的参与者记录会通过外键约束自动删除）
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM trips WHERE id = %s", (trip_id,))
        
        connection.commit()
        close_connection(connection)
        
        return jsonify({'message': '行程删除成功'}), 200
        
    except Exception as e:
        logger.error(f"删除行程失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500