def template(text, username, level=None):
    """
    Replaces placeholders in the given text with actual values.

    Args:
        text (str): The template text containing placeholders.
        username (str): The username to replace "{user}" placeholder.
        level (int, optional): The level to replace "{level}" placeholder. Defaults to None.

    Returns:
        str: The formatted text.
    """
    replacements = {
        "{user}": username,
        "{level}": str(level) if level is not None else ""
    }

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text
