import re

LACKING_BREAKLINE = re.compile(r"\s{2}\n(?!\n)")
EXTRA_BLOCKQUOTE = re.compile(r"(\n>\s){2}(\s\n)?(?!\s\w+)")
EXTRA_SPACE = re.compile(r"\n\s+")

SUBHEADER = re.compile(
    r"""
    (^|\s{2,}) # must have 2 or more spaces or be start of line
    \*{2,3}
    (?P<heading>.*?)
    \*{2,3}\s*\n
    """,
    re.X,
)

RULING = re.compile(
    r"""
    \W+
    (?P<ruling>
        the
        \s+
        court
        [\W\ss]+
        ruling
    )
    \W+
    """,
    re.I | re.X,
)  # sample  **The Court's Ruling**

BR = "\n\n"


def clean(text: str):
    if match := RULING.search(text):
        text = RULING.sub(f"{BR}## {match.group('ruling')}{BR}", text)
    for match in SUBHEADER.finditer(text):
        if old_text := match.group():
            if heading := match.group("heading"):
                replacement = f"{BR}### {heading}{BR}"
                text = text.replace(old_text, replacement)
    text = EXTRA_BLOCKQUOTE.sub(BR, text)
    text = LACKING_BREAKLINE.sub(BR, text)
    text = EXTRA_SPACE.sub(BR, text)

    return text.strip()
