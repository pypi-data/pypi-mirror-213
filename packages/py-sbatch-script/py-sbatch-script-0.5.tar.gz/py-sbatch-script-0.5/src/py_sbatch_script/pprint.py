"""Pretty printing helpers."""

import json
from textwrap import dedent

import pygments
from pygments.lexers.shell import BashLexer
from pygments.lexers.data import JsonLexer
from pygments.styles import get_style_by_name

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles.pygments import style_from_pygments_cls


def get_pygments_style(style):
    style = get_style_by_name(style)
    style = style_from_pygments_cls(style)  # type: ignore
    return style


PYGMENTS_STYLE = get_pygments_style("gruvbox-dark")

DEFAULT_STYLE = Style.from_dict(
    {
        "prompt": "ansimagenta bold",
        "success": "ansigreen bold",
        "info": "ansicyan",
        "warn": "ansiyellow bold",
        "error": "ansired bold",
    }
)


def pprint(text):
    print_formatted_text(HTML(text), style=DEFAULT_STYLE)


def pprint_info(text):
    return pprint(f"<info>{text}</info>")


def pprint_warn(text):
    return pprint(f"<warn>{text}</warn>")


def pprint_error(text):
    return pprint(f"<error>{text}</error>")


def pprint_success(text):
    return pprint(f"<success>{text}</success>")


def pprint_cmd(cmd):
    cmd = dedent(cmd).strip()
    tokens = pygments.lex(cmd, lexer=BashLexer())
    tokens = list(tokens)
    pygments_tokens = PygmentsTokens(tokens)
    print_formatted_text(pygments_tokens, style=PYGMENTS_STYLE)


def pprint_json(obj):
    obj_str = json.dumps(obj, indent=2)
    tokens = pygments.lex(obj_str, lexer=JsonLexer())
    tokens = list(tokens)
    pygments_tokens = PygmentsTokens(tokens)
    print_formatted_text(pygments_tokens, style=PYGMENTS_STYLE)
