# anncheck
Check for missing annotations in Python. It's super fast compared to mypy, checking for missing
annotations in [sympy](https://github.com/sympy/sympy) gave the following results:

| Benchmark | Query | Result | Execution time |
| :-------- | :---: | :----: | -------------: |
| MyPy | `mypy --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs sympy` | Found 31037 errors in 1171 files (checked 1405 source files) | 88.32 s |
| Anncheck | `anncheck sympy -r` | Found 128059 variables missing annotation(s) in 1197 files | 47.28 s |
| Anncheck Compact mode  | `anncheck sympy -r -c` | Found 128059 variables missing annotation(s) in 1197 files | 4.47 s |

It also has more options for annotation checking.

## Installation

`pip install anncheck`

## Usage

```
Usage: anncheck [OPTIONS] SRC...

Options:
  -a, --include-asterisk    Include variables starting with '*'.  [default:
                            False]

  -c, --compact             Compact mode, displays file name and number of
                            missing annotations on a single line.  [default:
                            False]

  -d, --include-docstrings  Anncheck doesn't check for functions inside
                            triple-quotes by default, set flag to do.
                            [default: False]

  -e, --exclude-return      Exclude return annotations.  [default: False]
  -n, --new-line            Set flag to separate functions by an empty line.
                            [default: False]

  -r, --recursive           Set flag to recursively go into folders.
                            [default: False]

  -m, --exclude-main        Exclude functions defined in 'if __name__ ==
                            "__main__": ...'  [default: False]

  -p, --padding INTEGER     Padding for line number.  [default: 3]
  --exclude-dunder          Exclude dunder functions.  [default: False]
  --init-return             Set flag to show if __init__ is missing a return
                            annotation.  [default: False]

  --match-function TEXT     Only search functions matching regex. Note: Put
                            regex in quotes.

  --match-variable TEXT     Match variables with regex. Note: Put regex in
                            quotes.

  --help                    Show this message and exit.
```