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
# Define models
# ----------------------------------------------------------------------------
class Args(BaseModel):
    language: str = "python"
    message: str
    target: str = "panorama"
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
    parser = argparse.ArgumentParser(description="Request ChatGPT to create script.")
    parser.add_argument(
        "--language",
        dest="language",
        default="python",
        help="The language to request ChatGPT to use to create the script",
    )

    parser.add_argument(
        "--message",
        dest="message",
        required=True,
        help="The message to user's request",
    )

    parser.add_argument(
        "--target",
        dest="target",
        default="panorama",
        help="Palo Alto Networks product to target",
    )

    parser.add_argument(
        "--log-level",
        dest="log_level",
        choices=LOGGING_LEVELS.keys(),
        default="debug",
        help="Set the logging output level",
    )

    args = parser.parse_args()

    # Return an instance of Args model
    return Args(
        language=args.language,
        message=args.message,
        target=args.target,
        log_level=args.log_level,
    )


# ----------------------------------------------------------------------------
# Run operations
# ----------------------------------------------------------------------------
def run_create_script(
    language: str,
    message: str,
    target: str,
) -> Union[Dict[str, Union[str, int, float, bool]], None]:
    """
    Request ChatGPT to create a script and return the result of the operation.

    Args:
        language (str): Language for the ChatGPT script
        message (str): User's request
        target (str): Palo Alto Networks product to target

    Returns:
        dict: Result of the operation
        None: If target is invalid
    """
    # enforce lowercase
    language = language.lower()
    target = target.lower()

    # Get environment variables
    env = Env()
    env.read_env()

    # setup OpenAI API key
    openai_config = {
        "temperature": env.float("OPENAI_TEMPERATURE", 0.6),
        "max_tokens": env.int("OPENAI_MAX_TOKENS", 4096),
    }

    openai.api_key = env("OPENAI_API_KEY")

    results = None

    logging.info("language: %s", language)
    logging.info("target: %s", target)
    logging.info("chatgpt_prompts: %s", chatgpt_prompts)

    # Accessing prompt using the get_prompt method
    prompt = chatgpt_prompts.get_prompt(language, target)

    logging.info("prompt: %s", prompt)

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
                    {"role": "user", "content": message},
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
            "Result of 'chatgpt_prompts.get_prompt(language, target)' was None"
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
    result = run_create_script(
        language=args.language,
        message=args.message,
        target=args.target,
    )
    if result:
        logging.info(f'Result: {result["choices"][0]["message"]["content"]}')
    else:
        logging.error("Result was None")
