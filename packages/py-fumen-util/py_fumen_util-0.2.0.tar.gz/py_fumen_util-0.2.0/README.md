# py-fumen-util
Python implementation of [swng's FumenUtil](https://github.com/swng/FumenUtil), using [py-fumen-py](https://github.com/OctupusTea/py-fumen-py)

## Dependency
- `py-fumen-py`: Python implementation of knewjade's `tetris-fumen` node module

## Installation

```bash
python3 -m pip install py-fumen-util
```

## Usage

```bash
python3 -m py_fumen_util command [commmand...] file
```

- `command`: Command(s) to execute on the Fumen(s).
- `file`: File with Fumen strings, separated with whitespace and/or linebreak. Use "-" to read from standard input.

### Commands

Commands are case-insensitive.

|Command|Description|Alias|
|:-|:-|:-|
|Combine|Combine multiple Fumens into one|Concat, Join|
|Split|Split each page into a Fumen||
|Glue|Glue each Fumen page into tetromino placements|Decompile|
|Unglue|Unglue Fumen placements into one page|Compile|
|Gray|Gray out the last of each Fumen|Grey|
|Grayall|Gray out all pages of each Fumen|Greyall|
|Lock|Lock the last page of each Fumen and append a new page||
|Mirror|Mirror Fumen pages|Flip|
|Uncomment|Uncomment Fumen pages||
