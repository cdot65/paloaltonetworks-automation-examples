# standard library imports
import logging
import argparse
from typing import Dict, Union

# OpenAI and PAN-OS imports
import openai
from environs import Env
from pydantic import BaseModel

# Local prompt file imports
from .prompts import chatgpt_prompts


# ----------------------------------------------------------------------------
# Define logging levels
# ----------------------------------------------------------------------------
LOGGING_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


# ----------------------------------------------------------------------------
# Define ChatGPT technical response depth, to revisit later
# ----------------------------------------------------------------------------
EXPERTISE_LEVEL = {
    "beginner": "beginner",
    "apprentice": "apprentice",
    "professional": "professional",
    "expert": "expert",
}


# ----------------------------------------------------------------------------
# Define models
# ----------------------------------------------------------------------------
class Args(BaseModel):
    after_snapshot_contents: Dict
    before_snapshot_contents: Dict
    message: str
    expertise_level: str
    log_level: str = "debug"


# ----------------------------------------------------------------------------
# Parse arguments
# ----------------------------------------------------------------------------
def parse_arguments() -> Args:
    """
    Parse command line arguments and returns a Namespace object with arguments as attributes.

    The --config argument should be a string that represents a Python dictionary.
    This function converts the string to a dictionary using ast.literal_eval().

    Returns:
        argparse.Namespace: Namespace object with arguments as attributes

    Raises:
        argparse.ArgumentError: If --config argument is not a valid dictionary string.
    """
    parser = argparse.ArgumentParser(
        description="Request ChatGPT to create the comparison job."
    )

    parser.add_argument(
        "--after-snapshot",
        dest="after_snapshot_contents",
        required=True,
        type=dict,
        help="The snapshot after the change",
    )

    parser.add_argument(
        "--before-snapshot",
        dest="before_snapshot_contents",
        required=True,
        type=dict,
        help="The snapshot before the change",
    )

    parser.add_argument(
        "--message",
        dest="message",
        required=True,
        help="The message to user's request",
    )

    parser.add_argument(
        "--log-level",
        dest="log_level",
        choices=LOGGING_LEVELS.keys(),
        default="debug",
        help="Set the logging output level",
    )

    parser.add_argument(
        "--expertise-level",
        dest="expertise_level",
        choices=EXPERTISE_LEVEL.keys(),
        default="expert",
        help="Set the technical depth that ChatGPT will respond in",
    )

    args = parser.parse_args()

    # Return an instance of Args model
    return Args(
        after_snapshot_contents=args.after_snapshot_contents,
        before_snapshot_contents=args.before_snapshot_contents,
        message=args.message,
        expertise_level=args.expertise_level,
        log_level=args.log_level,
    )


# ----------------------------------------------------------------------------
# Run operations
# ----------------------------------------------------------------------------
def run_change_analysis(
    after_snapshot_contents: Dict,
    before_snapshot_contents: Dict,
    message: str,
    expertise_level: str,
) -> Union[Dict[str, Union[str, int, float, bool]], None]:
    """
    Request ChatGPT to create a script and return the result of the operation.

    Args:
        after_snapshot_contents (dictionary): post change snapshot
        before_snapshot_contents (dictionary): pre change snapshot
        message (str): User's request

    Returns:
        dict: Result of the operation
        None: If target is invalid
    """
    # Get environment variables
    env = Env()
    env.read_env()

    # setup OpenAI API key
    openai_config = {
        "temperature": env.float("OPENAI_TEMPERATURE", 0.6),
        "max_tokens": env.int("OPENAI_MAX_TOKENS", 8192),
    }

    openai.api_key = env("OPENAI_API_KEY")

    results = None

    logging.debug("after_snapshot: %s", after_snapshot_contents)
    logging.debug("before_snapshot: %s", before_snapshot_contents)
    logging.debug("expertise_level: %s", expertise_level)

    # Accessing prompt using the get_prompt method
    prompt = chatgpt_prompts.get_prompt(expertise_level)

    logging.debug("prompt: %s", prompt)

    message = (
        f"{message} \n after: {after_snapshot_contents} \n before: {before_snapshot_contents}",
    )

    if prompt is not None:
        try:
            logging.info("Running request to ChatGPT...")
            results = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"{prompt}.",
                    },
                    {
                        "role": "user",
                        "content": f"{message}",
                    },
                ],
                **openai_config,
            )
            logging.info("ChatGPT request completed.")
            logging.debug("results: %s", results)
        except Exception as e:
            logging.error(f"ChatGPT request failed with exception: {e}")
            return
    else:
        logging.error(
            "Result of 'chatgpt_prompts.get_prompt(after_snapshot_contents, target)' was None"
        )
        return

    return results


# ----------------------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    # Configure logging
    logging.basicConfig(level=LOGGING_LEVELS[args.log_level])

    # Run script
    result = run_change_analysis(
        before_snapshot_contents=args.before_snapshot_contents,
        after_snapshot_contents=args.after_snapshot_contents,
        expertise_level=args.expertise_level,
        message=args.message,
    )
    if result:
        logging.debug(f'Result: {result["choices"][0]["message"]["content"]}')
    else:
        logging.error("Result was None")
