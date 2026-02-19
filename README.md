# CLRZ

Colorize standard output for better readability.

## Usage

To use this tool, simply preface another command with `clrz`. 

For example, to colorize the output of `go test`: 

```bash
clrz go test -v
```

## Installation

You can install CLRZ via `uv`:

```bash
uv tool install clrz
```
You can run it without installing:

```bash
uv tool run clrz
```
On windows you can use [Scoop](https://scoop.sh/):

```bash
scoop bucket add maciak https://github.com/maciakl/bucket
scoop update
scoop install clrz
```
