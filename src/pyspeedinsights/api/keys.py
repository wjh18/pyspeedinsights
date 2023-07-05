"""PageSpeed Insights API key management operations.

Storing an API key in keyring: `keyring set system psikey`
Verifying an API key is stored: `keyring get system psikey`
Removing an API key from keyring: `keyring del system psikey`

If no key is set in keyring, the user will be manually prompted for their key.
"""

import logging

import keyring
from keyring.errors import KeyringError

logger = logging.getLogger(__name__)


class RetryLimitExceededError(KeyringError):
    """Exception if the user has exceeded the retry limit for entering an API key."""


class InputTerminatedError(KeyringError):
    """Exception if the user manually terminates retry for entering an API key."""


def get_api_key() -> str:
    """Gets the user's PSI API key from their keyring store.

    Allows manual entry of the key if nonexistent or keystore errors occur.
    Reprompts for keys read in as empty strings. Otherwise, key validation should be
    lenient with errors handled at request time (in case Google changes the key format).

    Returns:
        A str representing the PSI API key.
    Raises:
        InputTerminatedError: The user terminated the reprompt.
        RetryLimitExceededError: The reprompt limit was exceeded.
    """
    logger.info("Attempting to retrieve API key from keystore.")
    try:
        # get_password() returns None for an empty key
        psi_api_key = keyring.get_password("system", "psikey")
    except KeyringError as err:
        logger.error(
            f"There was an error retrieving your API key from the keystore: {err}",
            exc_info=True,
        )
        psi_api_key = None

    if psi_api_key is None:
        logger.warning("No API key found. Defaulting to manual input.")
        psi_api_key = input("No API key found. Enter your key manually:\n")

    retry_limit = 5
    while not psi_api_key:
        logger.warning("Empty API key supplied. Reprompting user for key.")
        reprompt = input(
            "Empty API key supplied. Please re-enter your key or Q to quit:\n"
        )
        # Below errors logged as CRITICAL in main() before exit
        if reprompt in ("Q", "q"):
            raise InputTerminatedError("API key input cancelled.")
        elif retry_limit < 1:
            raise RetryLimitExceededError("Retry limit for entering API key exceeded.")
        else:
            psi_api_key = reprompt
        retry_limit -= 1

    logger.info("API key retrieval successful.")
    return psi_api_key
