"""Terminal colors."""
import html.parser
import logging
from typing import Optional, TypedDict

import termcolor


class ColoredFuncKwargs(TypedDict, total=False):
    """Colored func kwargs."""

    bold: Optional[bool]
    color: str | None


def colored(text, color: str | None = None, bold=True) -> str:
    """Return colored text."""
    attrs = []
    if bold:
        attrs.append("bold")
    return termcolor.colored(text, color=color, attrs=attrs)


class ColorParser(html.parser.HTMLParser):
    """Parse color markup."""

    tag_mapping: dict[str, ColoredFuncKwargs] = {
        "b": {"bold": True},
        "g": {"color": "green"},
        "y": {"color": "yellow"},
    }

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        """Initialise class variables."""
        super().__init__(convert_charrefs=convert_charrefs)
        self._text = ""
        self._style_stack: list[ColoredFuncKwargs] = []
        self._tag_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        """Handle start tags."""
        assert tag in self.tag_mapping, f"Unexpected open tag: <{tag}>. Tag is unknown."
        self._tag_stack.append(tag)
        self._style_stack.append(
            (self.get_current_style() or {}) | self.tag_mapping[tag]
        )

    def handle_endtag(self, tag: str) -> None:
        """Handle end tags."""
        assert self._tag_stack, "Unexpected close tag. No tags currently open."
        assert (
            self._tag_stack[-1] == tag
        ), f"Unexpected close tag: </{tag}>. Expected: </{self._tag_stack[-1]}>"
        self._tag_stack.pop()
        self._style_stack.pop()

    def handle_data(self, data: str) -> None:
        """Color the data based on the current style."""
        style = self.get_current_style()
        self._text += colored(data, **style) if style else data

    def get_current_style(self) -> ColoredFuncKwargs | None:
        """Return the current style or none."""
        if not self._style_stack:
            return None
        return self._style_stack[-1]

    def colorise(self, text: str) -> str:
        """Parse and colorise the passed text."""
        self.feed(text)
        return self._text


def colorise(text):
    """Colorise text."""
    return ColorParser().colorise(text)


class ColoredLoggingFormatter(logging.Formatter):
    """Logging formatter with colored output."""

    formats: dict[int, ColoredFuncKwargs | None] = {
        logging.DEBUG: None,
        logging.INFO: None,
        logging.WARNING: {"color": "yellow"},
        logging.ERROR: {"color": "red"},
        logging.CRITICAL: {"color": "red", "bold": True},
    }

    def format(self, record):
        """Format record."""
        style = self.formats.get(record.levelno)
        text = super().format(record)
        return colored(text, **style) if style else text


def get_colored_logger(*args, **kwargs):
    """Return a colored logger."""
    logger = logging.Logger(*args, **kwargs)
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredLoggingFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
