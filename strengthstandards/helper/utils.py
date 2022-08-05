import re


def table_namer(string: str) -> str:
    """
    Function for parsing soon-to-be SQL table names.

    Args:
        string (str): Some string to be converted into a table name.
    Returns:
        str: new table name
    Notes:
    Todo:
    """
    # Replace any hyphens
    new_table_name = string.replace("-", "_")
    # Grab [a-zA-Z0-9_]
    new_table_name = re.sub("\W+", "", new_table_name)
    # Convert to lowercase
    new_table_name = new_table_name.lower()
    # Remove leading/trailing whitespace
    new_table_name = new_table_name.strip()

    return new_table_name