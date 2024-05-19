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
    conversation_id: str
    llm: str
    message: str
    persona: str
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
        "--conversation_id",
        dest="conversation_id",
        default="53d8ec7d-10f2-4e92-bd4b-de5537a5b0d0",
        help="The conversation_id to request ChatGPT to use to create the script",
    )

    parser.add_argument(
        "--llm",
        dest="llm",
        default="gpt-4",
        help="Which LLM to use for the conversation",
    )

    parser.add_argument(
        "--message",
        dest="message",
        required=True,
        help="The message to user's request",
    )

    parser.add_argument(
        "--persona",
        dest="persona",
        default="Other",
        help="Persona to use for the conversation",
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
        conversation_id=args.conversation_id,
        llm=args.llm,
        message=args.message,
        persona=args.persona,
        log_level=args.log_level,
    )


# ----------------------------------------------------------------------------
# Run operations
# ----------------------------------------------------------------------------
def run_send_message(
    conversation_id: str,
    llm: str,
    message: str,
    persona: str,
) -> Union[Dict[str, Union[str, int, float, bool]], None]:
    """
    Request ChatGPT to create a script and return the result of the operation.

    Args:
        conversation_id (str): Conversation_id for the ChatGPT script
        message (str): User's request
        llm (str): Palo Alto Networks product to llm
        persona (str): Persona to use for the conversation

    Returns:
        dict: Result of the operation
        None: If llm is invalid
    """
    # enforce lowercase
    persona = persona.lower()
    llm = llm.lower()

    # swap hyphens for underscores
    fixed_llm_name = format_llm(llm)

    # Get environment variables
    env = Env()
    env.read_env()

    # setup OpenAI API key
    openai_config = {
        "temperature": env.float("OPENAI_TEMPERATURE", 0.6),
        "max_tokens": env.int("OPENAI_MAX_TOKENS", 4096),
    }

    # Set max_tokens to 2048 if fixed_llm_name equals gpt_3_5_turbo
    if fixed_llm_name == "gpt_3_5_turbo":
        openai_config["max_tokens"] = 2048

    openai.api_key = env("OPENAI_API_KEY")

    results = None

    logging.info("conversation_id: %s", conversation_id)
    logging.info("llm: %s", llm)
    logging.info("persona: %s", persona)

    # Accessing prompt using the get_prompt method
    prompt = chatgpt_prompts.get_prompt(fixed_llm_name, persona)

    logging.info("prompt: %s", prompt)

    if prompt is not None:
        try:
            logging.info("Running request to ChatGPT...")
            results = openai.ChatCompletion.create(
                model=llm,
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
        logging.error("Result of 'chatgpt_prompts.get_prompt(llm, persona)' was None")
        return

    return results


def format_llm(llm: str) -> str:
    llm = llm.replace("-", "_")
    llm = llm.replace(".", "_")
    return llm


# ----------------------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    # Configure logging
    logging.basicConfig(level=LOGGING_LEVELS[args.log_level])

    # Run script
    result = run_send_message(
        conversation_id=args.conversation_id,
        message=args.message,
        llm=args.llm,
        persona=args.persona,
    )
    if result:
        logging.info(f'Result: {result["choices"][0]["message"]["content"]}')
    else:
        logging.error("Result was None")
