// 应用程序类
class CarpoolApp {
    constructor() {
        this.currentUser = null;
        this.token = null;
        this.init();
    }

    // 初始化应用
    init() {
        this.bindEvents();
        this.checkAuth();
        this.loadTrips();
    }

    // 绑定事件
    bindEvents() {
        // 导航栏按钮事件
        const loginBtn = document.getElementById('loginBtn');
        if (loginBtn) loginBtn.addEventListener('click', () => this.openLoginModal());
        
        const registerBtn = document.getElementById('registerBtn');
        if (registerBtn) registerBtn.addEventListener('click', () => this.openRegisterModal());
        
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) logoutBtn.addEventListener('click', () => this.logout());
        
        const createTripBtn = document.getElementById('createTripBtn');
        if (createTripBtn) createTripBtn.addEventListener('click', () => this.openCreateTripModal());
        
        const createTripBtnMain = document.getElementById('createTripBtnMain');
        if (createTripBtnMain) createTripBtnMain.addEventListener('click', () => this.openCreateTripModal());
        
        const addVehicleBtn = document.getElementById('addVehicleBtn');
        if (addVehicleBtn) addVehicleBtn.addEventListener('click', () => this.openAddVehicleModal());
        

        
        const myApplicationsBtn = document.getElementById('myApplicationsBtn');
        if (myApplicationsBtn) myApplicationsBtn.addEventListener('click', () => this.loadMyApplications());
        
        const backToTripsBtn = document.getElementById('backToTripsBtn');
        if (backToTripsBtn) backToTripsBtn.addEventListener('click', () => this.backToTrips());

        const backToDriverTripsBtn = document.getElementById('backToDriverTripsBtn');
        if (backToDriverTripsBtn) backToDriverTripsBtn.addEventListener('click', () => this.backToTrips());

        // 搜索事件
        const searchBtn = document.getElementById('searchBtn');
        if (searchBtn) searchBtn.addEventListener('click', () => this.searchTrips());
        
        // 管理员按钮事件
        const adminDashboardBtn = document.getElementById('adminDashboardBtn');
        if (adminDashboardBtn) adminDashboardBtn.addEventListener('click', () => this.adminShowDashboard());
        
        const adminUsersBtn = document.getElementById('adminUsersBtn');
        if (adminUsersBtn) adminUsersBtn.addEventListener('click', () => this.adminLoadUsers());
        
        const adminVehiclesBtn = document.getElementById('adminVehiclesBtn');
        if (adminVehiclesBtn) adminVehiclesBtn.addEventListener('click', () => this.adminLoadVehicles());
        
        const adminTripsBtn = document.getElementById('adminTripsBtn');
        if (adminTripsBtn) adminTripsBtn.addEventListener('click', () => this.adminLoadTrips());
        
        const addUserBtn = document.getElementById('addUserBtn');
        if (addUserBtn) addUserBtn.addEventListener('click', () => this.adminAddUser());
        
        const addVehicleAdminBtn = document.getElementById('addVehicleAdminBtn');
        if (addVehicleAdminBtn) addVehicleAdminBtn.addEventListener('click', () => this.adminAddVehicle());
        
        // 编辑用户表单事件
        const editUserForm = document.getElementById('editUserForm');
        if (editUserForm) editUserForm.addEventListener('submit', (e) => this.handleEditUser(e));
        
        // 编辑用户角色切换事件
        const editUserRole = document.getElementById('editUserRole');
        if (editUserRole) editUserRole.addEventListener('change', (e) => this.toggleEditUserFields(e));
        
        // 添加用户表单事件
        const addUserForm = document.getElementById('addUserForm');
        if (addUserForm) addUserForm.addEventListener('submit', (e) => this.handleAddUser(e));
        
        // 编辑车辆表单事件
        const editVehicleForm = document.getElementById('editVehicleForm');
        if (editVehicleForm) editVehicleForm.addEventListener('submit', (e) => this.handleEditVehicle(e));
        
        // 编辑行程表单事件
        const editTripForm = document.getElementById('editTripForm');
        if (editTripForm) editTripForm.addEventListener('submit', (e) => this.handleEditTrip(e));
        


        // 登录模态框事件
        const loginForm = document.getElementById('loginForm');
        if (loginForm) loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        
        const loginRole = document.getElementById('loginRole');
        if (loginRole) loginRole.addEventListener('change', (e) => this.toggleLoginFields(e));
        
        const switchToRegister = document.getElementById('switchToRegister');
        if (switchToRegister) switchToRegister.addEventListener('click', (e) => {
            e.preventDefault();
            this.openRegisterModal();
        });

        // 注册模态框事件
        const registerForm = document.getElementById('registerForm');
        if (registerForm) registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        
        const registerRole = document.getElementById('registerRole');
        if (registerRole) registerRole.addEventListener('change', (e) => this.toggleRegisterFields(e));
        
        const switchToLogin = document.getElementById('switchToLogin');
        if (switchToLogin) switchToLogin.addEventListener('click', (e) => {
            e.preventDefault();
            this.openLoginModal();
        });

        // 行程创建模态框事件
        const createTripForm = document.getElementById('createTripForm');
        if (createTripForm) createTripForm.addEventListener('submit', (e) => this.handleCreateTrip(e));

        // 车辆添加模态框事件
        const addVehicleForm = document.getElementById('addVehicleForm');
        if (addVehicleForm) {
            // 移除旧的事件监听器
            addVehicleForm.removeEventListener('submit', this.handleAddVehicle);
            // 添加新的事件监听器，根据用户角色选择处理函数
            addVehicleForm.addEventListener('submit', (e) => {
                if (this.currentUser && this.currentUser.role === 'admin') {
                    this.handleAdminAddVehicle(e);
                } else {
                    this.handleAddVehicle(e);
                }
            });
        }

        // 初始化时切换登录字段
        const loginRoleSelect = document.getElementById('loginRole');
        if (loginRoleSelect) this.toggleLoginFields({ target: loginRoleSelect });
        
        const registerRoleSelect = document.getElementById('registerRole');
        if (registerRoleSelect) this.toggleRegisterFields({ target: registerRoleSelect });
    }

    // 切换登录字段显示
    toggleLoginFields(e) {
        const role = e.target.value;
        const studentIdGroup = document.getElementById('loginStudentIdGroup');
        const phoneGroup = document.getElementById('loginPhoneGroup');
        const studentIdInput = document.getElementById('loginStudentId');
        const phoneInput = document.getElementById('loginPhone');

        if (role === 'student') {
            studentIdGroup.classList.remove('d-none');
            phoneGroup.classList.add('d-none');
            studentIdInput.required = true;
            phoneInput.required = false;
            phoneInput.value = ''; // 清空手机号输入
        } else {
            studentIdGroup.classList.add('d-none');
            phoneGroup.classList.remove('d-none');
            studentIdInput.required = false;
            phoneInput.required = true;
            studentIdInput.value = ''; // 清空学号输入
        }
    }

    // 切换注册字段显示
    toggleRegisterFields(e) {
        const role = e.target.value;
        const studentIdGroup = document.getElementById('registerStudentIdGroup');

        if (role === 'student') {
            studentIdGroup.classList.remove('d-none');
            document.getElementById('registerStudentId').required = true;
        } else {
            studentIdGroup.classList.add('d-none');
            document.getElementById('registerStudentId').required = false;
        }
    }
    
    // 切换编辑用户字段显示
    toggleEditUserFields(e) {
        const role = e.target.value;
        const studentIdGroup = document.querySelector('#editUserModal .mb-3:has(#editUserStudentId)');
        
        if (role === 'student') {
            studentIdGroup.classList.remove('d-none');
        } else {
            studentIdGroup.classList.add('d-none');
            document.getElementById('editUserStudentId').value = ''; // 清空学号输入
        }
    }

    // 打开登录模态框
    openLoginModal() {
        this.hideAllModals();
        const modal = new bootstrap.Modal(document.getElementById('loginModal'));
        modal.show();
    }

    // 打开注册模态框
    openRegisterModal() {
        this.hideAllModals();
        const modal = new bootstrap.Modal(document.getElementById('registerModal'));
        modal.show();
    }

    // 加载司机的车辆列表
    async loadDriverVehicles() {
        try {
            const response = await this.apiRequest('/api/vehicles', 'GET');
            const vehicles = response;
            
            const vehicleSelect = document.getElementById('createVehicle');
            if (vehicleSelect) {
                // 清空现有选项
                vehicleSelect.innerHTML = '';
                
                // 添加车辆选项
                vehicles.forEach(vehicle => {
                    const option = document.createElement('option');
                    option.value = vehicle.id;
                    option.textContent = `${vehicle.plateNumber} - ${vehicle.brand} ${vehicle.model}`;
                    vehicleSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('加载车辆列表失败:', error);
            this.showMessage('加载车辆列表失败，请稍后重试', 'error');
        }
    }

    // 打开创建行程模态框
    openCreateTripModal() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            return;
        }

        if (this.currentUser && this.currentUser.role !== 'driver') {
            this.showMessage('只有司机可以发布行程', 'error');
            return;
        }

        const modal = new bootstrap.Modal(document.getElementById('createTripModal'));
        modal.show();
        
        // 加载司机的车辆列表
        this.loadDriverVehicles();
    }

    // 打开添加车辆模态框
    openAddVehicleModal() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            return;
        }

        if (this.currentUser && this.currentUser.role !== 'driver') {
            this.showMessage('只有司机可以添加车辆', 'error');
            return;
        }

        const modal = new bootstrap.Modal(document.getElementById('addVehicleModal'));
        modal.show();
        
        // 隐藏司机选择框，因为司机只能添加自己的车辆
        const driverSelectGroup = document.querySelector('#vehicleDriver').closest('.mb-3');
        const driverSelect = document.getElementById('vehicleDriver');
        if (driverSelectGroup) {
            driverSelectGroup.classList.add('d-none');
        }
        // 移除required属性，否则表单会因为必填字段没有值而无法提交
        if (driverSelect) {
            driverSelect.required = false;
        }
    }

    // 隐藏所有模态框
    hideAllModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        });
    }

    // 检查认证状态
    checkAuth() {
        this.token = localStorage.getItem('token');
        if (this.token) {
            this.getUserInfo();
        }
    }

    // 获取用户信息
    async getUserInfo() {
        try {
            const response = await this.apiRequest('/api/users/me', 'GET');
            this.currentUser = response;
            this.updateUI();
        } catch (error) {
            console.error('获取用户信息失败:', error);
            this.logout();
        }
    }

    // 登录处理
    async handleLogin(e) {
        e.preventDefault();
        const role = document.getElementById('loginRole').value;
        const password = document.getElementById('loginPassword').value;

        let data;
        if (role === 'student') {
            const studentId = document.getElementById('loginStudentId').value;
            data = { studentId, password, role };
        } else {
            const phone = document.getElementById('loginPhone').value;
            data = { phone, password, role };
        }

        try {
            const response = await this.apiRequest('/api/users/login', 'POST', data);
            this.token = response.token;
            localStorage.setItem('token', this.token);
            await this.getUserInfo();
            this.hideAllModals();
            this.showMessage('登录成功', 'success');
        } catch (error) {
            this.showMessage(error.message || '登录失败', 'error');
        }
    }

    // 注册处理
    async handleRegister(e) {
        e.preventDefault();
        const name = document.getElementById('registerName').value;
        const phone = document.getElementById('registerPhone').value;
        const password = document.getElementById('registerPassword').value;
        const role = document.getElementById('registerRole').value;

        const data = { name, phone, password, role };

        if (role === 'student') {
            data.studentId = document.getElementById('registerStudentId').value;
        }

        try {
            const response = await this.apiRequest('/api/users/register', 'POST', data);
            this.hideAllModals();
            this.showMessage('注册成功，请登录', 'success');
            this.openLoginModal();
        } catch (error) {
            this.showMessage(error.message || '注册失败', 'error');
        }
    }

    // 登出处理
    logout() {
        this.currentUser = null;
        this.token = null;
        localStorage.removeItem('token');
        this.updateUI();
        this.showMessage('已退出登录', 'success');
    }

    // 创建行程处理
    async handleCreateTrip(e) {
        e.preventDefault();
        const departure = document.getElementById('createDeparture').value;
        const arrival = document.getElementById('createArrival').value;
        const departureTime = document.getElementById('createDepartureTime').value;
        const seats = document.getElementById('createSeats').value;
        const price = document.getElementById('createPrice').value;
        const vehicleId = document.getElementById('createVehicle').value;

        // 使用与后端一致的驼峰命名格式
        const data = {
            departureLocation: departure,
            arrivalLocation: arrival,
            departureTime: departureTime,
            availableSeats: seats,
            pricePerSeat: price,
            vehicleId: vehicleId
        };

        try {
            const response = await this.apiRequest('/api/trips', 'POST', data);
            this.hideAllModals();
            this.loadTrips();
            this.showMessage('行程发布成功', 'success');
            // 清空表单
            e.target.reset();
        } catch (error) {
            this.showMessage(error.message || '行程发布失败', 'error');
        }
    }

    // 添加车辆处理
    async handleAddVehicle(e) {
        e.preventDefault();
        const plateNumber = document.getElementById('vehiclePlateNumber').value;
        const brand = document.getElementById('vehicleBrand').value;
        const model = document.getElementById('vehicleModel').value;
        const color = document.getElementById('vehicleColor').value;
        const seats = document.getElementById('vehicleSeats').value;
        const year = document.getElementById('vehicleYear').value;

        const data = {
            plateNumber,
            brand,
            model,
            color,
            seats,
            year: year || null
        };

        try {
            const response = await this.apiRequest('/api/vehicles', 'POST', data);
            this.hideAllModals();
            this.showMessage('车辆添加成功', 'success');
            // 清空表单
            e.target.reset();
        } catch (error) {
            this.showMessage(error.message || '车辆添加失败', 'error');
        }
    }

    // 搜索行程
    async searchTrips() {
        const departure = document.getElementById('departureInput').value;
        const arrival = document.getElementById('arrivalInput').value;
        const date = document.getElementById('dateInput').value;

        try {
            // 根据用户角色决定调用的API端点
            const baseUrl = this.currentUser && this.currentUser.role === 'driver' ? '/api/trips/driver' : '/api/trips';
            let url = `${baseUrl}?departureLocation=${departure}&arrivalLocation=${arrival}`;
            if (date) {
                url += `&departureDate=${date}`;
            }
            
            const response = await this.apiRequest(url, 'GET');
            
            // 根据用户角色渲染不同的行程列表
            if (this.currentUser && this.currentUser.role === 'driver') {
                this.renderDriverTrips(response);
            } else {
                this.renderTrips(response);
            }
        } catch (error) {
            this.showMessage('搜索行程失败', 'error');
        }
    }

    // 加载行程列表
    async loadTrips() {
        try {
            const response = await this.apiRequest('/api/trips', 'GET');
            this.renderTrips(response);
        } catch (error) {
            this.showMessage('加载行程失败', 'error');
        }
    }

    // 渲染行程列表
    renderTrips(trips) {
        const tripList = document.getElementById('tripList');
        if (!tripList) return;

        if (trips.length === 0) {
            tripList.innerHTML = `
                <div class="col-12 text-center text-muted py-5">
                    <i class="fas fa-search fa-3x mb-3 d-block"></i>
                    <h3 class="h5 mb-2">还没有找到行程</h3>
                    <p>请输入搜索条件查找合适的行程</p>
                </div>
            `;
            return;
        }

        const tripCards = trips.map(trip => this.createTripCard(trip)).join('');
        tripList.innerHTML = tripCards;
    }

    // 创建行程卡片
    createTripCard(trip) {
        // 处理GMT格式的时间字符串，确保日期显示正确
        // GMT时间字符串格式：Tue, 23 Dec 2025 10:00:00 GMT
        const departureTime = trip.departureTime;
        // 直接从字符串中提取日期部分：23 Dec 2025
        const datePart = departureTime.match(/\w{3},\s+(\d{1,2}\s+\w{3}\s+\d{4})/)[1];
        // 解析为日期对象
        const date = new Date(datePart);
        // 格式化日期为YYYY/MM/DD
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const formattedDate = `${year}/${month}/${day}`;
        // 提取时间部分：10:00
        const timePart = departureTime.match(/\d{2}:\d{2}:\d{2}/)[0].substring(0, 5);
        const formattedTime = timePart;

        return `
            <div class="col-lg-4 col-md-6">
                <div class="trip-card h-100">
                    <div class="trip-card-header">
                        <h5 class="mb-0">${trip.departureLocation} → ${trip.arrivalLocation}</h5>
                    </div>
                    <div class="trip-card-body">
                        <div class="trip-time mb-3">
                            <i class="fas fa-calendar-alt me-2"></i>${formattedDate}
                            <i class="fas fa-clock ms-4 me-2"></i>${formattedTime}
                        </div>
                        <div class="trip-info">
                            <i class="fas fa-user"></i>
                            <span>司机: ${trip.driver.name}</span>
                        </div>
                        <div class="trip-info">
                            <i class="fas fa-car"></i>
                            <span>${trip.vehicle?.brand || '未知'} ${trip.vehicle?.model || '车辆'}</span>
                        </div>
                        <div class="trip-details">
                            <div>
                                <span class="trip-price">¥${trip.pricePerSeat}</span>
                                <span class="trip-seats">/人</span>
                            </div>
                            <div class="trip-seats">
                                剩余座位: ${trip.availableSeats}
                            </div>
                        </div>
                        <button class="btn btn-primary w-100 mt-3" onclick="app.applyForTrip(${trip.id})">
                            <i class="fas fa-paper-plane me-2"></i>申请拼车
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // 申请拼车
    async applyForTrip(tripId) {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            this.openLoginModal();
            return;
        }

        if (this.currentUser && this.currentUser.role !== 'student') {
            this.showMessage('只有学生可以申请拼车', 'error');
            return;
        }

        try {
            const response = await this.apiRequest(`/api/participants/trip/${tripId}`, 'POST');
            this.showMessage('申请成功', 'success');
        } catch (error) {
            this.showMessage(error.message || '申请失败', 'error');
        }
    }

    // 查看申请
    async viewApplications(tripId = null) {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            return;
        }

        if (this.currentUser && this.currentUser.role !== 'driver') {
            this.showMessage('只有司机可以查看申请', 'error');
            return;
        }

        try {
            const response = await this.apiRequest(`/api/participants/trips/${tripId}/applications`, 'GET');
            this.renderApplications(response, tripId);
            
            // 显示模态框
            const modal = new bootstrap.Modal(document.getElementById('viewApplicationsModal'));
            modal.show();
        } catch (error) {
            this.showMessage(error.message || '查看申请失败', 'error');
        }
    }

    // 渲染申请列表
    renderApplications(applications, tripId) {
        const applicationsList = document.getElementById('applicationsList');
        if (!applicationsList) return;

        if (applications.length === 0) {
            applicationsList.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fas fa-inbox fa-3x mb-3 d-block"></i>
                    <h3 class="h5 mb-2">暂无申请</h3>
                    <p>还没有学生申请这个行程</p>
                </div>
            `;
            return;
        }

        const applicationItems = applications.map(application => this.createApplicationItem(application, tripId)).join('');
        applicationsList.innerHTML = applicationItems;
    }

    // 创建申请项
    createApplicationItem(application, tripId) {
        const student = application.student;
        const date = new Date(application.createdAt);
        const formattedDate = date.toLocaleString('zh-CN');

        return `
            <div class="application-item card mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h5 class="card-title mb-1">${student.name || '未知'}</h5>
                            <p class="card-text text-muted">学号: ${student.studentId || '未知'}</p>
                            <p class="card-text text-muted">申请时间: ${isNaN(date.getTime()) ? '未知' : formattedDate}</p>
                            <p class="card-text">申请座位数: ${application.seatsBooked === undefined || application.seatsBooked === null ? 1 : application.seatsBooked}人</p>
                        </div>
                        <div>
                            <button class="btn btn-success me-2" onclick="app.handleApplication(${application.id}, 'accepted')">
                                <i class="fas fa-check me-1"></i>同意
                            </button>
                            <button class="btn btn-danger" onclick="app.handleApplication(${application.id}, 'rejected')">
                                <i class="fas fa-times me-1"></i>拒绝
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // 处理申请
    async handleApplication(applicationId, status) {
        try {
            const response = await this.apiRequest(`/api/participants/${applicationId}/status`, 'PUT', { status });
            this.showMessage(`申请${status === 'accepted' ? '已同意' : '已拒绝'}`, 'success');
            
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('viewApplicationsModal'));
            if (modal) modal.hide();
            
            // 重新加载司机行程
            this.loadDriverTrips();
        } catch (error) {
            this.showMessage(error.message || '处理申请失败', 'error');
        }
    }

    // 加载司机行程列表
    async loadDriverTrips() {
        try {
            const response = await this.apiRequest('/api/trips/driver', 'GET');
            this.renderDriverTrips(response);
        } catch (error) {
            this.showMessage('加载行程失败', 'error');
        }
    }

    // 渲染司机行程列表
    renderDriverTrips(trips) {
        const driverTripList = document.getElementById('driverTripList');
        if (!driverTripList) return;

        if (trips.length === 0) {
            driverTripList.innerHTML = `
                <div class="col-12 text-center text-muted py-5">
                    <i class="fas fa-car fa-3x mb-3 d-block"></i>
                    <h3 class="h5 mb-2">还没有发布任何行程</h3>
                    <p>点击"发布行程"按钮开始创建您的第一个行程</p>
                </div>
            `;
            return;
        }

        const tripCards = trips.map(trip => this.createDriverTripCard(trip)).join('');
        driverTripList.innerHTML = tripCards;
    }

    // 创建司机行程卡片
    createDriverTripCard(trip) {
        // 处理GMT格式的时间字符串，确保日期显示正确
        // GMT时间字符串格式：Tue, 23 Dec 2025 10:00:00 GMT
        const departureTime = trip.departureTime;
        // 直接从字符串中提取日期部分：23 Dec 2025
        const datePart = departureTime.match(/\w{3},\s+(\d{1,2}\s+\w{3}\s+\d{4})/)[1];
        // 解析为日期对象
        const date = new Date(datePart);
        // 格式化日期为YYYY/MM/DD
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const formattedDate = `${year}/${month}/${day}`;
        // 提取时间部分：10:00
        const timePart = departureTime.match(/\d{2}:\d{2}:\d{2}/)[0].substring(0, 5);
        const formattedTime = timePart;

        return `
            <div class="col-lg-4 col-md-6">
                <div class="trip-card h-100">
                    <div class="trip-card-header">
                        <h5 class="mb-0">${trip.departureLocation} → ${trip.arrivalLocation}</h5>
                    </div>
                    <div class="trip-card-body">
                        <div class="trip-time mb-3">
                            <i class="fas fa-calendar-alt me-2"></i>${formattedDate}
                            <i class="fas fa-clock ms-4 me-2"></i>${formattedTime}
                        </div>
                        <div class="trip-info">
                            <i class="fas fa-car"></i>
                            <span>${trip.vehicle.brand} ${trip.vehicle.model}</span>
                        </div>
                        <div class="trip-details">
                            <div>
                                <span class="trip-price">¥${trip.pricePerSeat}</span>
                                <span class="trip-seats">/人</span>
                            </div>
                            <div class="trip-seats">
                                剩余座位: ${trip.availableSeats}
                            </div>
                        </div>
                        <div class="d-flex flex-wrap gap-2 mt-3">
                            <button class="btn btn-primary flex-1" onclick="app.viewApplications(${trip.id})">
                                <i class="fas fa-list-alt me-2"></i>查看申请
                            </button>
                            <button class="btn btn-info flex-1" onclick="app.viewPassengers(${trip.id})">
                                <i class="fas fa-users me-2"></i>查看乘客
                            </button>
                            <button class="btn btn-danger flex-1" onclick="app.deleteTrip(${trip.id})">
                                <i class="fas fa-trash-alt me-2"></i>删除
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // 删除行程
    async deleteTrip(tripId) {
        if (!confirm('确定要删除这个行程吗？删除后将无法恢复。')) {
            return;
        }

        try {
            const response = await this.apiRequest(`/api/trips/${tripId}`, 'DELETE');
            this.showMessage('行程删除成功', 'success');
            this.loadDriverTrips();
        } catch (error) {
            this.showMessage(error.message || '删除行程失败', 'error');
        }
    }

    // 返回行程列表
    backToTrips() {
        // 显示行程列表，隐藏其他区域
        const studentTripsSection = document.getElementById('studentTripsSection');
        const driverTripsSection = document.getElementById('driverTripsSection');
        const myApplicationsSection = document.getElementById('myApplicationsSection');
        const passengersSection = document.getElementById('passengersSection');
        
        if (this.currentUser && this.currentUser.role === 'driver') {
            // 司机返回时显示司机行程列表
            if (driverTripsSection) driverTripsSection.classList.remove('d-none');
            if (studentTripsSection) studentTripsSection.classList.add('d-none');
            this.loadDriverTrips();
        } else {
            // 学生或未登录用户返回时显示公共行程列表
            if (studentTripsSection) studentTripsSection.classList.remove('d-none');
            if (driverTripsSection) driverTripsSection.classList.add('d-none');
            this.loadTrips();
        }
        
        // 隐藏其他所有区域
        if (myApplicationsSection) myApplicationsSection.classList.add('d-none');
        if (passengersSection) passengersSection.classList.add('d-none');
    }
    
    // 查看行程乘客
    async viewPassengers(tripId) {
        if (!tripId) {
            this.showMessage('行程ID无效', 'error');
            return;
        }
        
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            this.openLoginModal();
            return;
        }
        
        if (this.currentUser && this.currentUser.role !== 'driver') {
            this.showMessage('只有司机可以查看乘客信息', 'error');
            return;
        }
        
        // 显示加载状态
        const passengersList = document.getElementById('passengersList');
        const totalIncome = document.getElementById('totalIncome');
        
        if (passengersList) {
            passengersList.innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
                    <h3 class="h5 mt-3">正在加载乘客信息...</h3>
                    <p class="text-muted">请稍候...</p>
                </div>
            `;
        }
        
        if (totalIncome) {
            totalIncome.textContent = '总收入: ¥0.00';
        }
        
        try {
            // 切换到乘客信息区域
            const driverTripsSection = document.getElementById('driverTripsSection');
            const passengersSection = document.getElementById('passengersSection');
            
            if (driverTripsSection) driverTripsSection.classList.add('d-none');
            if (passengersSection) passengersSection.classList.remove('d-none');
            
            const response = await this.apiRequest(`/api/participants/trips/${tripId}/passengers`, 'GET');
            this.renderPassengers(response);
            
        } catch (error) {
            console.error('查看乘客信息失败:', error);
            this.showMessage(error.message || '查看乘客信息失败，请稍后重试', 'error');
            
            // 恢复行程列表显示
            this.backToTrips();
        }
    }
    
    // 渲染乘客列表
    renderPassengers(data) {
        const passengersList = document.getElementById('passengersList');
        const totalIncome = document.getElementById('totalIncome');
        
        if (!passengersList || !totalIncome) return;
        
        // 添加调试信息
        console.log('渲染乘客列表，数据:', data);
        
        // 添加数据校验
        if (!data || !Array.isArray(data.passengers)) {
            passengersList.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fas fa-exclamation-circle fa-3x mb-3 d-block"></i>
                    <h3 class="h5 mb-2">数据加载错误</h3>
                    <p>无法获取乘客信息，请稍后重试</p>
                </div>
            `;
            totalIncome.textContent = '总收入: ¥0.00';
            return;
        }
        
        if (data.passengers.length === 0) {
            console.log('没有乘客数据');
            passengersList.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fas fa-users fa-3x mb-3 d-block"></i>
                    <h3 class="h5 mb-2">暂无乘客</h3>
                    <p>该行程还没有乘客确认</p>
                </div>
            `;
        } else {
            console.log('有乘客数据:', data.passengers);
            console.log('乘客数量:', data.passengers.length);
            const passengerItems = data.passengers.map((passenger, index) => {
                console.log(`处理乘客${index}:`, passenger);
                // 确保乘客数据完整
                const studentName = passenger.student?.name || '未知';
                const studentId = passenger.student?.studentId || '未知';
                const studentPhone = passenger.student?.phone || '未知';
                const seatsBooked = passenger.seatsBooked || 1;
                const paymentStatus = passenger.paymentStatus || 'unknown';
                
                // 支付状态样式
                let paymentStatusText = '未知';
                let paymentStatusClass = 'text-secondary';
                
                if (paymentStatus === 'paid') {
                    paymentStatusText = '已支付';
                    paymentStatusClass = 'text-success';
                } else if (paymentStatus === 'unpaid') {
                    paymentStatusText = '未支付';
                    paymentStatusClass = 'text-danger';
                }
                
                const passengerHTML = `
                    <div class="card mb-3">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h5 class="card-title mb-1">${studentName}</h5>
                                    <p class="card-text text-muted">学号: ${studentId}</p>
                                    <p class="card-text text-muted">电话: ${studentPhone}</p>
                                    <p class="card-text">座位数: ${seatsBooked}人</p>
                                    <p class="card-text ${paymentStatusClass}">支付状态: ${paymentStatusText}</p>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-primary">¥${((data.pricePerSeat || 0) * seatsBooked).toFixed(2)}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                console.log(`生成的HTML:`, passengerHTML);
                return passengerHTML;
            }).join('');
            
            console.log('最终生成的乘客列表HTML:', passengerItems);
            passengersList.innerHTML = passengerItems;
        }
        
        // 更新总收入
        totalIncome.textContent = `总收入: ¥${(data.totalIncome || 0).toFixed(2)}`;
    }

    // 加载我的申请
    async loadMyApplications() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            return;
        }

        if (this.currentUser && this.currentUser.role !== 'student') {
            this.showMessage('只有学生可以查看申请结果', 'error');
            return;
        }

        try {
            const response = await this.apiRequest('/api/participants/student', 'GET');
            this.renderMyApplications(response);
            
            // 显示申请结果区域，隐藏行程列表
            document.getElementById('studentTripsSection').classList.add('d-none');
            document.getElementById('myApplicationsSection').classList.remove('d-none');
        } catch (error) {
            this.showMessage(error.message || '加载申请结果失败', 'error');
        }
    }

    // 删除申请
    async deleteApplication(applicationId, participantStatus) {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'error');
            return;
        }

        if (this.currentUser && this.currentUser.role !== 'student') {
            this.showMessage('只有学生可以取消申请', 'error');
            return;
        }

        // 根据申请状态显示不同的确认信息
        let confirmMessage;
        if (participantStatus === 'accepted') {
            confirmMessage = '确定要取消已同意的申请吗？这将扣除您的信誉分。';
        } else {
            confirmMessage = '确定要取消这个申请吗？';
        }

        if (!confirm(confirmMessage)) {
            return;
        }

        try {
            const response = await this.apiRequest(`/api/participants/${applicationId}`, 'DELETE');
            this.showMessage('申请已取消', 'success');
            // 重新加载申请列表
            this.loadMyApplications();
        } catch (error) {
            this.showMessage(error.message || '取消申请失败', 'error');
        }
    }

    // 渲染我的申请
    renderMyApplications(applications) {
        const applicationsList = document.getElementById('myApplicationsList');
        if (!applicationsList) return;

        if (applications.length === 0) {
            applicationsList.innerHTML = `
                <div class="col-12 text-center text-muted py-5">
                    <i class="fas fa-file-alt fa-3x mb-3 d-block"></i>
                    <h3 class="h5 mb-2">还没有提交任何申请</h3>
                    <p>去查找合适的行程并提交申请吧</p>
                </div>
            `;
            return;
        }

        const applicationItems = applications.map(application => this.createMyApplicationItem(application)).join('');
        applicationsList.innerHTML = applicationItems;
    }

    // 创建我的申请项
    createMyApplicationItem(application) {
        // 处理GMT格式的时间字符串，确保日期显示正确
        // GMT时间字符串格式：Tue, 23 Dec 2025 10:00:00 GMT
        const departureTime = application.trip.departureTime;
        // 直接从字符串中提取日期部分：23 Dec 2025
        const datePart = departureTime.match(/\w{3},\s+(\d{1,2}\s+\w{3}\s+\d{4})/)[1];
        // 解析为日期对象
        const date = new Date(datePart);
        // 格式化日期为YYYY/MM/DD
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const formattedDate = `${year}/${month}/${day}`;
        // 提取时间部分：10:00
        const timePart = departureTime.match(/\d{2}:\d{2}:\d{2}/)[0].substring(0, 5);
        const formattedTime = timePart;
        
        let statusText = '待处理';
        let statusClass = 'badge-warning';
        
        if (application.participantStatus === 'accepted') {
            statusText = '已同意';
            statusClass = 'badge-success';
        } else if (application.participantStatus === 'rejected') {
            statusText = '已拒绝';
            statusClass = 'badge-danger';
        }

        return `
            <div class="col-lg-4 col-md-6">
                <div class="trip-card h-100">
                    <div class="trip-card-header">
                        <h5 class="mb-0">${application.trip.departureLocation} → ${application.trip.arrivalLocation}</h5>
                        <span class="badge ${statusClass}">${statusText}</span>
                    </div>
                    <div class="trip-card-body">
                        <div class="trip-time mb-3">
                            <i class="fas fa-calendar-alt me-2"></i>${formattedDate}
                            <i class="fas fa-clock ms-4 me-2"></i>${formattedTime}
                        </div>
                        <div class="trip-info">
                            <i class="fas fa-user"></i>
                            <span>司机: ${application.driver.name}</span>
                        </div>
                        <div class="trip-info">
                            <i class="fas fa-car"></i>
                            <span>${application.trip.vehicle?.brand || '未知'} ${application.trip.vehicle?.model || '车辆'}</span>
                        </div>
                        <div class="trip-details">
                            <div>
                                <span class="trip-price">¥${application.trip.pricePerSeat}</span>
                                <span class="trip-seats">/人</span>
                            </div>
                            <div class="trip-seats">
                                申请座位: ${application.seatsBooked || 1}人
                            </div>
                        </div>
                        ${application.participantStatus === 'pending' || application.participantStatus === 'accepted' ? `
                        <button class="btn btn-danger w-100 mt-3" onclick="app.deleteApplication(${application.id}, '${application.participantStatus}')">
                            <i class="fas fa-trash-alt me-2"></i>取消申请
                        </button>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    // 更新UI状态
    updateUI() {
        const isAuthenticated = this.isAuthenticated();

        // 更新导航栏
        const loginBtn = document.getElementById('loginBtn');
        if (loginBtn) loginBtn.classList.toggle('d-none', isAuthenticated);
        
        const registerBtn = document.getElementById('registerBtn');
        if (registerBtn) registerBtn.classList.toggle('d-none', isAuthenticated);
        
        const userInfo = document.getElementById('userInfo');
        if (userInfo) userInfo.classList.toggle('d-none', !isAuthenticated);

        // 管理员相关按钮（无论登录状态都检查，确保未登录时隐藏）
        const adminDashboardBtn = document.getElementById('adminDashboardBtn');
        if (adminDashboardBtn) adminDashboardBtn.classList.toggle('d-none', !isAuthenticated || !this.currentUser || this.currentUser.role !== 'admin');
        
        const adminUsersBtn = document.getElementById('adminUsersBtn');
        if (adminUsersBtn) adminUsersBtn.classList.toggle('d-none', !isAuthenticated || !this.currentUser || this.currentUser.role !== 'admin');
        
        const adminVehiclesBtn = document.getElementById('adminVehiclesBtn');
        if (adminVehiclesBtn) adminVehiclesBtn.classList.toggle('d-none', !isAuthenticated || !this.currentUser || this.currentUser.role !== 'admin');
        
        const adminTripsBtn = document.getElementById('adminTripsBtn');
        if (adminTripsBtn) adminTripsBtn.classList.toggle('d-none', !isAuthenticated || !this.currentUser || this.currentUser.role !== 'admin');

        if (isAuthenticated && this.currentUser) {
            const userName = document.getElementById('userName');
            if (userName) userName.textContent = this.currentUser.name;

            // 根据角色显示不同按钮
            const isDriver = this.currentUser.role === 'driver';
            const isAdmin = this.currentUser.role === 'admin';
            
            // 司机相关按钮
            const addVehicleBtn = document.getElementById('addVehicleBtn');
            if (addVehicleBtn) addVehicleBtn.classList.toggle('d-none', !isDriver);
            
            const createTripBtn = document.getElementById('createTripBtn');
            if (createTripBtn) createTripBtn.classList.toggle('d-none', !isDriver);
            
            const createTripBtnMain = document.getElementById('createTripBtnMain');
            if (createTripBtnMain) createTripBtnMain.classList.toggle('d-none', !isDriver);
            

            
            // 学生相关按钮
            const myApplicationsBtn = document.getElementById('myApplicationsBtn');
            if (myApplicationsBtn) myApplicationsBtn.classList.toggle('d-none', isDriver || isAdmin);
            
            // 根据角色显示不同的界面区域
            const studentTripsSection = document.getElementById('studentTripsSection');
            const driverTripsSection = document.getElementById('driverTripsSection');
            const myApplicationsSection = document.getElementById('myApplicationsSection');
            
            const adminDashboardSection = document.getElementById('adminDashboardSection');
            const adminUsersSection = document.getElementById('adminUsersSection');
            const adminVehiclesSection = document.getElementById('adminVehiclesSection');
            const adminTripsSection = document.getElementById('adminTripsSection');
            
            // 默认隐藏所有界面区域
            if (studentTripsSection) studentTripsSection.classList.add('d-none');
            if (driverTripsSection) driverTripsSection.classList.add('d-none');
            if (myApplicationsSection) myApplicationsSection.classList.add('d-none');
            if (adminDashboardSection) adminDashboardSection.classList.add('d-none');
            if (adminUsersSection) adminUsersSection.classList.add('d-none');
            if (adminVehiclesSection) adminVehiclesSection.classList.add('d-none');
            if (adminTripsSection) adminTripsSection.classList.add('d-none');
            
            // 根据角色显示相应的界面区域
            if (isAdmin) {
                // 管理员显示仪表盘
                if (adminDashboardSection) adminDashboardSection.classList.remove('d-none');
                this.adminShowDashboard();
            } else if (isDriver) {
                // 司机显示司机行程
                if (driverTripsSection) driverTripsSection.classList.remove('d-none');
                this.loadDriverTrips();
            } else {
                // 学生显示公共行程
                if (studentTripsSection) studentTripsSection.classList.remove('d-none');
                this.loadTrips();
            }
        } else {
            // 如果未登录，显示公共行程列表并隐藏所有管理员相关元素
            const studentTripsSection = document.getElementById('studentTripsSection');
            const driverTripsSection = document.getElementById('driverTripsSection');
            const myApplicationsSection = document.getElementById('myApplicationsSection');
            const adminDashboardSection = document.getElementById('adminDashboardSection');
            const adminUsersSection = document.getElementById('adminUsersSection');
            const adminVehiclesSection = document.getElementById('adminVehiclesSection');
            const adminTripsSection = document.getElementById('adminTripsSection');
            
            if (studentTripsSection) studentTripsSection.classList.remove('d-none');
            if (driverTripsSection) driverTripsSection.classList.add('d-none');
            if (myApplicationsSection) myApplicationsSection.classList.add('d-none');
            // 明确隐藏所有管理员区域
            if (adminDashboardSection) adminDashboardSection.classList.add('d-none');
            if (adminUsersSection) adminUsersSection.classList.add('d-none');
            if (adminVehiclesSection) adminVehiclesSection.classList.add('d-none');
            if (adminTripsSection) adminTripsSection.classList.add('d-none');
            
            this.loadTrips();
        }
    }

    // 检查是否已认证
    isAuthenticated() {
        return !!this.token;
    }

    // API请求封装
    async apiRequest(url, method = 'GET', data = null) {
        // 确保URL以/api/开头
        let fullUrl = url;
        if (!fullUrl.startsWith('/api/')) {
            fullUrl = `/api${fullUrl}`;
        }
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            },
            // 允许跨域请求
            credentials: 'include'
        };

        // 添加认证token
        console.log('当前token:', this.token);
        if (this.token) {
            options.headers['Authorization'] = `Bearer ${this.token}`;
            console.log('添加认证头:', options.headers['Authorization']);
        } else {
            console.warn('没有认证token，请求可能失败');
        }

        // 添加请求体
        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }

        try {
            console.log('发送API请求:', { url: fullUrl, method, headers: options.headers, data });
            
            // 添加超时处理
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('请求超时，请检查网络连接')), 10000);
            });
            
            const response = await Promise.race([fetch(fullUrl, options), timeoutPromise]);
            
            console.log('API响应状态:', response.status, '响应头:', response.headers);
            
            // 记录完整的响应内容
            const responseText = await response.text();
            console.log('API响应原始内容:', responseText);
            
            if (!response.ok) {
                let errorData = {};
                try {
                    errorData = JSON.parse(responseText);
                } catch (e) {
                    errorData = { message: responseText };
                }
                // 根据状态码提供更详细的错误信息
                let errorMessage = errorData.message || '请求失败';
                if (response.status === 401) {
                    errorMessage = errorData.message || '登录已过期，请重新登录';
                } else if (response.status === 403) {
                    errorMessage = errorData.message || '您没有权限执行此操作';
                } else if (response.status === 404) {
                    errorMessage = errorData.message || '请求的资源不存在';
                } else if (response.status === 500) {
                    errorMessage = errorData.message || '服务器错误，请稍后重试';
                }
                throw new Error(errorMessage);
            }

            // 处理空响应
            if (response.status === 204) {
                return null;
            }

            const result = JSON.parse(responseText);
            console.log('API响应数据:', result);
            return result;
        } catch (error) {
            console.error('API请求错误:', error);
            // 网络错误处理
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                throw new Error('网络连接失败，请检查您的网络设置');
            }
            throw error;
        }
    }

    // 显示消息提示
    showMessage(message, type = 'success') {
        // 创建消息元素
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type} alert-dismissible fade show fixed-top w-50 mx-auto mt-3`;
        messageDiv.style.zIndex = '1055';
        messageDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // 添加到页面
        document.body.appendChild(messageDiv);

        // 自动关闭
        setTimeout(() => {
            const bootstrapAlert = bootstrap.Alert.getInstance(messageDiv);
            if (bootstrapAlert) {
                bootstrapAlert.close();
            } else {
                messageDiv.remove();
            }
        }, 3000);
    }
    
    // 管理员仪表盘
    async adminShowDashboard() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        try {
            // 隐藏其他管理员区域，显示仪表盘
            this.hideAllAdminSections();
            const dashboardSection = document.getElementById('adminDashboardSection');
            if (dashboardSection) dashboardSection.classList.remove('d-none');
            
            // 加载统计数据
            const statsResponse = await this.apiRequest('/api/admin/stats', 'GET');
            
            // 更新统计卡片
            const totalUsersCount = document.getElementById('totalUsersCount');
            const totalVehiclesCount = document.getElementById('totalVehiclesCount');
            const totalTripsCount = document.getElementById('totalTripsCount');
            const todayNewUsersCount = document.getElementById('todayNewUsersCount');
            
            if (totalUsersCount) totalUsersCount.textContent = statsResponse.totalUsers;
            if (totalVehiclesCount) totalVehiclesCount.textContent = statsResponse.totalVehicles;
            if (totalTripsCount) totalTripsCount.textContent = statsResponse.totalTrips;
            if (todayNewUsersCount) todayNewUsersCount.textContent = statsResponse.todayNewUsers;
            
        } catch (error) {
            this.showMessage('加载仪表盘数据失败', 'error');
        }
    }
    
    // 加载用户列表
    async adminLoadUsers() {
        try {
            // 隐藏其他管理员区域，显示用户管理
            this.hideAllAdminSections();
            const usersSection = document.getElementById('adminUsersSection');
            if (usersSection) usersSection.classList.remove('d-none');
            
            // 加载用户数据
            const usersResponse = await this.apiRequest('/api/admin/users', 'GET');
            this.renderAdminUsers(usersResponse);
        } catch (error) {
            this.showMessage('加载用户列表失败', 'error');
        }
    }
    
    // 渲染管理员用户列表
    renderAdminUsers(users) {
        const usersTableBody = document.getElementById('adminUsersTable');
        if (!usersTableBody) return;
        
        if (users.length === 0) {
            usersTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">暂无用户数据</td></tr>';
            return;
        }
        
        const usersHtml = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.role === 'student' ? (user.studentId || '-') : (user.phone || '-')}</td>
                <td>${user.role}</td>
                <td>${new Date(user.createdAt || Date.now()).toLocaleString('zh-CN')}</td>
                <td>
                    <button class="btn btn-sm btn-primary me-1" onclick="app.adminEditUser(${JSON.stringify(user).replace(/"/g, '&quot;')})">编辑</button>
                    <button class="btn btn-sm btn-danger" onclick="app.adminDeleteUser(${user.id})">删除</button>
                </td>
            </tr>
        `).join('');
        
        usersTableBody.innerHTML = usersHtml;
    }
    
    // 加载车辆列表
    async adminLoadVehicles() {
        try {
            // 隐藏其他管理员区域，显示车辆管理
            this.hideAllAdminSections();
            const vehiclesSection = document.getElementById('adminVehiclesSection');
            if (vehiclesSection) vehiclesSection.classList.remove('d-none');
            
            // 加载车辆数据
            const vehiclesResponse = await this.apiRequest('/api/admin/vehicles', 'GET');
            this.renderAdminVehicles(vehiclesResponse);
        } catch (error) {
            this.showMessage('加载车辆列表失败', 'error');
        }
    }
    
    // 渲染管理员车辆列表
    renderAdminVehicles(vehicles) {
        const vehiclesTableBody = document.getElementById('adminVehiclesTable');
        if (!vehiclesTableBody) return;
        
        if (vehicles.length === 0) {
            vehiclesTableBody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">暂无车辆数据</td></tr>';
            return;
        }
        
        const vehiclesHtml = vehicles.map(vehicle => `
            <tr>
                <td>${vehicle.id}</td>
                <td>${vehicle.plateNumber}</td>
                <td>${vehicle.brand}</td>
                <td>${vehicle.model}</td>
                <td>${vehicle.color}</td>
                <td>${vehicle.seats}</td>
                <td>${vehicle.driverName || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-primary me-1" onclick="app.adminEditVehicle(${JSON.stringify(vehicle).replace(/"/g, '&quot;')})">编辑</button>
                    <button class="btn btn-sm btn-danger" onclick="app.adminDeleteVehicle(${vehicle.id})">删除</button>
                </td>
            </tr>
        `).join('');
        
        vehiclesTableBody.innerHTML = vehiclesHtml;
    }
    
    // 加载行程列表
    async adminLoadTrips() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        
        try {
            // 隐藏其他管理员区域，显示行程管理
            this.hideAllAdminSections();
            const tripsSection = document.getElementById('adminTripsSection');
            if (tripsSection) tripsSection.classList.remove('d-none');
            
            // 加载行程数据
            const tripsResponse = await this.apiRequest('/api/admin/trips', 'GET');
            this.renderAdminTrips(tripsResponse);
        } catch (error) {
            this.showMessage('加载行程列表失败', 'error');
        }
    }
    
    // 渲染管理员行程列表
    renderAdminTrips(trips) {
        const tripsTableBody = document.getElementById('adminTripsTable');
        if (!tripsTableBody) return;
        
        if (trips.length === 0) {
            tripsTableBody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">暂无行程数据</td></tr>';
            return;
        }
        
        const tripsHtml = trips.map(trip => {
            const date = new Date(trip.departureTime);
            const formattedDate = date.toLocaleString('zh-CN');
            return `
                <tr>
                    <td>${trip.id}</td>
                    <td>${trip.departureLocation} → ${trip.arrivalLocation}</td>
                    <td>${formattedDate}</td>
                    <td>${trip.pricePerSeat}</td>
                    <td>${trip.availableSeats}</td>
                    <td>${trip.driver?.name || '未知'}</td>
                    <td>${trip.vehicle?.brand || '未知'} ${trip.vehicle?.model || '车辆'}</td>
                    <td>
                        <button class="btn btn-sm btn-warning me-1" onclick="app.adminEditTrip(${JSON.stringify(trip).replace(/"/g, '&quot;')})">编辑</button>
                        <button class="btn btn-sm btn-danger" onclick="app.adminDeleteTrip(${trip.id})">删除</button>
                    </td>
                </tr>
            `;
        }).join('');
        
        tripsTableBody.innerHTML = tripsHtml;
    }
    
    // 隐藏所有管理员区域
    hideAllAdminSections() {
        const adminSections = [
            'adminDashboardSection',
            'adminUsersSection',
            'adminVehiclesSection',
            'adminTripsSection'
        ];
        
        adminSections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) section.classList.add('d-none');
        });
    }
    
    // 显示用户管理页面
    adminShowUsers() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        this.hideAllAdminSections();
        const usersSection = document.getElementById('adminUsersSection');
        if (usersSection) usersSection.classList.remove('d-none');
        this.adminLoadUsers();
    }
    
    // 显示车辆管理页面
    adminShowVehicles() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        this.hideAllAdminSections();
        const vehiclesSection = document.getElementById('adminVehiclesSection');
        if (vehiclesSection) vehiclesSection.classList.remove('d-none');
        this.adminLoadVehicles();
    }
    
    // 显示行程管理页面
    adminShowTrips() {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        
        this.hideAllAdminSections();
        const tripsSection = document.getElementById('adminTripsSection');
        if (tripsSection) tripsSection.classList.remove('d-none');
        this.adminLoadTrips();
    }
    
    // 添加用户
    adminAddUser() {
        // 打开添加用户模态框
        const addUserModal = new bootstrap.Modal(document.getElementById('addUserModal'));
        addUserModal.show();
        // 重置表单
        document.getElementById('addUserForm').reset();
    }
    
    // 编辑用户
    adminEditUser(user) {
        // 打开编辑用户模态框
        const editUserModal = new bootstrap.Modal(document.getElementById('editUserModal'));
        editUserModal.show();
        
        // 填充用户数据到表单
        document.getElementById('editUserId').value = user.id;
        document.getElementById('editUserName').value = user.name;
        document.getElementById('editUserRole').value = user.role;
        document.getElementById('editUserStudentId').value = user.studentId || '';
        document.getElementById('editUserPhone').value = user.phone || '';
        
        // 根据用户角色切换显示字段
        this.toggleEditUserFields({ target: document.getElementById('editUserRole') });
    }
    
    // 处理添加用户表单提交
    async handleAddUser(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const userData = {
            name: formData.get('name'),
            role: formData.get('role'),
            studentId: formData.get('studentId') || null,
            phone: formData.get('phone') || null,
            password: formData.get('password')
        };
        
        try {
            await this.apiRequest('/api/admin/users', 'POST', userData);
            this.showMessage('用户添加成功', 'success');
            
            // 关闭模态框
            const addUserModal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
            addUserModal.hide();
            
            // 重新加载用户列表
            this.adminLoadUsers();
        } catch (error) {
            this.showMessage('添加用户失败', 'error');
        }
    }
    
    // 处理编辑用户表单提交
    async handleEditUser(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const userId = formData.get('id');
        const role = formData.get('role');
        
        const userData = {
            name: formData.get('name'),
            role: role,
            phone: formData.get('phone') || null
        };
        
        // 只有当角色是学生时才添加学号字段
        if (role === 'student') {
            userData.studentId = formData.get('studentId') || null;
        }
        
        try {
            await this.apiRequest(`/api/admin/users/${userId}`, 'PUT', userData);
            this.showMessage('用户编辑成功', 'success');
            
            // 关闭模态框
            const editUserModal = bootstrap.Modal.getInstance(document.getElementById('editUserModal'));
            editUserModal.hide();
            
            // 重新加载用户列表
            this.adminLoadUsers();
        } catch (error) {
            this.showMessage('编辑用户失败', 'error');
        }
    }
    
    // 处理编辑车辆表单提交
    async handleEditVehicle(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const vehicleId = formData.get('id');
        const vehicleData = {
            plateNumber: formData.get('plateNumber'),
            brand: formData.get('brand'),
            model: formData.get('model'),
            color: formData.get('color'),
            seats: formData.get('seats'),
            year: formData.get('year') || null,
            description: formData.get('description') || null
        };
        
        try {
            await this.apiRequest(`/api/admin/vehicles/${vehicleId}`, 'PUT', vehicleData);
            this.showMessage('车辆编辑成功', 'success');
            
            // 关闭模态框
            const editVehicleModal = bootstrap.Modal.getInstance(document.getElementById('editVehicleModal'));
            editVehicleModal.hide();
            
            // 重新加载车辆列表
            this.adminLoadVehicles();
        } catch (error) {
            this.showMessage('编辑车辆失败', 'error');
        }
    }
    
    // 处理编辑行程表单提交
    async handleEditTrip(e) {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const tripId = formData.get('id');
        const tripData = {
            departureLocation: formData.get('departureLocation'),
            arrivalLocation: formData.get('arrivalLocation'),
            departureTime: formData.get('departureTime'),
            pricePerSeat: formData.get('pricePerSeat'),
            availableSeats: formData.get('availableSeats'),
            tripStatus: formData.get('tripStatus'),
            description: formData.get('description') || null
        };
        
        try {
            await this.apiRequest(`/api/admin/trips/${tripId}`, 'PUT', tripData);
            this.showMessage('行程编辑成功', 'success');
            
            // 关闭模态框
            const editTripModal = bootstrap.Modal.getInstance(document.getElementById('editTripModal'));
            editTripModal.hide();
            
            // 重新加载行程列表
            this.adminLoadTrips();
        } catch (error) {
            this.showMessage('编辑行程失败', 'error');
        }
    }
    
    // 删除用户
    async adminDeleteUser(userId) {
        if (confirm('确定要删除这个用户吗？')) {
            try {
                await this.apiRequest(`/api/admin/users/${userId}`, 'DELETE');
                this.showMessage('用户删除成功', 'success');
                this.adminLoadUsers(); // 重新加载用户列表
            } catch (error) {
                this.showMessage('删除用户失败', 'error');
            }
        }
    }
    
    // 添加车辆
    async adminAddVehicle() {
        // 打开添加车辆模态框
        const addVehicleModal = new bootstrap.Modal(document.getElementById('addVehicleModal'));
        addVehicleModal.show();
        
        // 显示司机选择框
        const driverSelectGroup = document.querySelector('#vehicleDriver').closest('.mb-3');
        const driverSelect = document.getElementById('vehicleDriver');
        if (driverSelectGroup) {
            driverSelectGroup.classList.remove('d-none');
        }
        // 恢复required属性，确保管理员添加车辆时必须选择司机
        if (driverSelect) {
            driverSelect.required = true;
        }
        
        // 加载司机列表
        await this.loadDriversForAdminVehicleAdd();
    }
    
    // 加载司机列表用于管理员添加车辆
    async loadDriversForAdminVehicleAdd() {
        try {
            const response = await this.apiRequest('/api/admin/users?role=driver', 'GET');
            const drivers = response;
            
            const driverSelect = document.getElementById('vehicleDriver');
            if (driverSelect) {
                // 清空现有选项
                driverSelect.innerHTML = '';
                
                // 添加司机选项
                drivers.forEach(driver => {
                    const option = document.createElement('option');
                    option.value = driver.id;
                    option.textContent = `${driver.name} (${driver.phone})`;
                    driverSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('加载司机列表失败:', error);
            this.showMessage('加载司机列表失败，请稍后重试', 'error');
        }
    }
    
    // 处理管理员添加车辆表单提交
    async handleAdminAddVehicle(e) {
        e.preventDefault();
        
        try {
            // 获取表单数据
            const formData = {
                plateNumber: document.getElementById('vehiclePlateNumber').value,
                brand: document.getElementById('vehicleBrand').value,
                model: document.getElementById('vehicleModel').value,
                color: document.getElementById('vehicleColor').value,
                seats: parseInt(document.getElementById('vehicleSeats').value),
                year: document.getElementById('vehicleYear').value,
                description: document.getElementById('vehicleDescription').value,
                userId: parseInt(document.getElementById('vehicleDriver').value)
            };
            
            // 提交表单
            await this.apiRequest('/api/admin/vehicles', 'POST', formData);
            
            // 显示成功消息
            this.showMessage('车辆添加成功', 'success');
            
            // 关闭模态框
            const addVehicleModal = bootstrap.Modal.getInstance(document.getElementById('addVehicleModal'));
            if (addVehicleModal) {
                addVehicleModal.hide();
            }
            
            // 重置表单
            e.target.reset();
            
            // 重新加载车辆列表
            this.adminLoadVehicles();
        } catch (error) {
            console.error('添加车辆失败:', error);
            this.showMessage(error.message || '添加车辆失败，请稍后重试', 'error');
        }
    }
    
    // 编辑车辆
    adminEditVehicle(vehicle) {
        // 打开编辑车辆模态框
        const editVehicleModal = new bootstrap.Modal(document.getElementById('editVehicleModal'));
        editVehicleModal.show();
        
        // 填充车辆数据到表单
        document.getElementById('editVehicleId').value = vehicle.id;
        document.getElementById('editVehiclePlateNumber').value = vehicle.plateNumber;
        document.getElementById('editVehicleBrand').value = vehicle.brand;
        document.getElementById('editVehicleModel').value = vehicle.model;
        document.getElementById('editVehicleColor').value = vehicle.color;
        document.getElementById('editVehicleSeats').value = vehicle.seats;
        document.getElementById('editVehicleYear').value = vehicle.year || '';
        document.getElementById('editVehicleDescription').value = vehicle.description || '';
    }
    
    // 编辑行程
    adminEditTrip(trip) {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        
        // 打开编辑行程模态框
        const editTripModal = new bootstrap.Modal(document.getElementById('editTripModal'));
        editTripModal.show();
        
        // 填充行程数据到表单
        document.getElementById('editTripId').value = trip.id;
        document.getElementById('editTripDepartureLocation').value = trip.departureLocation;
        document.getElementById('editTripArrivalLocation').value = trip.arrivalLocation;
        
        // 处理日期时间格式
        const departureTime = new Date(trip.departureTime);
        const formattedDepartureTime = departureTime.toISOString().slice(0, 16); // 格式化为YYYY-MM-DDThh:mm
        document.getElementById('editTripDepartureTime').value = formattedDepartureTime;
        
        document.getElementById('editTripPricePerSeat').value = trip.pricePerSeat;
        document.getElementById('editTripAvailableSeats').value = trip.availableSeats;
        document.getElementById('editTripStatus').value = trip.tripStatus || 'pending';
        document.getElementById('editTripDescription').value = trip.description || '';
    }
    
    // 删除车辆
    async adminDeleteVehicle(vehicleId) {
        if (confirm('确定要删除这个车辆吗？')) {
            try {
                await this.apiRequest(`/api/admin/vehicles/${vehicleId}`, 'DELETE');
                this.showMessage('车辆删除成功', 'success');
                this.adminLoadVehicles(); // 重新加载车辆列表
            } catch (error) {
                this.showMessage('删除车辆失败', 'error');
            }
        }
    }
    

    
    // 删除行程
    async adminDeleteTrip(tripId) {
        if (!this.isAuthenticated()) {
            this.showMessage('请先登录', 'warning');
            return;
        }
        
        if (confirm('确定要删除这个行程吗？')) {
            try {
                await this.apiRequest(`/api/admin/trips/${tripId}`, 'DELETE');
                this.showMessage('行程删除成功', 'success');
                this.adminLoadTrips(); // 重新加载行程列表
            } catch (error) {
                this.showMessage('删除行程失败', 'error');
            }
        }
    }
}

// 初始化应用
const app = new CarpoolApp();