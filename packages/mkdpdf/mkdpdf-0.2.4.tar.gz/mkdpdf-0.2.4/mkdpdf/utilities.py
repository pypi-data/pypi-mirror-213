import re

from mkdpdf import configuration

def clean(content: str) -> str:
    """
    Cleanup on markdown for downstream render.

    Args:
        content (string): partial of Markdown or HTML

    Returns:
        A string representing the content.
    """

    # clean up content
    content = re.sub(r"^__", "", content, flags=re.MULTILINE)
    content = re.sub(r"^None", "\n", content, flags=re.MULTILINE)
    content = re.sub(r"(\r\n\r\n)+", "REPLACE_RETURNS", content)
    content = re.sub(r"\r\n", "KEEP_RETURNS", content)
    content = re.sub(r"\n+", "REPLACE_RETURNS", content)
    content = re.sub(r"KEEP_RETURNS", configuration.GITFLAVOR_BREAK_RETURN, content)
    content = re.sub(r"REPLACE_RETURNS", "\n\n", content)
    content = re.sub(r"\n+\Z", "", content)
    content = re.sub(r"```python\n+", "```python%s" % configuration.GITFLAVOR_BREAK_RETURN, content)
    content = re.sub(r"\n+```\n+", "%s```%s" % (configuration.GITFLAVOR_BREAK_RETURN, configuration.GITFLAVOR_RETURN), content)

    return content
