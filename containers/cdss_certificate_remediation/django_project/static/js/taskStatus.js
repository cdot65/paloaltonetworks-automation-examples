class TaskStatusManager {
    constructor() {
        this.tasks = new Map();
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 5000;
        this.pendingSubscriptions = new Set();
        this.connect();
    }

    connect() {
        if (this.socket && (this.socket.readyState === WebSocket.CONNECTING || this.socket.readyState === WebSocket.OPEN)) {
            console.log('WebSocket already connecting or connected');
            return;
        }

        this.socket = new WebSocket('ws://' + window.location.host + '/ws/task_status/');

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
            this.reconnectAttempts = 0;
            this.processPendingSubscriptions();
        };

        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            console.log('Received message:', data);
            if (this.tasks.has(data.task_id)) {
                this.updateUI(data);
            }
        };

        this.socket.onclose = (e) => {
            console.log('WebSocket connection closed', e.reason);
            this.handleReconnect();
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        } else {
            console.error('Max reconnection attempts reached. Please refresh the page.');
        }
    }

    sendTaskSubscription(taskId) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log('Subscribing to task:', taskId);
            this.socket.send(JSON.stringify({action: 'subscribe', task_id: taskId}));
        } else {
            console.log('WebSocket not ready, queueing subscription for task:', taskId);
            this.pendingSubscriptions.add(taskId);
        }
    }

    processPendingSubscriptions() {
        this.pendingSubscriptions.forEach(taskId => {
            this.sendTaskSubscription(taskId);
        });
        this.pendingSubscriptions.clear();
    }

    addTask(taskId) {
        console.log(`Adding task: ${taskId}`);
        if (!this.tasks.has(taskId)) {
            const container = document.getElementById(`taskStatus_${taskId}`);
            if (container) {
                this.tasks.set(taskId, container);
                this.sendTaskSubscription(taskId);
            } else {
                console.warn(`Task container not found for task ID: ${taskId}`);
            }
        }
    }

    updateUI(data) {
        const container = this.tasks.get(data.task_id);
        if (!container) return;

        const statusElement = container.querySelector('.task-status');
        const progressBar = container.querySelector('.progress-bar');
        const resultElement = container.querySelector('.task-result');

        statusElement.textContent = data.status;

        let progress = 0;
        switch (data.status) {
            case 'STARTED':
                progress = 25;
                break;
            case 'PROGRESS':
                progress = 50;
                break;
            case 'SUCCESS':
                progress = 100;
                break;
            case 'FAILURE':
                progress = 100;
                progressBar.classList.remove('bg-primary');
                progressBar.classList.add('bg-danger');
                break;
        }

        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.textContent = `${progress}%`;

        if (data.result) {
            resultElement.textContent = JSON.stringify(data.result);
        }

        container.classList.remove('d-none');
    }
}

// Initialize the TaskStatusManager when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.taskStatusManager = new TaskStatusManager();
    document.querySelectorAll('[id^="taskStatus_"]').forEach(container => {
        const taskId = container.id.split('_')[1];
        window.taskStatusManager.addTask(taskId);
    });
});
