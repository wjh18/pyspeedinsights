"""Generic utilities that extend Python's built-in functionality."""


def remove_nonetype_dict_items(dct: dict) -> dict:
    """Dictcomp that creates a new dict excluding items with NoneType values."""
    return {k: v for k, v in dct.items() if v is not None}


def remove_dupes_from_list(lst: list) -> list:
    """Removes duplicate values from a list."""
    return list(set(lst))


def sort_dict_alpha(dct: dict) -> dict:
    """Sorts a dictionary alphabetically."""
    return dict(sorted(dct.items()))
