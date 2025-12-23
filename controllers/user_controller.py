import logging
from flask import request, jsonify
from config.database import get_connection, close_connection
from utils.auth_utils import hash_password, verify_password, generate_token
from utils.naming_utils import snake_to_camel_dict

"""
用户控制器模块，处理用户注册、登录和信息管理
"""

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 用户注册
def register():
    """用户注册"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        role = data.get('role', 'student')  # 默认学生角色
        name = data.get('name')
        phone = data.get('phone')
        password = data.get('password')
        student_id = data.get('studentId')
        
        # 简单验证输入
        if not name or not phone or not password:
            return jsonify({'message': '请填写所有必填字段'}), 400
        
        # 根据角色验证学号需求
        if role == 'student' and not student_id:
            return jsonify({'message': '学生角色必须填写学号'}), 400
        
        # 检查学号是否已存在（仅当提供学号时）
        connection = get_connection()
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
        hashed_password = hash_password(password)
        
        # 创建用户
        with connection.cursor() as cursor:
            if role == 'student':
                # 学生角色：需要学号
                cursor.execute(
                    "INSERT INTO users (student_id, name, phone, password, role) VALUES (%s, %s, %s, %s, %s)",
                    (student_id, name, phone, hashed_password, role)
                )
            else:
                # 司机和管理员角色：不需要学号
                cursor.execute(
                    "INSERT INTO users (name, phone, password, role) VALUES (%s, %s, %s, %s)",
                    (name, phone, hashed_password, role)
                )
            user_id = cursor.lastrowid
        
        # 提交事务
        connection.commit()
        
        # 继续使用同一个连接查询新创建的用户信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, student_id, name, phone, role FROM users WHERE id = %s", (user_id,))
            new_user = cursor.fetchone()
        
        # 关闭新连接
        close_connection(connection)
        
        # 返回用户信息
        return jsonify({
            'message': '注册成功',
            'user': {
                'id': new_user['id'],
                'studentId': new_user['student_id'],
                'name': new_user['name'],
                'phone': new_user['phone'],
                'role': new_user['role']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"注册失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 用户登录
def login():
    """用户登录"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        role = data.get('role', 'student')
        identifier = data.get('studentId') if role == 'student' else data.get('phone')
        password = data.get('password')
        
        # 根据角色选择查询条件
        connection = get_connection()
        with connection.cursor() as cursor:
            if role == 'student':
                cursor.execute("SELECT * FROM users WHERE student_id = %s", (identifier,))
            else:
                cursor.execute("SELECT * FROM users WHERE phone = %s AND role = %s", (identifier, role))
            user = cursor.fetchone()
        
        close_connection(connection)
        
        if not user:
            return jsonify({'message': f'{"学号" if role == "student" else "手机号"}或密码错误'}), 401
        
        # 验证密码
        if not verify_password(password, user['password']):
            return jsonify({'message': f'{"学号" if role == "student" else "手机号"}或密码错误'}), 401
        
        # 生成JWT令牌
        token = generate_token(user['id'], user['student_id'] or '')
        
        # 返回用户信息和令牌
        return jsonify({
            'message': '登录成功',
            'token': token,
            'user': {
                'id': user['id'],
                'studentId': user['student_id'],
                'name': user['name'],
                'phone': user['phone'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"登录失败: {e}")
        return jsonify({'message': '服务器错误，请稍后重试'}), 500

# 获取用户信息
def get_user_profile(user_id=None):
    """获取用户信息"""
    try:
        # 确保用户只能查看自己的信息
        current_user_id = request.user_id  # 从认证中间件获取
        
        # 如果没有提供user_id，使用当前用户的ID（用于/me路由）
        if user_id is None:
            user_id = current_user_id
        elif int(user_id) != int(current_user_id):
            return jsonify({'message': '无权查看其他用户信息'}), 403
        
        # 查找用户
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, student_id, name, phone, role, created_at FROM users WHERE id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
        
        close_connection(connection)
        
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 转换字段名格式
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

# 更新用户信息
def update_user_profile(user_id):
    """更新用户信息"""
    try:
        # 确保用户只能修改自己的信息
        current_user_id = request.user_id  # 从认证中间件获取
        if int(user_id) != int(current_user_id):
            return jsonify({'message': '无权修改其他用户信息'}), 403
        
        data = request.get_json(force=True, silent=True) or {}
        name = data.get('name')
        phone = data.get('phone')
        
        # 查找用户
        connection = get_connection()
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
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            updated_user = cursor.fetchone()
        
        close_connection(connection)
        
        # 返回更新后的用户信息
        return jsonify({
            'message': '信息更新成功',
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
