#!/usr/bin/env python3

# This script takes stdin and outputs to stdout colorizing the lines
# based on the presence of certain keywords.

# Main goal was to colorize Go test outputs.

import sys
import termcolor
from collections import namedtuple

VERSION = "0.1.1"


def main():

    name = termcolor.colored("clrz", "cyan", attrs=["bold"])
    ver = termcolor.colored(f"{VERSION}", "yellow", attrs=["bold"])

    # check for flags
    if "-v" in sys.argv or "--version" in sys.argv:
        print(f"{name} v{ver}")
        sys.exit(0)

    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"{name} v{ver} - colorize stdin based on keywords\n")
        print("\nUsage: clrz [options]\n")
        print("Options:")
        print("  -h, --help       Show this help message and exit")
        print("  -v, --version    Show version information and exit")
        print("\nExample:")
        print(f"  go test -v ./... | {name}")
        sys.exit(0)

    try:
        run()
    except KeyboardInterrupt:
        print(termcolor.colored("Process interrupted by user.", "red"),
              file=sys.stderr)
        sys.exit(1)
    except BrokenPipeError:
        print(termcolor.colored("Broken pipe error.", "red"),
              file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(termcolor.colored(f"Unexpected error: {e}", "red"),
              file=sys.stderr)
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
        "info":     Category(["INFO", "Info", "INFORMATION"], "blue"),
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
