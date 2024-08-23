# django_project/jobs/tasks.py
from celery import shared_task
from .models import Automation, Job, JobLog
from .utils import send_job_update
import importlib
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def run_automation_job(self, automation_id):
    """
    Execute an automation job as a Celery task.

    This task performs the following steps:
    1. Retrieves or creates a Job instance using the Celery task ID.
    2. Loads the associated Automation instance.
    3. Imports the specified automation script.
    4. Executes the script for each hostname in the Automation.
    5. Updates the Job status and results throughout the process.
    6. Logs each step of the job execution.
    7. Sends real-time updates via WebSocket.

    Args:
        self (Task): The Celery Task instance (automatically injected).
        automation_id (int): The ID of the Automation instance to run.

    Returns:
        str: The job_id (UUID) of the executed job.

    Raises:
        Automation.DoesNotExist: If the specified Automation instance doesn't exist.
        ImportError: If the specified automation script cannot be imported.
        Exception: For any other errors during job execution.
    """
    # Retrieve the Celery task ID (UUID)
    job_id = self.request.id
    logger.info(f"Starting automation job with ID: {job_id}")

    # Create or retrieve the Job instance
    job, created = Job.objects.get_or_create(
        job_id=job_id, defaults={"status": "PENDING", "task_name": "run_automation_job"}
    )
    if created:
        logger.info(f"Created new Job instance with ID: {job_id}")
    else:
        logger.info(f"Retrieved existing Job instance with ID: {job_id}")

    try:
        # Retrieve the associated Automation instance
        automation = Automation.objects.get(id=automation_id)
        logger.info(f"Retrieved Automation instance with ID: {automation_id}")

        # Link the Automation to the Job
        automation.job = job
        automation.save()
        logger.info(f"Linked Automation {automation_id} to Job {job_id}")

        # Log the job start
        JobLog.objects.create(job=job, message="Job started")
        logger.info(f"Job {job_id} started")

        # Send a real-time update via WebSocket
        send_job_update(job_id, "STARTED", None)
        logger.info(f"Sent 'STARTED' status update for Job {job_id}")

        # Import the selected automation script
        script_module = importlib.import_module(
            f"scripts.{automation.automation_script}"
        )
        logger.info(f"Imported automation script: {automation.automation_script}")

        # Execute the script for each selected hostname
        results = []
        for hostname in automation.hostnames.all():
            logger.info(f"Processing hostname: {hostname}")
            JobLog.objects.create(job=job, message=f"Processing hostname: {hostname}")

            # Run the script for the current hostname
            result = script_module.run(hostname, dry_run=automation.dry_run)
            results.append(result)
            logger.info(f"Script execution result for {hostname}: {result}")

            # Log the result for this hostname
            JobLog.objects.create(job=job, message=f"Result for {hostname}: {result}")

        # Update the Job status to COMPLETED
        job.status = "COMPLETED"
        job.result = {"results": results}
        job.save()
        logger.info(f"Job {job_id} completed successfully")

        # Log job completion
        JobLog.objects.create(job=job, message="Job completed successfully")

        # Send a real-time update via WebSocket
        send_job_update(job_id, "SUCCESS", job.result)
        logger.info(f"Sent 'SUCCESS' status update for Job {job_id}")

    except Automation.DoesNotExist:
        logger.error(f"Automation with ID {automation_id} not found")
        job.status = "FAILED"
        job.result = {"error": f"Automation with ID {automation_id} not found"}
        job.save()
        JobLog.objects.create(
            job=job, message=f"Job failed: Automation not found", level="ERROR"
        )
        send_job_update(job_id, "FAILURE", job.result)

    except ImportError as e:
        logger.error(f"Failed to import automation script: {str(e)}")
        job.status = "FAILED"
        job.result = {"error": f"Failed to import automation script: {str(e)}"}
        job.save()
        JobLog.objects.create(
            job=job, message=f"Job failed: Import error", level="ERROR"
        )
        send_job_update(job_id, "FAILURE", job.result)

    except Exception as e:
        logger.error(f"Job {job_id} failed with error: {str(e)}")
        job.status = "FAILED"
        job.result = {"error": str(e)}
        job.save()
        JobLog.objects.create(job=job, message=f"Job failed: {str(e)}", level="ERROR")
        send_job_update(job_id, "FAILURE", job.result)

    return job.job_id
