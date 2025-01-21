import sys
import os
import django
import logging
import traceback

from celery import shared_task
from django.contrib.auth import get_user_model
from saute.models import Message, Conversation, Jobs

# third party library imports
from environs import Env

# import our python scripts
from saute.scripts import (
    run_admin_report,
    run_assurance,
    run_change_analysis,
    run_create_script,
    run_export_rules_to_csv,
    run_get_system_info,
    run_pan_to_prisma,
    run_send_message,
    run_upload_cert_chain,
)

# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
env = Env()
env.read_env()

sendgrid_api_key = env(
    "SENDGRID_API_KEY",
    "go to https://docs.sendgrid.com/ui/account-and-settings/api-keys",
)

sys.path.append("/code/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()
User = get_user_model()


# ----------------------------------------------------------------------------
# Export Security Rules to CSV file
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_export_rules_to_csv(self, pan_url, api_key, author_id):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new Jobs entry
    job = Jobs.objects.create(
        job_type="export_rules_to_csv",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )

    try:
        output_filepath = run_export_rules_to_csv(pan_url, api_key)
        job.result = f"Job ID: {job.pk}\nExported to {output_filepath}"
    except Exception as e:
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Get Panorama System Info
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_get_system_info(self, pan_url, api_key, author_id):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new Jobs entry
    job = Jobs.objects.create(
        job_type="get_system_info",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )

    try:
        system_info = run_get_system_info(pan_url, api_key)
        job.json_data = system_info
    except Exception as e:
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Retrieve and upload Certificate Chain
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_upload_cert_chain(self, api_key, author_id, pan_url, url):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new Jobs entry
    job = Jobs.objects.create(
        author=author,
        job_type="upload_cert_chain",
        json_data=None,
        task_id=self.request.id,
    )

    try:
        json_object = run_upload_cert_chain(pan_url, api_key, url)
        job.json_data = json_object
    except Exception as e:
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Sync Panorama to Prisma
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_pan_to_prisma(
    self,
    pan_url,
    api_key,
    client_id,
    client_secret,
    tsg_id,
    token_url,
    config_objects,
    author_id,
):
    logging.debug("Hey, we made it to the task!")
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)
    logging.debug(f"Here is the author {author}")

    # Create a new Jobs entry
    job = Jobs.objects.create(
        job_type="pan_to_prisma",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    logging.debug("About to run the script")
    logging.debug(
        f"pan_url: {pan_url}, api_key: {api_key}, client_id: {client_id}, client_secret: {client_secret}, tsg_id: {tsg_id}, token_url: {token_url}, config_objects: {config_objects}"
    )

    try:
        logging.debug("About to run the script")
        json_report = run_pan_to_prisma(
            pan_url,
            api_key,
            client_id,
            client_secret,
            tsg_id,
            token_url,
            config_objects,
        )
        if json_report is None:
            logging.error("json_report is None")
        logging.debug(json_report)
        job.json_data = json_report
    except Exception as e:
        job.result = f"Job ID: {job.pk}\nError: {e}"
        logging.error(f"Exception Type: {type(e).__name__}")
        logging.error(f"Traceback: {traceback.format_exc()}")

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Report of Administrators
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_admin_report(
    self,
    pan_url,
    api_key,
    to_emails,
    author_id,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new Jobs entry
    job = Jobs.objects.create(
        job_type="admin_report",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.info(f"Job ID: {job.pk}")

    try:
        json_report = run_admin_report(pan_url, api_key, to_emails, sendgrid_api_key)
        logging.info(json_report)
        job.json_data = json_report
        logging.info(job)
    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Assurance: Check for ARP entry
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_assurance_arp(
    self,
    hostname,
    api_key,
    operation_type,
    action,
    config,
    author_id,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new entry in our Jobs database table
    job = Jobs.objects.create(
        job_type="assurance_arp_entry",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    # Execute the assurance check
    try:
        json_report = run_assurance(
            hostname,
            api_key,
            operation_type,
            action,
            config,
        )

        # logging.debug(json_report)
        job.json_data = json_report
        logging.debug(job)

    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Assurance: Readiness Check
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_assurance_readiness(
    self,
    hostname,
    api_key,
    operation_type,
    action,
    config,
    author_id,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new entry in our Jobs database table
    job = Jobs.objects.create(
        job_type="assurance_readiness",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    # Execute the assurance check
    try:
        json_report = run_assurance(
            hostname,
            api_key,
            operation_type,
            action,
            config,
        )

        # logging.debug(json_report)
        job.json_data = json_report
        logging.debug(job)

    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# Assurance: Snapshot
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_assurance_snapshot(
    self,
    hostname,
    api_key,
    operation_type,
    action,
    config,
    author_id,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new entry in our Jobs database table
    job = Jobs.objects.create(
        job_type="assurance_snapshot",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    # Execute the assurance check
    try:
        json_report = run_assurance(
            hostname,
            api_key,
            operation_type,
            action,
            config,
        )

        # logging.debug(json_report)
        job.json_data = json_report
        logging.debug(job)

    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# AI: Change Analysis with ChatGPT
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_change_analysis(
    self,
    after_snapshot_id,
    before_snapshot_id,
    message,
    expertise_level,
    author_id,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new entry in our Jobs database table
    job = Jobs.objects.create(
        job_type="change_analysis",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    # Retrieve the JSON data for the before_snapshot and after_snapshot
    before_snapshot_contents = (
        Jobs.objects.filter(task_id=before_snapshot_id).values("json_data").first()
    )
    after_snapshot_contents = (
        Jobs.objects.filter(task_id=after_snapshot_id).values("json_data").first()
    )

    if before_snapshot_contents:
        before_snapshot_contents = before_snapshot_contents["json_data"]
        if not isinstance(before_snapshot_contents, dict):
            raise ValueError(
                f"Unexpected data format for 'before_snapshot_contents', got {type(before_snapshot_contents)}"
            )

    if after_snapshot_contents:
        after_snapshot_contents = after_snapshot_contents["json_data"]
        if not isinstance(after_snapshot_contents, dict):
            raise ValueError(
                f"Unexpected data format for 'after_snapshot_contents', got {type(after_snapshot_contents)}"
            )

    logging.debug(f"before_snapshot_contents: {before_snapshot_contents}")
    logging.debug(f"after_snapshot_contents: {after_snapshot_contents}")

    # Execute the assurance check
    try:
        result = run_change_analysis(
            after_snapshot_contents,
            before_snapshot_contents,
            message,
            expertise_level,
        )

        # logging.debug(result)
        job.json_data = result["choices"][0]["message"]["content"]
        logging.debug(job)

    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# AI: Create Script with ChatGPT
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_create_script(
    self,
    message,
    language,
    target,
    author_id,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new entry in our Jobs database table
    job = Jobs.objects.create(
        job_type="create_script",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    # Execute the creation of the script
    try:
        result = run_create_script(
            message,
            language,
            target,
        )

        # logging.debug(result)
        job.json_data = result["choices"][0]["message"]["content"]
        logging.debug(job)

    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()


# ----------------------------------------------------------------------------
# AI: Chat with ChatGPT
# ----------------------------------------------------------------------------
@shared_task(bind=True)
def execute_chat(
    self,
    author_id,
    conversation_id,
    llm,
    message,
    persona,
):
    # Retrieve the user object by id
    author = User.objects.get(id=author_id)

    # Create a new entry in our Jobs database table
    job = Jobs.objects.create(
        job_type="send_message",
        json_data=None,
        author=author,
        task_id=self.request.id,
    )
    logging.debug(f"Job ID: {job.pk}")

    # Execute the assurance check
    try:
        result = run_send_message(
            conversation_id,
            llm,
            message,
            persona,
        )

        # Store the result in the Message model
        convo = Conversation.objects.get(conversation_id=conversation_id)

        # Compute next message index
        next_index = convo.messages.count() + 1

        Message.objects.create(
            index=next_index,
            content=message,
            role="user",
            author=author,
            conversation=convo,
        )
        Message.objects.create(
            index=next_index + 1,
            content=result["choices"][0]["message"]["content"],
            role="bot",
            author=author,
            conversation=convo,
        )

        # logging.debug(result)
        job.json_data = result["choices"][0]["message"]["content"]
        logging.debug(job)

    except Exception as e:
        logging.error(e)
        job.result = f"Job ID: {job.pk}\nError: {e}"

    # Save the updated job information
    job.save()
