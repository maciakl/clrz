#!/usr/bin/env python3

# This script takes stdin and outputs to stdout colorizing the lines
# based on the presence of certain keywords.

# Main goal was to colorize Go test outputs.

import sys
import termcolor
from collections import namedtuple

VERSION = "0.0.1"


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Process interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except BrokenPipeError:
        print("Broken pipe error.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def run():

    Category = namedtuple("Category", ["keywords", "color"])

    # categories to be colorized
    categories = {
        "fail":     Category(["Fail", "FAIL", "Failed", "FAILED"], "red"),
        "pass":     Category(["PASS", "Passed", "PASSED"], "green"),
        "run":      Category(["RUN", "Executing", "EXECUTING"], "blue"),
        "error":    Category(["ERROR", "Error", "ERRORS", "Errors"], "red"),
        "warning":  Category(["WARN", "Warning", "WARNING"], "yellow"),
        "info":     Category(["INFO", "Information", "INFORMATION"], "blue"),
        "debug":    Category(["Debug", "DEBUG"], "magenta"),
        "trace":    Category(["Trace", "TRACE"], "cyan"),
        "critical": Category(["Critical", "CRITICAL"], "red"),
        "success":  Category(["Success", "SUCCESS"], "green"),
        }

    for line in sys.stdin:

        color = None

        # set color based on category
        for name in list(categories.keys()):
            cat = categories[name]
            if any(keyword in line for keyword in cat.keywords):
                color = cat.color
                break

        # print to stdout and flush the buffer
        sys.stdout.write(termcolor.colored(line, color) if color else line)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
