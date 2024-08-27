/**
 * JobsManager class
 *
 * This class manages WebSocket connections for job status updates.
 * It handles connection lifecycle, job subscriptions, and UI updates.
 * The browser loads this script through the template, and it initializes
 * when the DOM is fully loaded. It creates a WebSocket connection to the
 * server, subscribes to job updates, and manages the connection state,
 * including automatic reconnection attempts on disconnection.
 */
class JobsManager {
    /**
     * Initializes the JobsManager instance.
     * Sets up initial state and attempts to establish a WebSocket connection.
     */
    constructor() {
        this.jobs = new Map();
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 5000;
        this.pendingSubscriptions = new Set();
        this.connect();
    }

    /**
     * Establishes a WebSocket connection to the server.
     * Handles connection lifecycle events (open, message, close, error).
     */
    connect() {
        if (this.socket && (this.socket.readyState === WebSocket.CONNECTING || this.socket.readyState === WebSocket.OPEN)) {
            console.log('WebSocket already connecting or connected');
            return;
        }

        this.socket = new WebSocket('wss://' + window.location.host + '/ws/jobs/');

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

    /**
     * Handles reconnection attempts when the WebSocket connection is closed.
     * Implements an exponential backoff strategy for reconnection.
     */
    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        } else {
            console.error('Max reconnection attempts reached. Please refresh the page.');
        }
    }

    /**
     * Sends a job subscription request to the server.
     * If the WebSocket is not ready, it queues the subscription for later processing.
     * @param {string} jobId - The ID of the job to subscribe to.
     */
    sendJobSubscription(jobId) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log('Subscribing to job:', jobId);
            this.socket.send(JSON.stringify({action: 'subscribe', job_id: jobId}));
        } else {
            console.log('WebSocket not ready, queueing subscription for job:', jobId);
            this.pendingSubscriptions.add(jobId);
        }
    }

    /**
     * Processes any pending job subscriptions.
     * Called when the WebSocket connection is established.
     */
    processPendingSubscriptions() {
        this.pendingSubscriptions.forEach(jobId => {
            this.sendJobSubscription(jobId);
        });
        this.pendingSubscriptions.clear();
    }

    /**
     * Adds a new job to be managed by the JobsManager.
     * Subscribes to updates for the job if the corresponding DOM element exists.
     * @param {string} jobId - The ID of the job to add.
     */
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

    /**
     * Updates the UI based on received job status data.
     * @param {Object} data - The job status data received from the server.
     */
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

/**
 * Initializes the JobsManager when the DOM is fully loaded.
 * Adds all jobs found in the DOM to the JobsManager.
 */
document.addEventListener('DOMContentLoaded', () => {
    window.jobsManager = new JobsManager();
    document.querySelectorAll('[id^="jobs_"]').forEach(container => {
        const jobId = container.id.replace('jobs_', '');
        window.jobsManager.addJob(jobId);
    });
});
