class JobsManager {
    constructor() {
        this.jobs = new Map();
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

        this.socket = new WebSocket('ws://' + window.location.host + '/ws/jobs/');

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
            this.reconnectAttempts = 0;
            this.processPendingSubscriptions();
        };

        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            console.log('Received message:', data);
            if (this.jobs.has(data.job_id)) {
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

    sendJobSubscription(jobId) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log('Subscribing to job:', jobId);
            this.socket.send(JSON.stringify({action: 'subscribe', job_id: jobId}));
        } else {
            console.log('WebSocket not ready, queueing subscription for job:', jobId);
            this.pendingSubscriptions.add(jobId);
        }
    }

    processPendingSubscriptions() {
        this.pendingSubscriptions.forEach(jobId => {
            this.sendJobSubscription(jobId);
        });
        this.pendingSubscriptions.clear();
    }

    addJob(jobId) {
        console.log(`Adding job: ${jobId}`);
        if (!this.jobs.has(jobId)) {
            const container = document.getElementById(`jobs_${jobId}`);
            if (container) {
                this.jobs.set(jobId, container);
                this.sendJobSubscription(jobId);
            } else {
                console.warn(`Job container not found for job ID: ${jobId}`);
            }
        }
    }

    updateUI(data) {
        const container = this.jobs.get(data.job_id);
        if (!container) return;

        const statusElement = container.querySelector('.jobs');
        const progressBar = container.querySelector('.progress-bar');
        const resultElement = container.querySelector('.job');

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

// Initialize the JobsManager when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.jobsManager = new JobsManager();
    document.querySelectorAll('[id^="jobs_"]').forEach(container => {
        const jobId = container.id.split('_')[1];
        window.jobsManager.addJob(jobId);
    });
});
