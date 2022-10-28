import keyring
from keyring.errors import KeyringError


def get_api_key():
    """
    Get the user's PSI API key from their keystore using keyring.

    Allow manual entry of key if nonexistent or keystore errors occur.

    Re-prompt for keys read in as empty strings. Otherwise, key validation
    should be lenient with any errors handled at request time.
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
