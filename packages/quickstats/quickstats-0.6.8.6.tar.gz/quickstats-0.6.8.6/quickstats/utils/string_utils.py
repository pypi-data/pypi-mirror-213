from typing import Optional, Callable
import re

whitespace_trans = str.maketrans('', '', " \t\r\n\v")
newline_trans = str.maketrans('', '', "\r\n")

def split_lines(string:str, comment_string:Optional[str]="#", remove_blank:bool=True,
                with_line_number:bool=False, keepends:bool=False):
    lines = string.splitlines(keepends=keepends)
    # remove comments
    lines = [l.split(comment_string)[0] for l in lines]
    # remove blank lines
    if with_line_number:
        if remove_blank:
            return [(l, i+1) for i, l in enumerate(lines) if not re.match(r'^\s*$', l)]
        return [(l, i+1) for i, l in enumerate(lines)]
    if remove_blank:
        lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
    return lines


def split_str(string:str, sep:str=None, strip:bool=True,
              remove_empty:bool=False, cast:Optional[Callable]=None):
    if strip:
        tokens = [s.strip() for s in string.strip().split(sep)]
    else:
        tokens = string.split(sep)
    if remove_empty:
        # remove empty tokens
        tokens = [s for s in tokens if s]
    if cast is not None:
        tokens = [cast(s) for s in tokens]
    return tokens

def remove_whitespace(string:str):
    return string.translate(whitespace_trans)

def remove_newline(string:str):
    return string.translate(newline_trans)