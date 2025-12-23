# 拼车应用API部署指南

## 项目概述
这是一个基于Flask的拼车应用API，使用MySQL数据库，提供用户认证、行程管理等功能。

## 部署环境要求
- Python 3.8+
- MySQL 5.7+
- Linux/Windows/macOS服务器

## 部署方式一：传统部署

### 1. 服务器准备

**Linux服务器**
```bash
# 更新系统
apt update && apt upgrade -y

# 安装Python3和pip
apt install python3 python3-pip python3-venv -y

# 安装MySQL服务器
apt install mysql-server -y
```

**Windows服务器**
- 下载并安装Python 3.8+：https://www.python.org/downloads/
- 下载并安装MySQL 5.7+：https://dev.mysql.com/downloads/mysql/

### 2. 数据库配置

**创建数据库**
```sql
CREATE DATABASE carpool_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**创建用户并授权**
```sql
CREATE USER 'carpool_user'@'%' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON carpool_db.* TO 'carpool_user'@'%';
FLUSH PRIVILEGES;
```

### 3. 项目部署

**克隆项目**
```bash
cd /opt
git clone <your-repository-url>
cd carpool_api
```

**创建虚拟环境**
```bash
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

**安装依赖**
```bash
pip install -r requirements.txt
```

**配置环境变量**
```bash
# 创建.env文件
cp .env.example .env

# 编辑.env文件，配置数据库和JWT信息
nano .env
```

**启动应用**
```bash
# 开发模式
python main.py

# 生产模式（推荐使用gunicorn）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 main:app
```

### 4. 配置反向代理（可选）

**安装Nginx**
```bash
apt install nginx -y
```

**配置Nginx**
```bash
nano /etc/nginx/sites-available/carpool_api
```

添加以下配置：
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**启用配置并重启Nginx**
```bash
ln -s /etc/nginx/sites-available/carpool_api /etc/nginx/sites-enabled/
nginx -t
nginx -s reload
```

## 部署方式二：Docker容器化部署

### 1. 安装Docker和Docker Compose

**Linux服务器**
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 2. 创建Docker配置文件

**创建Dockerfile**
```bash
nano Dockerfile
```

添加以下内容：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "main.py"]
```

**创建docker-compose.yml**
```bash
nano docker-compose.yml
```

添加以下内容：
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=your_secure_password
      - DB_NAME=carpool_db
      - JWT_SECRET=your_jwt_secret_key
      - JWT_EXPIRES_IN=24h
      - PORT=3000
      - DEBUG=False
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: mysql:5.7
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=your_secure_password
      - MYSQL_DATABASE=carpool_db
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

volumes:
  mysql_data:
```

### 3. 启动容器

```bash
docker-compose up -d
```

### 4. 验证部署

```bash
# 查看容器状态
docker-compose ps

# 查看应用日志
docker-compose logs app
```

## 部署后验证

1. **健康检查**
```bash
curl http://your_server_ip:3000/health
```

2. **API测试**
- 使用Postman或curl测试API端点
- 测试用户注册和登录功能

## 生产环境建议

1. **安全配置**
   - 更改默认的JWT_SECRET
   - 设置DEBUG=False
   - 使用HTTPS（配置SSL证书）
   - 限制数据库访问IP

2. **性能优化**
   - 调整Gunicorn的worker数量
   - 配置MySQL连接池
   - 启用Nginx缓存

3. **监控与日志**
   - 配置应用日志收集
   - 监控服务器资源使用
   - 设置错误报警

4. **备份策略**
   - 定期备份MySQL数据库
   - 备份.env配置文件
   - 实施版本控制

## 更新部署

**传统部署**
```bash
# 拉取最新代码
git pull

# 激活虚拟环境
source venv/bin/activate

# 安装新依赖
pip install -r requirements.txt

# 重启应用
systemctl restart carpool_api
```

**Docker部署**
```bash
docker-compose down
git pull
docker-compose up -d --build
```