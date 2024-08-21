from celery import shared_task
from .models import Automation, Job, JobLog
import importlib


@shared_task
def run_automation_job(automation_id):
    automation = Automation.objects.get(id=automation_id)
    job = automation.job

    try:
        # Update job status
        job.status = "STARTED"
        job.save()

        # Log job start
        JobLog.objects.create(job=job, log={"message": "Job started"})

        # Import the selected script
        script_module = importlib.import_module(
            f"scripts.{automation.automation_script}"
        )

        # Run the script for each selected hostname
        results = []
        for hostname in automation.hostnames.all():
            result = script_module.run(hostname, dry_run=automation.dry_run)
            results.append(result)
            JobLog.objects.create(
                job=job, log={"hostname": hostname.hostname, "result": result}
            )

        # Update job with final results
        job.status = "COMPLETED"
        job.result = {"results": results}
        job.save()

        JobLog.objects.create(job=job, log={"message": "Job completed successfully"})

    except Exception as e:
        job.status = "FAILED"
        job.result = {"error": str(e)}
        job.save()
        JobLog.objects.create(job=job, log={"message": f"Job failed: {str(e)}"})

    return job.job_id
