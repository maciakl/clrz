# CLRZ

Colorize standard output for better readability.

## Usage

To use this tool, simply pipe the output of another command into it:

```bash
go test -v | clrz
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
