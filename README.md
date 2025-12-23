# 校园拼车平台

一个专为校园设计的便捷、安全的拼车服务平台，连接有出行需求的学生和有空余座位的司机，提供高效的出行解决方案。

## 功能特性

### 学生端
- 搜索和筛选校园内外的拼车行程
- 申请感兴趣的行程
- 查看申请状态
- 管理个人信息

### 司机端
- 发布新的拼车行程（出发地、目的地、时间、价格、座位数）
- 管理行程申请（接受/拒绝）
- 查看已确认的乘客信息
- 计算行程总收入
- 管理车辆信息

### 管理员端
- 仪表盘统计（用户数、车辆数、行程数）
- 管理所有用户（查看、编辑、删除）
- 管理所有车辆（查看、编辑、删除）
- 管理所有行程（查看、编辑、删除）

### 通用功能
- 用户注册和登录（学生/司机/管理员角色）
- 响应式设计，支持移动端访问
- 实时状态更新
- 操作通知
- 现代化UI设计，基于Bootstrap 5

## 技术栈

### 后端
- **框架**: Flask (Python 3.10+)
- **数据库**: MySQL 8.0+
- **认证**: JWT (JSON Web Token)
- **数据库驱动**: PyMySQL
- **CORS**: Flask-CORS
- **连接池**: 自定义实现的数据库连接池

### 前端
- **框架**: 原生JavaScript
- **UI组件库**: Bootstrap 5
- **图标**: Font Awesome
- **HTTP客户端**: Fetch API

### 部署
- **服务器**: 支持Nginx + Gunicorn/uWSGI
- **系统服务**: systemd配置文件
- **快速部署**: 内置一键部署脚本

## 项目结构

```
./
├── config/              # 配置文件
│   └── database.py      # 数据库连接配置和连接池实现
├── controllers/         # 业务逻辑控制器
│   ├── admin_controller.py       # 管理员功能
│   ├── participant_controller.py # 参与者（乘客）管理
│   ├── trip_controller.py         # 行程管理
│   ├── user_controller.py         # 用户管理
│   └── vehicle_controller.py      # 车辆管理
├── middleware/          # 中间件
│   └── auth_middleware.py         # 认证中间件
├── routes/              # API路由
│   ├── admin_routes.py         # 管理员相关路由
│   ├── participant_routes.py   # 参与者相关路由
│   ├── trip_routes.py          # 行程相关路由
│   ├── user_routes.py          # 用户相关路由
│   └── vehicle_routes.py       # 车辆相关路由
├── scripts/             # 辅助脚本
│   ├── alter_participants_index.py    # 数据库索引维护
│   ├── check_trips.py                 # 行程检查工具
│   ├── check_users.py                 # 用户检查工具
│   └── check_vehicles.py              # 车辆检查工具
├── static/              # 静态资源
│   ├── css/            # 样式文件
│   ├── fonts/          # 字体文件
│   ├── js/             # JavaScript文件
│   └── index.html      # 主页面
├── test_database/       # 测试数据库脚本
├── utils/               # 工具函数
│   ├── auth_utils.py   # 认证工具
│   └── naming_utils.py # 命名转换工具
├── .env                 # 环境变量配置
├── DEPLOYMENT_GUIDE.md  # 详细部署指南
├── QUICK_DEPLOY.md      # 快速部署指南
├── README.md            # 项目说明文档
├── carpool_api.service  # Systemd服务配置
├── deploy.py            # 快速部署脚本
├── main.py              # 应用入口
└── requirements.txt     # 依赖包列表
```

## 数据库设计

### 核心表结构

#### 用户表 (users)
- `id`: 主键
- `student_id`: 学号（学生角色）
- `name`: 姓名
- `phone`: 手机号
- `email`: 邮箱
- `password`: 密码
- `avatar`: 头像
- `role`: 角色 (student/driver/admin)
- `rating`: 评分
- `total_ratings`: 评分总数
- `status`: 状态 (active/inactive/banned)

#### 车辆表 (vehicles)
- `id`: 主键
- `user_id`: 所属司机ID
- `plate_number`: 车牌号
- `brand`: 品牌
- `model`: 型号
- `color`: 颜色
- `seats`: 座位数
- `year`: 购买年份
- `status`: 状态 (active/inactive)

#### 行程表 (trips)
- `id`: 主键
- `driver_id`: 司机ID
- `vehicle_id`: 车辆ID
- `departure_location`: 出发地
- `arrival_location`: 目的地
- `departure_time`: 出发时间
- `available_seats`: 可用座位数
- `price_per_seat`: 座位单价
- `trip_status`: 行程状态 (pending/ongoing/completed/cancelled)

#### 参与者表 (participants)
- `id`: 主键
- `trip_id`: 行程ID
- `user_id`: 用户ID
- `seats_booked`: 预订座位数
- `participant_status`: 参与状态 (pending/accepted/rejected/completed/cancelled)
- `payment_status`: 支付状态 (unpaid/paid/refunded)

## 安装和配置

### 环境要求
- Python 3.10+
- MySQL 8.0+
- pip (Python包管理器)

### 安装步骤

#### 1. 克隆项目
```bash
git clone <repository-url>
cd db_test_py
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
. venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 配置数据库

1. 创建MySQL数据库：
```sql
CREATE DATABASE carpool_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 配置环境变量：
   复制或编辑 `.env` 文件并修改配置：
   ```env
   # 数据库配置
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=123123
   DB_NAME=carpool_db
   DB_PORT=3306
   
   # 应用配置
   SECRET_KEY=your_secret_key
   PORT=3000
   DEBUG=True
   ```

#### 5. 启动应用

```bash
python main.py
```

应用将在 `http://localhost:3000` 启动。

## 快速部署

本项目提供了一键快速部署脚本，适用于已安装Python和MySQL（密码为123123）的计算机。

### 使用方法

```bash
python deploy.py
```

部署脚本将自动完成以下操作：
- 检查Python版本
- 安装依赖
- 检查MySQL连接
- 创建数据库
- 配置环境变量
- 初始化数据库表
- 创建默认管理员账号
- 启动应用

详细说明请参考 `QUICK_DEPLOY.md` 文件。

## API接口

### 用户管理
- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/profile` - 获取当前用户信息

### 车辆管理
- `POST /api/vehicles` - 创建车辆
- `GET /api/vehicles` - 获取车辆列表
- `PUT /api/vehicles/:id` - 更新车辆信息
- `DELETE /api/vehicles/:id` - 删除车辆

### 行程管理
- `GET /api/trips` - 获取行程列表
- `POST /api/trips` - 创建新行程
- `GET /api/trips/:id` - 获取行程详情
- `PUT /api/trips/:id` - 更新行程信息
- `DELETE /api/trips/:id` - 删除行程

### 申请管理
- `POST /api/participants` - 创建行程申请
- `DELETE /api/participants/:id` - 取消申请
- `GET /api/participants/trips/:trip_id/applications` - 获取行程申请列表
- `PUT /api/participants/:id/status` - 更新申请状态

### 管理员API
- `GET /api/admin/dashboard` - 获取仪表盘统计
- `GET /api/admin/users` - 获取所有用户
- `PUT /api/admin/users/:id` - 更新用户信息
- `DELETE /api/admin/users/:id` - 删除用户
- `GET /api/admin/vehicles` - 获取所有车辆
- `PUT /api/admin/vehicles/:id` - 更新车辆信息
- `DELETE /api/admin/vehicles/:id` - 删除车辆
- `GET /api/admin/trips` - 获取所有行程
- `PUT /api/admin/trips/:id` - 更新行程信息
- `DELETE /api/admin/trips/:id` - 删除行程

## 使用说明

### 用户注册和登录

1. 访问平台首页
2. 选择用户角色（学生/司机/管理员）
3. 填写注册信息
4. 使用注册的账号登录

### 学生使用流程

1. 登录后，在首页搜索行程
2. 选择合适的行程，点击"申请"
3. 在"我的申请"中查看申请状态
4. 等待司机确认

### 司机使用流程

1. 登录后，点击"发布行程"
2. 填写行程信息（出发地、目的地、时间、价格、座位数等）
3. 在"我的行程"中管理行程
4. 点击"查看申请"处理学生的行程申请
5. 点击"查看乘客"查看已确认的乘客信息和行程收入

### 管理员使用流程

1. 使用管理员账号登录
2. 在仪表盘查看统计信息
3. 点击统计卡片跳转到对应管理页面
4. 管理用户、车辆和行程

## 部署指南

详细的部署步骤请参考 `DEPLOYMENT_GUIDE.md` 文件。

## 默认账户

- **管理员账号**: 13800138000 / password: admin123

## 许可证

MIT License

## 开发和维护

- 本项目使用 Flask 框架开发
- 数据库采用 MySQL 存储所有数据
- 所有API接口遵循 RESTful 设计规范
- 前端采用响应式设计，支持各种设备访问
- 提供完整的部署文档和快速部署脚本

## 注意事项

1. 本项目为校园内部使用设计，请勿用于商业用途
2. 使用前请确保已正确配置数据库连接
3. 生产环境部署时请关闭 DEBUG 模式
4. 定期备份数据库以防止数据丢失
5. 部署时请修改默认账户的密码