from flask import request, jsonify
from config.database import get_connection, close_connection
from utils.naming_utils import snake_to_camel_dict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 检查用户是否为管理员
def check_admin():
    """检查当前用户是否为管理员"""
    try:
        user_id = request.user_id  # From auth middleware
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
        close_connection(connection)
        return user and user['role'] == 'admin'
    except Exception as e:
        logger.error(f"检查管理员权限失败: {e}")
        return False

# 获取所有用户
def get_all_users():
    """获取所有用户列表，可以通过role查询参数过滤"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        # 获取查询参数
        role = request.args.get('role')
        
        connection = get_connection()
        with connection.cursor() as cursor:
            if role:
                cursor.execute("SELECT id, student_id, name, phone, role, created_at FROM users WHERE role = %s", (role,))
            else:
                cursor.execute("SELECT id, student_id, name, phone, role, created_at FROM users")
            users = cursor.fetchall()
        close_connection(connection)
        
        # 转换为前端期望的格式
        result = []
        for user in users:
            result.append({
                'id': user['id'],
                'studentId': user['student_id'],
                'name': user['name'],
                'phone': user['phone'],
                'role': user['role'],
                'createdAt': user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else None
            })
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取单个用户
def get_user(user_id):
    """获取单个用户信息"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, student_id, name, phone, role, created_at FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
        close_connection(connection)
        
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 转换为前端期望的格式
        user_data = {
            'id': user['id'],
            'studentId': user['student_id'],
            'name': user['name'],
            'phone': user['phone'],
            'role': user['role'],
            'createdAt': user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else None
        }
        
        return jsonify(user_data), 200
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 创建用户
def create_user():
    """管理员创建新用户"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        data = request.get_json(force=True, silent=True) or {}
        role = data.get('role', 'student')
        name = data.get('name')
        phone = data.get('phone')
        password = data.get('password')
        student_id = data.get('studentId')
        
        # 验证输入
        if not name or not phone or not password:
            return jsonify({'message': '请填写所有必填字段'}), 400
        
        # 根据角色验证学号需求
        if role == 'student' and not student_id:
            return jsonify({'message': '学生角色必须填写学号'}), 400
        
        connection = get_connection()
        
        # 检查学号是否已存在（仅当提供学号时）
        if student_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE student_id = %s", (student_id,))
                existing_user = cursor.fetchone()
                if existing_user:
                    close_connection(connection)
                    return jsonify({'message': '该学号已被注册'}), 400
        
        # 检查手机号是否已存在
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
            existing_user = cursor.fetchone()
            if existing_user:
                close_connection(connection)
                return jsonify({'message': '该手机号已被注册'}), 400
        
        # 密码加密
        from utils.auth_utils import hash_password
        hashed_password = hash_password(password)
        
        # 创建用户
        with connection.cursor() as cursor:
            if role == 'student':
                cursor.execute(
                    "INSERT INTO users (student_id, name, phone, password, role, status) VALUES (%s, %s, %s, %s, %s, %s)",
                    (student_id, name, phone, hashed_password, role, 'active')
                )
            else:
                cursor.execute(
                    "INSERT INTO users (name, phone, password, role, status) VALUES (%s, %s, %s, %s, %s)",
                    (name, phone, hashed_password, role, 'active')
                )
            user_id = cursor.lastrowid
        
        # 提交事务
        connection.commit()
        
        # 获取新创建的用户信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, student_id, name, phone, role FROM users WHERE id = %s", (user_id,))
            new_user = cursor.fetchone()
        
        close_connection(connection)
        
        # 返回用户信息
        return jsonify({
            'message': '用户创建成功',
            'user': {
                'id': new_user['id'],
                'studentId': new_user['student_id'],
                'name': new_user['name'],
                'phone': new_user['phone'],
                'role': new_user['role']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"创建用户失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 更新用户信息
def update_user(user_id):
    """管理员更新用户信息"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        data = request.get_json(force=True, silent=True) or {}
        name = data.get('name')
        phone = data.get('phone')
        role = data.get('role')
        student_id = data.get('studentId')
        
        connection = get_connection()
        
        # 查找用户
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                close_connection(connection)
                return jsonify({'message': '用户不存在'}), 404
        
        # 更新用户信息
        update_data = []
        params = []
        
        if name:
            update_data.append("name = %s")
            params.append(name)
        if phone:
            update_data.append("phone = %s")
            params.append(phone)
        if role:
            update_data.append("role = %s")
            params.append(role)
            
            # 如果角色不是学生，清空学号
            if role != 'student':
                update_data.append("student_id = NULL")
        
        # 只有当角色是学生且提供了学号时才更新学号
        if role == 'student' and student_id:
            update_data.append("student_id = %s")
            params.append(student_id)
        
        if not update_data:
            close_connection(connection)
            return jsonify({'message': '没有可更新的信息'}), 400
        
        params.append(user_id)
        
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET {', '.join(update_data)} WHERE id = %s",
                params
            )
        
        # 提交事务
        connection.commit()
        
        # 获取更新后的用户信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, student_id, name, phone, role FROM users WHERE id = %s", (user_id,))
            updated_user = cursor.fetchone()
        
        close_connection(connection)
        
        # 返回更新后的用户信息
        return jsonify({
            'message': '用户信息更新成功',
            'user': {
                'id': updated_user['id'],
                'studentId': updated_user['student_id'],
                'name': updated_user['name'],
                'phone': updated_user['phone'],
                'role': updated_user['role']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 删除用户
def delete_user(user_id):
    """管理员删除用户"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        # 不允许删除管理员自己
        current_user_id = request.user_id
        if int(user_id) == int(current_user_id):
            return jsonify({'message': '不能删除自己的管理员账户'}), 400
        
        connection = get_connection()
        
        # 查找用户
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                close_connection(connection)
                return jsonify({'message': '用户不存在'}), 404
        
        # 删除用户
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        # 提交事务
        connection.commit()
        close_connection(connection)
        
        return jsonify({'message': '用户删除成功'}), 200
        
    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取所有车辆
def get_all_vehicles():
    """获取所有车辆列表"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT vehicles.*, users.name as driver_name FROM vehicles JOIN users ON vehicles.user_id = users.id")
            vehicles = cursor.fetchall()
        close_connection(connection)
        
        # 转换为前端期望的格式
        result = []
        for vehicle in vehicles:
            vehicle_data = snake_to_camel_dict(vehicle)
            result.append(vehicle_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"获取车辆列表失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 更新车辆信息
def update_vehicle(vehicle_id):
    """管理员更新车辆信息"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        data = request.get_json(force=True, silent=True) or {}
        plate_number = data.get('plateNumber')
        brand = data.get('brand')
        model = data.get('model')
        color = data.get('color')
        seats = data.get('seats')
        year = data.get('year')
        description = data.get('description')
        
        connection = get_connection()
        
        # 查找车辆
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
            vehicle = cursor.fetchone()
            if not vehicle:
                close_connection(connection)
                return jsonify({'message': '车辆不存在'}), 404
        
        # 更新车辆信息
        update_data = []
        params = []
        
        if plate_number:
            update_data.append("plate_number = %s")
            params.append(plate_number)
        if brand:
            update_data.append("brand = %s")
            params.append(brand)
        if model:
            update_data.append("model = %s")
            params.append(model)
        if color:
            update_data.append("color = %s")
            params.append(color)
        if seats:
            update_data.append("seats = %s")
            params.append(seats)
        if year:
            update_data.append("year = %s")
            params.append(year)
        if description:
            update_data.append("description = %s")
            params.append(description)
        
        if not update_data:
            close_connection(connection)
            return jsonify({'message': '没有可更新的信息'}), 400
        
        params.append(vehicle_id)
        
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE vehicles SET {', '.join(update_data)} WHERE id = %s",
                params
            )
        connection.commit()
        
        # 获取更新后的车辆信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
            updated_vehicle = cursor.fetchone()
        
        close_connection(connection)
        
        # 返回更新后的车辆信息
        return jsonify({
            'message': '车辆信息更新成功',
            'vehicle': snake_to_camel_dict(updated_vehicle)
        }), 200
        
    except Exception as e:
        logger.error(f"更新车辆信息失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 删除车辆
def delete_vehicle(vehicle_id):
    """管理员删除车辆"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        connection = get_connection()
        
        # 查找车辆
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
            vehicle = cursor.fetchone()
            if not vehicle:
                close_connection(connection)
                return jsonify({'message': '车辆不存在'}), 404
        
        # 删除车辆
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
        
        # 提交事务
        connection.commit()
        close_connection(connection)
        
        return jsonify({'message': '车辆删除成功'}), 200
        
    except Exception as e:
        logger.error(f"删除车辆失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 创建车辆
def create_vehicle():
    """管理员创建车辆"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        # 获取请求数据
        data = request.get_json(force=True, silent=True) or {}
        
        # 验证必填字段
        required_fields = ['plateNumber', 'brand', 'model', 'color', 'seats', 'userId']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'缺少必填字段: {field}'}), 400
        
        connection = get_connection()
        
        # 验证司机是否存在
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s AND role = 'driver'", (data['userId'],))
            driver = cursor.fetchone()
            if not driver:
                close_connection(connection)
                return jsonify({'message': '指定的司机不存在'}), 400
        
        # 检查车牌号是否已存在
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles WHERE plate_number = %s", (data['plateNumber'],))
            existing_vehicle = cursor.fetchone()
            if existing_vehicle:
                close_connection(connection)
                return jsonify({'message': '该车牌号已被添加'}), 400
        
        # 创建车辆
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO vehicles (user_id, plate_number, brand, model, color, seats, year, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['userId'],
                data['plateNumber'],
                data['brand'],
                data['model'],
                data['color'],
                data['seats'],
                data.get('year'),
                data.get('description')
            ))
        
        # 提交事务
        connection.commit()
        close_connection(connection)
        
        return jsonify({'message': '车辆创建成功'}), 201
        
    except Exception as e:
        logger.error(f"创建车辆失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取所有行程
def get_all_trips():
    """获取所有行程列表"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    trips.*, 
                    users.name as driver_name,
                    vehicles.brand as vehicle_brand,
                    vehicles.model as vehicle_model
                FROM trips 
                JOIN users ON trips.driver_id = users.id 
                JOIN vehicles ON trips.vehicle_id = vehicles.id
            """)
            trips = cursor.fetchall()
        close_connection(connection)
        
        # 转换为前端期望的格式
        result = []
        for trip in trips:
            trip_data = {
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
            }
            result.append(trip_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"获取行程列表失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 更新行程信息
def update_trip(trip_id):
    """管理员更新行程信息"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        data = request.get_json(force=True, silent=True) or {}
        departure_location = data.get('departureLocation')
        arrival_location = data.get('arrivalLocation')
        departure_time = data.get('departureTime')
        available_seats = data.get('availableSeats')
        price_per_seat = data.get('pricePerSeat')
        trip_status = data.get('tripStatus')
        description = data.get('description')
        departure_latitude = data.get('departureLatitude')
        departure_longitude = data.get('departureLongitude')
        arrival_latitude = data.get('arrivalLatitude')
        arrival_longitude = data.get('arrivalLongitude')
        
        connection = get_connection()
        
        # 查找行程
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trips WHERE id = %s", (trip_id,))
            trip = cursor.fetchone()
            if not trip:
                close_connection(connection)
                return jsonify({'message': '行程不存在'}), 404
        
        # 更新行程信息
        update_data = []
        params = []
        
        if departure_location:
            update_data.append("departure_location = %s")
            params.append(departure_location)
        if arrival_location:
            update_data.append("arrival_location = %s")
            params.append(arrival_location)
        if departure_time:
            update_data.append("departure_time = %s")
            params.append(departure_time)
        if available_seats:
            update_data.append("available_seats = %s")
            params.append(available_seats)
        if price_per_seat:
            update_data.append("price_per_seat = %s")
            params.append(price_per_seat)
        if trip_status:
            update_data.append("trip_status = %s")
            params.append(trip_status)
        if description:
            update_data.append("description = %s")
            params.append(description)
        if departure_latitude is not None:
            update_data.append("departure_latitude = %s")
            params.append(departure_latitude)
        if departure_longitude is not None:
            update_data.append("departure_longitude = %s")
            params.append(departure_longitude)
        if arrival_latitude is not None:
            update_data.append("arrival_latitude = %s")
            params.append(arrival_latitude)
        if arrival_longitude is not None:
            update_data.append("arrival_longitude = %s")
            params.append(arrival_longitude)
        
        if not update_data:
            close_connection(connection)
            return jsonify({'message': '没有可更新的信息'}), 400
        
        params.append(trip_id)
        
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE trips SET {', '.join(update_data)} WHERE id = %s",
                params
            )
        
        # 提交事务
        connection.commit()
        
        # 获取更新后的行程信息
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    trips.*, 
                    users.name as driver_name,
                    vehicles.brand as vehicle_brand,
                    vehicles.model as vehicle_model
                FROM trips 
                JOIN users ON trips.driver_id = users.id 
                JOIN vehicles ON trips.vehicle_id = vehicles.id
                WHERE trips.id = %s
            """, (trip_id,))
            updated_trip = cursor.fetchone()
        
        close_connection(connection)
        
        # 返回更新后的行程信息
        if updated_trip:
            trip_data = {
                'id': updated_trip['id'],
                'driverId': updated_trip['driver_id'],
                'vehicleId': updated_trip['vehicle_id'],
                'departureLocation': updated_trip['departure_location'],
                'arrivalLocation': updated_trip['arrival_location'],
                'departureTime': updated_trip['departure_time'],
                'availableSeats': updated_trip['available_seats'],
                'pricePerSeat': float(updated_trip['price_per_seat']),
                'tripStatus': updated_trip['trip_status'],
                'description': updated_trip['description'],
                'departureLatitude': updated_trip['departure_latitude'],
                'departureLongitude': updated_trip['departure_longitude'],
                'arrivalLatitude': updated_trip['arrival_latitude'],
                'arrivalLongitude': updated_trip['arrival_longitude'],
                'driver': {
                    'id': updated_trip['driver_id'],
                    'name': updated_trip['driver_name']
                },
                'vehicle': {
                    'id': updated_trip['vehicle_id'],
                    'brand': updated_trip['vehicle_brand'],
                    'model': updated_trip['vehicle_model']
                }
            }
            return jsonify({
                'message': '行程信息更新成功',
                'trip': trip_data
            }), 200
        else:
            return jsonify({'message': '行程更新失败'}), 500
            
    except Exception as e:
        logger.error(f"更新行程信息失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 删除行程
def delete_trip(trip_id):
    """管理员删除行程"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        connection = get_connection()
        
        # 查找行程
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trips WHERE id = %s", (trip_id,))
            trip = cursor.fetchone()
            if not trip:
                close_connection(connection)
                return jsonify({'message': '行程不存在'}), 404
        
        # 删除行程
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM trips WHERE id = %s", (trip_id,))
        
        close_connection(connection)
        
        return jsonify({'message': '行程删除成功'}), 200
        
    except Exception as e:
        logger.error(f"删除行程失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取统计数据
def get_stats():
    """获取系统统计数据"""
    try:
        # 检查管理员权限
        if not check_admin():
            return jsonify({'message': '您没有权限执行此操作'}), 403
        
        connection = get_connection()
        
        # 获取总用户数
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = cursor.fetchone()['total']
        
        # 获取总车辆数
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM vehicles")
            total_vehicles = cursor.fetchone()['total']
        
        # 获取总行程数
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM trips")
            total_trips = cursor.fetchone()['total']
        
        # 获取今日新用户数
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM users WHERE DATE(created_at) = CURDATE()")
            today_new_users = cursor.fetchone()['total']
        
        close_connection(connection)
        
        return jsonify({
            'totalUsers': total_users,
            'totalVehicles': total_vehicles,
            'totalTrips': total_trips,
            'todayNewUsers': today_new_users
        }), 200
        
    except Exception as e:
        logger.error(f"获取统计数据失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500
