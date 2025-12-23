from config.database import get_connection, close_connection

# 查询现有车辆
def check_vehicles():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, user_id, brand, model, plate_number FROM vehicles')
        vehicles = cursor.fetchall()
        print('现有车辆：')
        if not vehicles:
            print('暂无车辆信息')
        else:
            for vehicle in vehicles:
                print(f'ID: {vehicle["id"]}, 用户ID: {vehicle["user_id"]}, 品牌: {vehicle["brand"]}, 型号: {vehicle["model"]}, 车牌号: {vehicle["plate_number"]}')
    finally:
        close_connection(conn)

if __name__ == '__main__':
    check_vehicles()