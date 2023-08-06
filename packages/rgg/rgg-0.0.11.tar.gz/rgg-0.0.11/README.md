[![pipeline status](https://gitlab.com/0bs1d1an/rgg/badges/master/pipeline.svg)](https://gitlab.com/0bs1d1an/rgg/commits/master)

# Risk graph generator (rgg)

This tool takes a CSV or YAML file with your observations and can output either a grid graph, or a donut ring.
It also accepts a CSV or YAML file with recommendations to output a recommendations grid.

## Rationale

I was fed-up with having to manually create these graphs for a client and I wanted to make my life easier.
And since I want to increase my Python skills some more, this would be a fun little project to catch two birds with one stone.

## Dependencies

1. argparse (dev-python/argparse);
2. matplotlib (dev-python/matplotlib);
3. python (dev-lang/python).

## Install

Using Pip:

`pip install --user rgg`

## Usage

You can use `rgg` in two ways:

* When installed as package, call the installed script: `rgg --help`.
* When Git cloned, call the package directly from the root of the Git repository: `python -m src.rgg --help`

```
$ rgg -h
usage: rgg [-h] (-iC INPUT_CSV_FILE | -iY INPUT_YAML_FILE) (-g | -d | -r)
           [-oP OUTPUT_PNG_FILE] [--axis-labels AXIS_LABELS]
           [--axis-arrows AXIS_ARROWS] [--legend LEGEND]

Converting scanning reports to a tabular format

optional arguments:
  -h, --help            show this help message and exit
  -iC INPUT_CSV_FILE, --input-csv-file INPUT_CSV_FILE
                        specify an input CSV file (e.g. observations.csv).
  -iY INPUT_YAML_FILE, --input-yaml-file INPUT_YAML_FILE
                        specify an input YAML file (e.g. observations.yml).
  -g, --grid            generate a risk grid graph.
  -d, --donut           generate a risk donut.
  -r, --recommendations
                        generate a risk recommendations graph.
  -oP OUTPUT_PNG_FILE, --output-png-file OUTPUT_PNG_FILE
                        specify an output PNG file (e.g. risk.png).
  --axis-labels         specify to print the axis labels
  --axis-arrows         specify to print arrows along the axis
```

## Example

A few examples

### Risk grid graph

To generate a risk grid graph: `$ rgg -iC example/input/observations.csv -oP example/output/grid.png -g`

Or if you prefer YAML: `$ rgg -iY example/input/observations.yaml -oP example/output/grid.png -g`

![Grid](example/output/grid.png)

### Risk donut

To generate a risk donut: `$ rgg -iC example/input/observations.csv -oP example/output/donut.png -d`

Or if you prefer YAML: `$ rgg -iY example/input/observations.yaml -oP example/output/donut.png -d`

![Donut](example/output/donut.png)

### Risk recommendations

To generate a recommendations graph: `$ rgg -iC example/input/recommendations.csv -oP example/output/recommendations.png -r`

Or if you prefer YAML: `$ rgg -iY example/input/recommendations.yaml -oP example/output/recommendations.png -r`

![Recommendations](example/output/recommendations.png)
