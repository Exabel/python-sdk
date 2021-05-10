
def escape(string: str) -> str:
    """
    Returns the SQL representation of the given string,
    by escaping all single-quotes with two single-quotes
    and surrounding the string with single-quotes.
    """
    return f"""'{string.replace("'", "''")}'"""
