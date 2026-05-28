const API = '/api/todos';

const { createApp } = Vue;

createApp({
    data() {
        return {
            view: 'list',
            todos: [],
            form: { info: '' },
            editingId: null,
        };
    },
    mounted() {
        this.loadTodos();
    },
    methods: {
        async loadTodos() {
            const res = await fetch(API);
            this.todos = await res.json();
        },

        async toggleDone(id) {
            await fetch(`${API}/${id}/done`, { method: 'PUT' });
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
            await fetch(API, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ info }),
            });
            this.form.info = '';
            this.view = 'list';
            this.loadTodos();
        },

        async saveEdit() {
            const info = this.form.info.trim();
            if (!info) return;
            await fetch(`${API}/${this.editingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ info }),
            });
            this.form.info = '';
            this.editingId = null;
            this.view = 'list';
            this.loadTodos();
        },

        async deleteTodo(id) {
            if (!confirm('确定要删除吗？')) return;
            await fetch(`${API}/${id}`, { method: 'DELETE' });
            this.loadTodos();
        },
    },
}).mount('#app');
