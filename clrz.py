#!/usr/bin/env python3

# This script wraps around a cli command and colorizes its output
# based on the presence of certain keywords.

# Main goal was to colorize Go test outputs.

import sys
import subprocess
import termcolor
from collections import namedtuple

VERSION = "0.2.1"


def err(msg):
    print(termcolor.colored(msg, "red"), file=sys.stderr)


def main():

    if len(sys.argv) < 2:
        err("No command provided. Use -h for help.")
        sys.exit(1)

    name = termcolor.colored("clrz", "cyan", attrs=["bold"])
    ver = termcolor.colored(f"{VERSION}", "yellow", attrs=["bold"])

    # check for flags
    if sys.argv[1] == "-v" or sys.argv[1] == "--version":
        print(f"{name} v{ver}")
        sys.exit(0)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(f"{name} v{ver} - colorize stdin based on keywords\n")
        print("\nUsage: clrz [options] <command>\n")
        print("Options:")
        print("  -h, --help       Show this help message and exit")
        print("  -v, --version    Show version information and exit")
        print("\nExample:")
        print(f"  {name} go test -v ./...")
        sys.exit(0)

    cmd = sys.argv[1:]

    try:
        run(cmd)
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


def run(cmd):

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

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:

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
