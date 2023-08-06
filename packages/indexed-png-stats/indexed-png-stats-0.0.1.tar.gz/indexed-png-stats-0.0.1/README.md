# indexed-png-stats
Python library that inspects indexed PNG files.

## Installation

```
pip install indexed-png-stats
```

## Command-line

```
usage: indexed-png-stats [-h] -d DIR [-r] [-t {summary,per-file}]
                         [-f {plain-text,json}] [-o FILE] [-v]

Generates statistics from indexed PNG files.

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --image_dir DIR
                        the directory with the PNG files (default: None)
  -r, --recursive       whether to scan the directory recursively (default:
                        False)
  -t {summary,per-file}, --stats_type {summary,per-file}
                        the type of statistics to generate (default: summary)
  -f {plain-text,json}, --output_format {plain-text,json}
                        how to present the statistics (default: plain-text)
  -o FILE, --output_file FILE
                        the file to store the generated statistics in
                        (default: None)
  -v, --verbose         whether to be more verbose with the processing
                        (default: False)
```
