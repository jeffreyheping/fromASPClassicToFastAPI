const API = '/api/todos';
const AUTH_API = '/api/auth';

const { createApp } = Vue;

createApp({
    data() {
        return {
            view: 'list',
            todos: [],
            form: { info: '' },
            editingId: null,
            // 认证相关
            isLoggedIn: false,
            currentUser: null,
            showLogin: false,
            showRegister: false,
            authForm: { username: '', password: '' },
            authError: '',
        };
    },
    mounted() {
        // 检查本地存储的token
        const token = localStorage.getItem('token');
        if (token) {
            this.validateToken(token);
        }
    },
    methods: {
        // 认证方法
        async doLogin() {
            this.authError = '';
            try {
                const res = await fetch(`${AUTH_API}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.authForm),
                });
                const data = await res.json();
                if (!res.ok) {
                    this.authError = data.detail || '登录失败';
                    return;
                }
                localStorage.setItem('token', data.access_token);
                this.currentUser = data.user;
                this.isLoggedIn = true;
                this.showLogin = false;
                this.authForm = { username: '', password: '' };
                this.loadTodos();
            } catch (e) {
                this.authError = '网络错误';
            }
        },

        async doRegister() {
            this.authError = '';
            try {
                const res = await fetch(`${AUTH_API}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.authForm),
                });
                const data = await res.json();
                if (!res.ok) {
                    this.authError = data.detail || '注册失败';
                    return;
                }
                // 注册成功后自动登录
                await this.doLogin();
                this.showRegister = false;
            } catch (e) {
                this.authError = '网络错误';
            }
        },

        doLogout() {
            localStorage.removeItem('token');
            this.isLoggedIn = false;
            this.currentUser = null;
            this.todos = [];
        },

        async validateToken(token) {
            try {
                const res = await fetch(`${AUTH_API}/me?token=${token}`);
                if (res.ok) {
                    this.currentUser = await res.json();
                    this.isLoggedIn = true;
                    this.loadTodos();
                } else {
                    localStorage.removeItem('token');
                }
            } catch (e) {
                localStorage.removeItem('token');
            }
        },

        // Todo 方法
        async loadTodos() {
            const token = localStorage.getItem('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
            const res = await fetch(API, { headers });
            this.todos = await res.json();
        },

        async toggleDone(id) {
            const token = localStorage.getItem('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
            await fetch(`${API}/${id}/done`, { method: 'PUT', headers });
            this.loadTodos();
        },

        editTodo(todo) {
            this.editingId = todo.id;
            this.form.info = todo.info;
            this.view = 'edit';
        },

        async saveAdd() {
            const info = this.form.info.trim();
            if (!info) return;
            const token = localStorage.getItem('token');
            const headers = {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            };
            await fetch(API, {
                method: 'POST',
                headers,
                body: JSON.stringify({ info }),
            });
            this.form.info = '';
            this.view = 'list';
            this.loadTodos();
        },

        async saveEdit() {
            const info = this.form.info.trim();
            if (!info) return;
            const token = localStorage.getItem('token');
            const headers = {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            };
            await fetch(`${API}/${this.editingId}`, {
                method: 'PUT',
                headers,
                body: JSON.stringify({ info }),
            });
            this.form.info = '';
            this.editingId = null;
            this.view = 'list';
            this.loadTodos();
        },

        async deleteTodo(id) {
            if (!confirm('确定要删除吗？')) return;
            const token = localStorage.getItem('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
            await fetch(`${API}/${id}`, { method: 'DELETE', headers });
            this.loadTodos();
        },
    },
}).mount('#app');
