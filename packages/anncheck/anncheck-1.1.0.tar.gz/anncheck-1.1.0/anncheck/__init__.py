from colorama import Style as s
from colorama import Fore as fo
from colorama import init
import typing as ty
import click
import glob
import time
import os
import re


init()

r"""
    \s*                    # Whitespace
    (\*{0,2}[a-zA-Z_0-9]+) # Valid characters for variable name, group is full name of variable
    \s*                    # Whitespace
    [=,]*                  # Variables are seperated by either = or ,
"""
VARIABLE_RE = re.compile(r"\s*([*a-zA-Z_0-9]+)\s*[=,]*")
# Regex to match variable name
# Group 0 - Full match
# Group 1 - Variable name

r"""
    \(          # Opening parentheses of function defenition
        (.*)    # Variables etc.
    \)          # Closing parentheses of function defenition
    (           # Open capture group for return annotation
        [ ]*    # Space before arrow
        ->      # Arrow denoting return annotation
        [ ]*    # Space after arrow
        [^:]+   # The return annotation
                # 
    )?:         # Close return annotation group, also
                # make it optional and add colon to indicate
                # the end of function definition.
"""
FUNC_INFO_RE = re.compile(
    r"\((.*)\)( *-> *[^:]+)?:", re.DOTALL
)
# Regex to match variables and return annotation
# from first parenthesis after function name until colon
# Group 0 - Full match
# Group 1 - Variables
# Group 2 - Return annotation (if any)

r"""
    ^                   # Start of line to not match `def` keyword insides string etc
    (?:                 # Open capture group for characters before `def`
        [ \t]           # Valid characters before `def` is spaces and tabs
        |               # or
        (?:             # Open capture group for `async` keyword
            async       # `async` can be before `def`
        )               #
    )*                  # Close capture group for chars before `def`
      def[ ]            # the `def` keyword
    (                   # Open capture group for function name
        [a-zA-Z_0-9]+   # Valid function name characters
    )
    \(                  # First parentheses of function definition
"""
FIND_FUNC_DEF_RE = re.compile(
    r"^(?:[ \t]|(?:async))*def ([a-zA-Z_0-9]+)\(", re.MULTILINE
)
# Regex to find a function definition
# Group 0 - Full match
# Group 1 - Function name

r"""
    \"{3}   # Opening triple quotes
    (.*?)   # everything inside multiline comment
    \"{3}   # Closing triple quotes
"""
TRIPLE_Q_RE = re.compile(
    r"\"{3}(.*?)\"{3}", re.DOTALL
)
# Regex for matching anything inside triple quotation marks (")
# Group 0 - Full match
# Group 1 - Text inside comment

r"""
    \'{3}   # Opening triple apostrophes
    (.*?)   # everything inside multiline comment
    \'{3}   # Closing triple apostrophes
"""
TRIPLE_A_RE = re.compile(
    r"\'{3}(.*?)\'{3}", re.DOTALL
)
# Regex for matching anything inside triple apostrophes (')
# Group 0 - Full match
# Group 1 - Text inside comment

r"""
(?s)              # the dot matches newlines too
(                 # open the capture group 1
    ["']          # " or '
    [^"'\\]*      # all characters except a quote, backslash, or an apostrophe
                  # zero or more times
    (?:           # open a non-capturing group
        \\.       # a backslash and any character
        [^"'\\]*  # 
    )*            # repeat zero or more times
    ["']          # " or '
)                 # close the capture group 1

|                 # OR

#[^\n]*           # a sharp and zero or one characters that are not a newline.
"""
COMMENT_RE = re.compile(
    r"(?s)([\"'][^\"'\\]*(?:\\.[^\"'\\]*)*[\"'])|#[^\n]*",
    flags=re.MULTILINE
)
# Regex for everything after "#" until line end
# Group 0 - Full match
# Group 1 - Empty

r"""
    ^(              # Line must start with whole match
        if +        # `if` and optional space
        __name__    # Match string
        [ ]*==[ ]*  # Comparison with optional space around it
        ['"]        # Match either quote or apostrophe
        __main__    # Match string
        ['"]        # Match either quote or apostrophe
        [ ]*:       # Optional space after string and colon ending function defenition
    )
"""
MAIN_RE = re.compile(
    r"^(if +__name__ *== *('|\")__main__('|\") *:)", flags=re.MULTILINE
)
# Regex for matching line containing if __name__ == '__main__'
# Group 0 - Full match
# Group 1 - Whole line


def _split_vars(input_str: str) -> list:
    """Split variables into a list.

    This function ensures it splits variables based on commas not inside
    default values or annotations but those between variables only. Brackets,
    commas, and parentheses inside strings will not count.
    """
    input_str = input_str.rstrip()
    parent_count = 0
    bracket_count = 0
    last_read = 0
    str_count = 0
    output = []

    for i, char in enumerate(input_str):
        if char in "\"'":
            str_count = 0 if str_count == 1 else 1

        if str_count == 0:
            if char == ",":
                if bracket_count == 0 and parent_count == 0:
                    output.append(input_str[last_read:i])
                    last_read = i + 1
            elif char == "(":
                parent_count += 1
            elif char == "[":
                bracket_count += 1
            elif char == ")":
                parent_count -= 1
            elif char == "]":
                bracket_count -= 1

    _last_var = input_str[last_read: len(input_str)]
    if _last_var:
        output.append(_last_var)
    return output


def _get_function_def(start: int, input_string: str) -> str:
    """Get index on first parentheses from function definition
    and return the string of the whole function definition.
    """
    i = start
    paren_count = 0
    while i < len(input_string):
        if input_string[i] == "(":
            paren_count += 1
        if input_string[i] == ")":
            paren_count -= 1
        if input_string[i] == ":" and paren_count == 0:
            return input_string[start: i + 1]
        i += 1
    return ""


def _is_dunder(function_name: str) -> bool:
    """Checks if a function is a dunder function."""
    return function_name.startswith("__") and function_name.endswith("__")


def _doc(match: re.Match) -> str:
    """Returns string filled with dots with same number of lines as match
    so the line numbers doesn't get messed up
    """
    return "\n" * match.group(0).count("\n")


def _finditer_with_line_numbers(
    pattern: re.Pattern, string: str
) -> ty.Iterator[ty.Tuple[re.Match, int]]:
    """
    A version of 're.finditer' that returns '(match, line_number)' pairs.
    """

    matches = list(pattern.finditer(string))
    if not matches:
        return []

    end = matches[-1].start()
    # -1 so a failed 'rfind' maps to the first line.
    newline_table = {-1: 0}
    for i, m in enumerate(re.finditer(r"\n", string), 1):
        # don't find newlines past our last match
        offset = m.start()
        if offset > end:
            break
        newline_table[offset] = i

    # Failing to find the newline is OK, -1 maps to 0.
    for m in matches:
        newline_offset = string.rfind("\n", 0, m.start())
        line_number = (
            newline_table[newline_offset] + 1
        )  # + 1 since line numbers doesnt start at 0
        yield m, line_number


def _has_annotation(var: str) -> bool:
    """Check if a variable has an annotation. 'self' and 'cls'
    can't have annotations.

    :param var: str
        String containing variable name, annotations, and default value
    :return: bool
        Returns whether or not the variable has an annotation
    """
    if var.strip() == "self" or var.strip() == "cls":
        return True
    return ":" in var


def _get_file_info(path: str, **options: ty.Dict[str, ty.Union[str, bool]]) -> list:
    """Checks for annotations for each function in a file given its path.

    :param path: str
        Path of file
    :param options: dict
        Options
    :return: list
        List containing each missing annotation with function name, line number,
        and variable name
    """
    output_list = []

    with open(f"{os.getcwd()}\\{path}", "r", encoding="utf8") as f:
        _file_text = f.read()

    _source_file = _file_text

    if options["exclude_main"]:
        if MAIN_RE.search(_file_text):
            for f, l in _finditer_with_line_numbers(MAIN_RE, _source_file):
                _main_line = l
        else:
            _main_line = None
    else:
        _main_line = None

    # Remove everything inside triple quotes and comments and
    # Remove comments
    if not options["include_docstrings"]:
        _file_text = TRIPLE_Q_RE.sub(_doc, _file_text)
        _file_text = TRIPLE_A_RE.sub(_doc, _file_text)
    _file_text = COMMENT_RE.sub(lambda m: m.group(1) if m.group(1) else "", _file_text)

    if options["match_function"]:
        match_func = re.compile(options["match_function"])
    else:
        match_func = None

    if options["match_variable"]:
        match_var = re.compile(options["match_variable"])
    else:
        match_var = None

    for func, _line_number in _finditer_with_line_numbers(FIND_FUNC_DEF_RE, _file_text):
        if _main_line:
            if _line_number >= _main_line:
                return output_list

        has_output = 0
        _func_name = func.group(1)

        if match_func:
            if not match_func.match(_func_name):
                continue

        if options["exclude_dunder"]:
            if _is_dunder(_func_name):
                continue

        _func_rest = _get_function_def(func.span()[1] - 1, _file_text)
        _func_rest_m = FUNC_INFO_RE.search(_func_rest)
        if not _func_rest_m:
            raise Exception("Failed to parse function, make sure function is syntactically correct. Maybe it's a "
                            "function incorrectly defined in a docstring?")

        _func_vars_str = _func_rest_m.group(1)
        _func_return_ann = _func_rest_m.group(2)

        _func_vars = _split_vars(_func_vars_str)

        _line_number = (
            (" " * (options["padding"] - len(str(_line_number))) if len(str(_line_number)) < options["padding"] else "")
        ) + str(_line_number)

        for f_var in _func_vars:
            if f_var:
                if not _has_annotation(f_var):
                    _var_name = VARIABLE_RE.search(f_var).group(1).strip()

                    if match_var:
                        if not match_var.match(_var_name):
                            continue

                    if not options["include_asterisk"]:
                        if _var_name.startswith("*"):
                            continue

                    output_list.append(
                        f"{fo.MAGENTA}{_line_number}{s.RESET_ALL}:"
                        f"Function {fo.BLUE}{_func_name}{s.RESET_ALL} is missing annotations for "
                        f"argument {fo.MAGENTA}{_var_name}{s.RESET_ALL}."
                    )
                    has_output = 1

        if not _func_return_ann and not options["exclude_return"]:
            # if init_return - show return
            # else: show if not
            if options["init_return"]:
                output_list.append(
                    f"{fo.MAGENTA}{_line_number}{s.RESET_ALL}:"
                    f"Function {fo.BLUE}{_func_name}{s.RESET_ALL} is missing a return annotation."
                )
                has_output = 1
            else:
                if not(_func_name == "__init__" and not _func_return_ann):
                    output_list.append(
                        f"{fo.MAGENTA}{_line_number}{s.RESET_ALL}:"
                        f"Function {fo.BLUE}{_func_name}{s.RESET_ALL} is missing a return annotation."
                    )
                    has_output = 1

        if options["new_line"] and has_output == 1:
            output_list.append("")

    return output_list


@click.command()
@click.option(
    "-a",
    "--include-asterisk",
    is_flag=True,
    default=False,
    show_default=True,
    help="Include variables starting with '*'.",
)
@click.option(
    "-c",
    "--compact",
    is_flag=True,
    default=False,
    show_default=True,
    help="Compact mode, displays file name and number of missing annotations on a single line.",
)
@click.option(
    "-d",
    "--include-docstrings",
    is_flag=True,
    default=False,
    show_default=True,
    help="Anncheck doesn't check for functions inside triple-quotes by default, set flag to do.",
)
@click.option(
    "-e",
    "--exclude-return",
    is_flag=True,
    default=False,
    show_default=True,
    help="Exclude return annotations.",
)
@click.option(
    "-n",
    "--new-line",
    is_flag=True,
    default=False,
    show_default=True,
    help="Set flag to separate functions by an empty line.",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
    show_default=True,
    help="Set flag to recursively go into folders.",
)
@click.option(
    "-m",
    "--exclude-main",
    is_flag=True,
    default=False,
    show_default=True,
    help="Exclude functions defined in 'if __name__ == \"__main__\": ...'",
)
@click.option(
    "-p",
    "--padding",
    type=int,
    default=3,
    show_default=True,
    help="Padding for line number."
)
@click.option(
    "--exclude-dunder",
    is_flag=True,
    default=False,
    show_default=True,
    help="Exclude dunder functions."
)
@click.option(
    "--init-return",
    is_flag=True,
    default=False,
    show_default=True,
    help="Set flag to show if __init__ is missing a return annotation."
)
@click.option(
    "--match-function",
    type=str,
    help="Only search functions matching regex. Note: Put regex in quotes.",
)
@click.option(
    "--match-variable",
    type=str,
    help="Match variables with regex. Note: Put regex in quotes.",
)
@click.argument(
    "src",
    type=click.Path(
        exists=True,
        readable=True,
        path_type=str,
    ),
    nargs=-1,
    required=True,
)
def main(src: click.Path, **options: ty.Dict[str, ty.Union[str, bool]]) -> None:
    start = time.time()
    count = 0
    file_count = 0
    if os.path.isdir(src[0]):
        if options["recursive"]:
            for filename in glob.iglob(src[0] + "/" + "**/**.py", recursive=True):
                _output = _get_file_info(filename, **options)
                if _output:
                    file_count += 1
                    count += len(_output)

                    if options["compact"]:
                        print(
                            f"{fo.GREEN}{filename}{s.RESET_ALL}:"
                            f"Missing {fo.BLUE}{len(_output)}{s.RESET_ALL}"
                            f" annotations."
                        )
                    else:
                        print(
                            f"\n{'-' * 10} {fo.GREEN}{filename}{s.RESET_ALL} {'-' * 10}\n"
                        )
                        for f in _output:
                            print(f)
            else:
                for filename in glob.iglob(src[0] + "/" + "*.py"):
                    _output = _get_file_info(filename, **options)
                    if _output:
                        file_count += 1
                        count += len(_output)

                        if options["compact"]:
                            print(
                                f"{fo.GREEN}{filename}{s.RESET_ALL}:"
                                f"Missing {fo.BLUE}{len(_output)}{s.RESET_ALL}"
                                f" annotations."
                            )
                        else:
                            print(
                                f"\n{'-' * 10} {fo.GREEN}{filename}{s.RESET_ALL} {'-' * 10}\n"
                            )
                            for f in _output:
                                print(f)
    else:
        _output = _get_file_info(src[0], **options)
        if _output:
            if options["compact"]:
                print(
                    f"{fo.GREEN}{src[0]}{s.RESET_ALL}:"
                    f"Missing {fo.BLUE}{len(_output)}{s.RESET_ALL}"
                    f" annotations."
                )
            else:
                for f in _output:
                    count += 1
                    print(f)
        else:
            print(f"The file '{src[0]}' aren't missing annotations")

    print(f"\nFound {fo.RED if count else fo.GREEN}{count}{s.RESET_ALL}", end=" ")
    print(f"missing annotation(s) in", end=" ")
    print(
        f"{fo.BLUE}{file_count}{s.RESET_ALL} file{'' if file_count == 1 else 's'}.",
        end=" ",
    )
    print(f"Execution time: {fo.CYAN}{round(time.time() - start,2)}{fo.RESET}s")
