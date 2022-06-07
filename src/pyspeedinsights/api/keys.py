import keyring


def get_api_key():
    """
    Get the user's PSI API key from their keystore using keyring.

    Exit the program if key is not set.
    """

    PSI_API_KEY = keyring.get_password("system", "psikey")

    if PSI_API_KEY is not None:
        return PSI_API_KEY
    else:
        err = "Error: Your PageSpeed Insights API key is empty.\
              \nGenerate a key with Google and set it with the command\
                  `keyring set system psikey`.\
              \nTo verify your key can be found, run the command\
                  `keyring get system psikey`."
        raise SystemExit(err)
