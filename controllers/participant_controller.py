from flask import request, jsonify
from config.database import get_connection, close_connection
from utils.naming_utils import snake_to_camel_dict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取行程的加入申请
def get_trip_applications(trip_id):
    """获取行程的所有加入申请"""
    try:
        connection = get_connection()
        
        # 验证行程是否存在且当前用户是司机
        with connection.cursor() as cursor:
            cursor.execute("SELECT driver_id FROM trips WHERE id = %s", (trip_id,))
            trip = cursor.fetchone()
            
            if not trip:
                close_connection(connection)
                return jsonify({'message': '行程不存在'}), 404
            
            if trip['driver_id'] != request.user_id:
                close_connection(connection)
                return jsonify({'message': '只有行程司机可以查看申请'}), 403
        
        # 获取所有申请
        with connection.cursor() as cursor:
            cursor.execute("SELECT participants.*, users.name as student_name, users.phone as student_phone, users.student_id FROM participants JOIN users ON participants.user_id = users.id WHERE participants.trip_id = %s AND participants.participant_status = 'pending' ORDER BY participants.created_at DESC", (trip_id,))
            applications = cursor.fetchall()
        
        close_connection(connection)
        
        # 转换格式
        result = []
        for app in applications:
            result.append({
                'id': app['id'],
                'tripId': app['trip_id'],
                'userId': app['user_id'],
                'student': {
                    'name': app['student_name'],
                    'phone': app['student_phone'],
                    'studentId': app['student_id']
                },
                'seatsBooked': app['seats_booked'],
                'participantStatus': app['participant_status'],
                'paymentStatus': app['payment_status'],
                'createdAt': app['created_at']
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"获取行程申请失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 申请加入行程
def join_trip(trip_id):
    """用户申请加入行程"""
    try:
        # 获取当前用户ID
        user_id = request.user_id
        
        # 获取请求数据
        data = request.get_json(force=True, silent=True) or {}
        seats_booked = data.get('seatsBooked', 1)
        
        # 验证行程是否存在且有足够座位
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT available_seats, trip_status FROM trips WHERE id = %s", (trip_id,))
            trip = cursor.fetchone()
            
            if not trip:
                close_connection(connection)
                return jsonify({'message': '行程不存在'}), 404
            
            if trip['trip_status'] != 'pending':
                close_connection(connection)
                return jsonify({'message': '该行程已关闭'}), 400
            
            if trip['available_seats'] < seats_booked:
                close_connection(connection)
                return jsonify({'message': '座位不足'}), 400
        
        # 检查用户是否已经申请过该行程（不考虑已取消的申请）
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM participants WHERE trip_id = %s AND user_id = %s AND participant_status != 'cancelled'", (trip_id, user_id))
            existing_participant = cursor.fetchone()
            
            if existing_participant:
                close_connection(connection)
                return jsonify({'message': '您已经申请过该行程'}), 400
        
        # 创建参与者记录
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO participants (trip_id, user_id, seats_booked) VALUES (%s, %s, %s)",
                (trip_id, user_id, seats_booked)
            )
        
        connection.commit()
        close_connection(connection)
        
        return jsonify({'message': '申请成功，等待司机确认'}), 201
        
    except Exception as e:
        logger.error(f"申请加入行程失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取学生的申请列表
def get_student_applications():
    """获取当前学生的所有申请"""
    try:
        connection = get_connection()
        user_id = request.user_id
        
        # 获取所有申请及相关行程信息
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    participants.*, 
                    trips.departure_location,
                    trips.arrival_location,
                    trips.departure_time,
                    trips.price_per_seat,
                    users.name as driver_name
                FROM participants 
                JOIN trips ON participants.trip_id = trips.id
                JOIN users ON trips.driver_id = users.id
                WHERE participants.user_id = %s AND participants.participant_status != 'cancelled'
                ORDER BY participants.created_at DESC
            """, (user_id,))
            applications = cursor.fetchall()
        
        close_connection(connection)
        
        # 转换格式
        result = []
        for app in applications:
            result.append({
                'id': app['id'],
                'tripId': app['trip_id'],
                'seatsBooked': app['seats_booked'],
                'participantStatus': app['participant_status'],
                'paymentStatus': app['payment_status'],
                'createdAt': app['created_at'],
                'trip': {
                    'departureLocation': app['departure_location'],
                    'arrivalLocation': app['arrival_location'],
                    'departureTime': app['departure_time'],
                    'pricePerSeat': float(app['price_per_seat'])
                },
                'driver': {
                    'name': app['driver_name']
                }
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"获取学生申请列表失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 学生取消申请
def cancel_application(application_id):
    """学生取消加入申请"""
    try:
        connection = get_connection()
        user_id = request.user_id
        
        # 验证申请是否存在且当前用户是申请人
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT participants.*, trips.trip_status
                FROM participants
                JOIN trips ON participants.trip_id = trips.id
                WHERE participants.id = %s
            """, (application_id,))
            application = cursor.fetchone()
            
            if not application:
                close_connection(connection)
                return jsonify({'message': '申请不存在'}), 404
            
            if application['user_id'] != user_id:
                close_connection(connection)
                return jsonify({'message': '只有申请人可以取消申请'}), 403
            
            if application['participant_status'] == 'completed' or application['participant_status'] == 'cancelled':
                close_connection(connection)
                return jsonify({'message': '该申请已完成或已取消，无法再操作'}), 400
            
            if application['trip_status'] != 'pending':
                close_connection(connection)
                return jsonify({'message': '行程已关闭，无法取消申请'}), 400
        
        # 开始事务
        connection.begin()
        
        try:
            # 如果申请已被接受，需要恢复行程的可用座位
            if application['participant_status'] == 'accepted':
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE trips SET available_seats = available_seats + %s WHERE id = %s",
                        (application['seats_booked'], application['trip_id'])
                    )
            
            # 删除申请记录而不是更新状态为cancelled，避免重复键错误
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM participants WHERE id = %s",
                    (application_id,)
                )
            
            connection.commit()
            close_connection(connection)
            
            return jsonify({'message': '申请取消成功'}), 200
            
        except Exception as e:
            connection.rollback()
            close_connection(connection)
            raise e
            
    except Exception as e:
        logger.error(f"取消申请失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 处理加入申请
def handle_application(application_id):
    """司机同意或拒绝加入申请"""
    try:
        connection = get_connection()
        data = request.get_json(force=True, silent=True) or {}
        
        # 验证请求数据
        if 'status' not in data or data['status'] not in ['accepted', 'rejected']:
            close_connection(connection)
            return jsonify({'message': '无效的请求数据'}), 400
        
        # 验证申请是否存在且当前用户是对应行程的司机
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT participants.*, trips.driver_id, trips.available_seats
                FROM participants
                JOIN trips ON participants.trip_id = trips.id
                WHERE participants.id = %s
            """, (application_id,))
            application = cursor.fetchone()
            
            if not application:
                close_connection(connection)
                return jsonify({'message': '申请不存在'}), 404
            
            if application['driver_id'] != request.user_id:
                close_connection(connection)
                return jsonify({'message': '只有行程司机可以处理申请'}), 403
            
            if application['participant_status'] != 'pending':
                close_connection(connection)
                return jsonify({'message': '该申请已处理'}), 400
        
        # 开始事务
        connection.begin()
        
        try:
            # 更新申请状态
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE participants SET participant_status = %s WHERE id = %s",
                    (data['status'], application_id)
                )
            
            # 如果同意申请，减少行程的可用座位
            if data['status'] == 'accepted':
                # 检查是否有足够的座位
                if application['available_seats'] < application['seats_booked']:
                    connection.rollback()
                    close_connection(connection)
                    return jsonify({'message': '座位不足，无法同意申请'}), 400
                
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE trips SET available_seats = available_seats - %s WHERE id = %s",
                        (application['seats_booked'], application['trip_id'])
                    )
            
            connection.commit()
            close_connection(connection)
            
            return jsonify({'message': '申请处理成功'}), 200
            
        except Exception as e:
            connection.rollback()
            close_connection(connection)
            raise e
            
    except Exception as e:
        logger.error(f"处理申请失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取行程的乘客信息和计算收入
def get_trip_passengers_and_income(trip_id):
    """获取行程的所有乘客信息和计算总收入"""
    try:
        logger.info(f"处理查看乘客请求，行程ID: {trip_id}")
        logger.info(f"请求路径: {request.path}")
        logger.info(f"请求用户ID: {getattr(request, 'user_id', '无用户ID')}")
        
        connection = get_connection()
        logger.info("成功连接数据库")
        
        # 验证行程是否存在且当前用户是司机
        with connection.cursor() as cursor:
            cursor.execute("SELECT driver_id, price_per_seat FROM trips WHERE id = %s", (trip_id,))
            trip = cursor.fetchone()
            logger.info(f"查询行程信息: {trip}")
            
            if not trip:
                close_connection(connection)
                logger.warning(f"行程不存在，ID: {trip_id}")
                return jsonify({'message': '行程不存在'}), 404
            
            # 只有在不是测试路由的情况下才验证司机权限
            if request.path.startswith('/api/participants/') and hasattr(request, 'user_id'):
                logger.info(f"验证司机权限，行程司机ID: {trip['driver_id']}, 请求用户ID: {request.user_id}")
                if trip['driver_id'] != request.user_id:
                    close_connection(connection)
                    logger.warning(f"权限验证失败，行程司机ID: {trip['driver_id']}, 请求用户ID: {request.user_id}")
                    return jsonify({'message': '只有行程司机可以查看乘客信息'}), 403
        
        # 获取所有已接受的乘客
        with connection.cursor() as cursor:
            logger.info(f"查询已接受的乘客，行程ID: {trip_id}")
            cursor.execute("SELECT participants.*, users.name as student_name, users.phone as student_phone, users.student_id FROM participants JOIN users ON participants.user_id = users.id WHERE participants.trip_id = %s AND participants.participant_status = 'accepted' ORDER BY participants.created_at DESC", (trip_id,))
            passengers = cursor.fetchall()
        
        logger.info(f"查询到乘客数量: {len(passengers)}")
        logger.info(f"乘客详情: {passengers}")
        
        # 计算总收入
        total_income = 0
        for passenger in passengers:
            total_income += trip['price_per_seat'] * passenger['seats_booked']
        
        logger.info(f"计算总收入: {total_income}, 单价: {trip['price_per_seat']}")
        
        close_connection(connection)
        
        # 转换格式
        result = {
            'tripId': trip_id,
            'passengers': [],
            'totalIncome': float(total_income),
            'pricePerSeat': float(trip['price_per_seat'])
        }
        
        for passenger in passengers:
            result['passengers'].append({
                'id': passenger['id'],
                'student': {
                    'name': passenger['student_name'],
                    'phone': passenger['student_phone'],
                    'studentId': passenger['student_id']
                },
                'seatsBooked': passenger['seats_booked'],
                'paymentStatus': passenger['payment_status'],
                'createdAt': passenger['created_at'].isoformat() if passenger['created_at'] else None
            })
        
        # 添加调试日志
        logger.info(f"最终返回的乘客数据: {result}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"获取行程乘客信息失败: {e}", exc_info=True)
        return jsonify({'message': '服务器错误，请稍后重试'}), 500