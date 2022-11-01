"""PageSpeed Insights API key management operations.

Storing an API key in keyring: `keyring set system psikey`
Verifying an API key is stored: `keyring get system psikey`
Removing an API key from keyring: `keyring del system psikey`

If no key is set in keyring, the user will be manually prompted for their key.
"""

import keyring
from keyring.errors import KeyringError


def get_api_key() -> str:
    """Gets the user's PSI API key from their keyring store.

    Allows manual entry of the key if nonexistent or keystore errors occur.
    Reprompts for keys read in as empty strings. Otherwise, key validation should be
    lenient with errors handled at request time (in case Google changes the key format).

    Returns:
        A str representing the PSI API key.
    Raises:
        SystemExit: The user terminated the reprompt.
    """
    try:
        # get_password() returns None for an empty key
        PSI_API_KEY = keyring.get_password("system", "psikey")
    except KeyringError:
        print("There was an error retrieving your API key from the keystore.")
        PSI_API_KEY = None

    if PSI_API_KEY is None:
        PSI_API_KEY = input("No API key found. Enter it manually:\n")

    while not PSI_API_KEY:
        reprompt = input(
            "Empty API key supplied. Please re-enter your key or Q to quit:\n"
        )
        if reprompt in ["Q", "q"]:
            raise SystemExit
        else:
            PSI_API_KEY = reprompt

    return PSI_API_KEY
