class TaskStatusManager {
    constructor() {
        this.tasks = new Map();
        this.socket = null;
        this.connect();
    }

    connect() {
        this.socket = new WebSocket('ws://' + window.location.host + '/ws/task_status/');

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
            this.tasks.forEach((task, taskId) => {
                this.sendTaskSubscription(taskId);
            });
        };

        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (this.tasks.has(data.task_id)) {
                this.updateUI(data);
            }
        };

        this.socket.onclose = () => {
            console.log('WebSocket connection closed');
            setTimeout(() => this.connect(), 5000);
        };
    }

    sendTaskSubscription(taskId) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({action: 'subscribe', task_id: taskId}));
        }
    }

    addTask(taskId) {
        if (!this.tasks.has(taskId)) {
            this.tasks.set(taskId, {
                container: document.querySelector(`#taskStatusContainer[data-task-id="${taskId}"]`)
            });
            this.sendTaskSubscription(taskId);
        }
    }

    removeTask(taskId) {
        this.tasks.delete(taskId);
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({action: 'unsubscribe', task_id: taskId}));
        }
    }

    updateUI(data) {
        const task = this.tasks.get(data.task_id);
        if (!task) return;

        const container = task.container;
        container.classList.remove('d-none');

        const taskIdElement = container.querySelector('#taskId');
        const statusElement = container.querySelector('#taskStatus');
        const progressBar = container.querySelector('#taskProgress');
        const resultElement = container.querySelector('#taskResult');

        taskIdElement.textContent = data.task_id;
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
                this.removeTask(data.task_id);
                break;
            case 'FAILURE':
                progress = 100;
                progressBar.classList.remove('bg-primary');
                progressBar.classList.add('bg-danger');
                this.removeTask(data.task_id);
                break;
        }

        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.textContent = `${progress}%`;

        if (data.result) {
            resultElement.textContent = JSON.stringify(data.result);
        }
    }
}

// Initialize the TaskStatusManager when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.taskStatusManager = new TaskStatusManager();
    document.querySelectorAll('#taskStatusContainer[data-task-id]').forEach(container => {
        const taskId = container.dataset.taskId;
        window.taskStatusManager.addTask(taskId);
    });
});
