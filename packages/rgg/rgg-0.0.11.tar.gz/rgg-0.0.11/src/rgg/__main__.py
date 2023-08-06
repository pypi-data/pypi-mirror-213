#!/usr/bin/env python3

""" Risk graph generator (rgg) """

import argparse
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import pkg_resources
import yaml
# from pprint import pprint

numbers = []
observation_names = []
amount_of_observations = []
risk_rating = []
mylabels = []
x_coords = []
y_coords = []
fixed = []


def get_args():
    """ Get arguments """

    parser = argparse.ArgumentParser(
        description='Converting scanning reports to a tabular format')
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-iC', '--input-csv-file',
        help='specify an input CSV file (e.g. observations.csv).')
    input_group.add_argument(
        '-iY', '--input-yaml-file',
        help='specify an input YAML file (e.g. observations.yml).')
    render_group = parser.add_mutually_exclusive_group(required=True)
    render_group.add_argument(
        '-g', '--grid', action='store_true', help='generate a risk grid plot.')
    render_group.add_argument(
        '-d', '--donut', action='store_true', help='generate a risk donut.')
    render_group.add_argument(
        '-r', '--recommendations', action='store_true',
        help='generate a risk recommendations plot.')
    parser.add_argument(
        '-oP', '--output-png-file',
        help='specify an output PNG file (e.g. risk.png).')
    parser.add_argument(
        '--axis-labels', action='store_true',
        help='specify to print the axis labels')
    parser.add_argument(
        '--axis-arrows', action='store_true',
        help='specify to print arrows along the axis')
    return parser.parse_args()


def load_risk_csv(args):
    """ Import CSV and translate Likelihood and Impact to numbers """

    amount_high = 0
    amount_medium = 0
    amount_low = 0

    with open(args.input_csv_file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)
        for row in data:
            numbers.append(row[0])
            observation_names.append(row[1])
            risk_rating.append(row[4])
            if row[2] == "H":
                x = 450
            elif row[2] == "M":
                x = 300
            elif row[2] == "L":
                x = 150
            if row[3] == "H":
                y = 300
            elif row[3] == "M":
                y = 200
            elif row[3] == "L":
                y = 100
            if row[4] == "H":
                amount_high += 1
            elif row[4] == "M":
                amount_medium += 1
            elif row[4] == "L":
                amount_low += 1
            x_coords.append(x)
            y_coords.append(y)
            fixed.append(row[5])

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])

    return amount_low, amount_medium, amount_high


def load_risk_yaml(args):
    """ Import YAML and translate Likelihood and Impact to numbers """

    amount_high = 0
    amount_medium = 0
    amount_low = 0

    with open(args.input_yaml_file, newline='') as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        for key, value in data.items():
            numbers.append(key)
            observation_names.append(value.get('name'))
            risk_rating.append(value.get('risk'))
            if value.get('likelihood') == "H":
                x = 450
            elif value.get('likelihood') == "M":
                x = 300
            elif value.get('likelihood') == "L":
                x = 150
            if value.get('impact') == "H":
                y = 300
            elif value.get('impact') == "M":
                y = 200
            elif value.get('impact') == "L":
                y = 100
            if value.get('risk') == "H":
                amount_high += 1
            elif value.get('risk') == "M":
                amount_medium += 1
            elif value.get('risk') == "L":
                amount_low += 1
            x_coords.append(x)
            y_coords.append(y)
            fixed.append(value.get('fixed'))

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])

    return amount_low, amount_medium, amount_high


def load_recommendations_csv(args):
    """ Import CSV and translate Likelihood and Impact to numbers """

    with open(args.input_csv_file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)
        for row in data:
            numbers.append(row[0])
            observation_names.append(row[1])
            if row[2] == "H":
                x = 450
            elif row[2] == "M":
                x = 300
            elif row[2] == "L":
                x = 150
            if row[3] == "H":
                y = 300
            elif row[3] == "M":
                y = 200
            elif row[3] == "L":
                y = 100
            x_coords.append(x)
            y_coords.append(y)

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])


def load_recommendations_yaml(args):
    """ Import YAML and translate Likelihood and Impact to numbers """

    with open(args.input_yaml_file, newline='') as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        for key, value in data.items():
            numbers.append(key)
            observation_names.append(value.get('name'))
            if value.get('complexity') == "H":
                x = 450
            elif value.get('complexity') == "M":
                x = 300
            elif value.get('complexity') == "L":
                x = 150
            if value.get('risk_mitigation') == "H":
                y = 300
            elif value.get('risk_mitigation') == "M":
                y = 200
            elif value.get('risk_mitigation') == "L":
                y = 100
            x_coords.append(x)
            y_coords.append(y)

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])


def donut(args, amount_low, amount_medium, amount_high):
    """ Ring functions """

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))

    # Ring width size
    size = 0.25

    data = amount_high, amount_medium, amount_low
    colors = ["red", "orange", "yellow"]

    # Plot wedges
    ax.pie(
        data, wedgeprops=dict(width=size, edgecolor="black", linewidth=1),
        startangle=90, colors=colors, labels=data)

    # Determine exposure_level
    largest_index = data.index(max(data))
    if largest_index == 0:
        exposure_level = "High"
    elif largest_index == 1:
        exposure_level = "Medium"
    elif largest_index == 2:
        exposure_level = "Low"

    # Print exposure level
    ax.text(
        0.5, 0.53, "Exposure level", transform=ax.transAxes, fontsize=16,
        horizontalalignment='center', verticalalignment='center')
    ax.text(
        0.5, 0.45, exposure_level, transform=ax.transAxes, fontsize=24,
        horizontalalignment='center', verticalalignment='center',
        weight='bold')

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(
            args.output_png_file, transparent=True, dpi=200,
            bbox_inches='tight')


def grid(args):
    """ Grid function """

    # Background
    grid_bg = pkg_resources.resource_stream(__name__, 'data/grid-bg.png')
    img = plt.imread(grid_bg)

    # Axis spacing values
    x_axis_spacing = plticker.MultipleLocator(base=150)
    y_axis_spacing = plticker.MultipleLocator(base=100)

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 450, 0, 300])

    # Plot observations with a sequential offset inside their quadrant
    if x_coords and y_coords:

        # Build list of sequential x and y offsets
        x_seq = list(range(0, 130, 20))
        y_seq = list(range(0, 80, 20))

        x_plus_y = list(zip(x_coords, y_coords))
        new_x_plus_y = []
        for coord in x_plus_y:
            old_coord = [coord[0], coord[1]]
            if old_coord not in new_x_plus_y:
                new_x_plus_y.append(old_coord)
            else:
                for y_offset in y_seq:
                    plotted = False
                    for x_offset in x_seq:
                        new_coord = [coord[0] + x_offset, coord[1] - y_offset]
                        if new_coord not in new_x_plus_y:
                            new_x_plus_y.append(new_coord)
                            plotted = True
                            break
                    if plotted is True:
                        break

        all_x = []
        all_y = []
        for x, _ in new_x_plus_y:
            all_x.append(x - 135)
        for _, y in new_x_plus_y:
            all_y.append(y - 15)

        for number, i, name, risk, x, y, obs_fixed in zip(
                numbers, amount_of_observations, observation_names,
                risk_rating, all_x, all_y, fixed):

            # Actual plotting of observations
            if risk == 'H':
                if obs_fixed == '1':
                    ax.text(
                        x+0, y-3, number, fontsize=7,
                        horizontalalignment='center', color='white',
                        weight='bold')
                    ax.scatter(
                        x, y, marker='o', c='#e20000', s=200,
                        edgecolors='white', hatch='////')
                    ax.scatter(
                        x, y, marker='o', c='#ffffff00', s=200,
                        edgecolors='black')
                else:
                    ax.scatter(
                        x, y, marker='o', c='#e20000', s=200,
                        edgecolors='black')
                    ax.text(
                        x+0, y-3, number, fontsize=7,
                        horizontalalignment='center', color='white',
                        weight='bold')
            elif risk == 'M':
                if obs_fixed == '1':
                    ax.text(
                        x+0, y-3, number, fontsize=7,
                        horizontalalignment='center', color='white',
                        weight='bold')
                    ax.scatter(
                        x, y, marker='o', c='#fecb00', s=200,
                        edgecolors='white', hatch='////')
                    ax.scatter(
                        x, y, marker='o', c='#ffffff00', s=200,
                        edgecolors='black')
                else:
                    ax.scatter(
                        x, y, marker='o', c='#fecb00', s=200,
                        edgecolors='black')
                    ax.text(
                        x+0, y-3, number, fontsize=7,
                        horizontalalignment='center', color='white',
                        weight='bold')
            elif risk == 'L':
                if obs_fixed == '1':
                    ax.text(
                        x+0, y-3, number, fontsize=7,
                        horizontalalignment='center', color='#00000080',
                        weight='bold')
                    ax.scatter(
                        x, y, marker='o', c='#ffff80', s=200,
                        edgecolors='#00000080', hatch='////')
                    ax.scatter(
                        x, y, marker='o', c='#ffffff00', s=200,
                        edgecolors='black')
                else:
                    ax.scatter(
                        x, y, marker='o', c='#ffff00', s=200,
                        edgecolors='black')
                    ax.text(
                        x+0, y-3, number, fontsize=7,
                        horizontalalignment='center', color='black',
                        weight='bold')

    # Hide axis numbers
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Grid spacing
    ax.xaxis.set_major_locator(x_axis_spacing)
    ax.yaxis.set_major_locator(y_axis_spacing)

    # Print arrows along axis
    if args.axis_arrows:
        ax.annotate(
            'High', va="center", xy=(0, -0.07), xycoords='axes fraction',
            xytext=(1, -0.07), arrowprops=dict(arrowstyle="<-", color='black'))
        ax.annotate(
            'High', ha="center", xy=(-0.05, 0), xycoords='axes fraction',
            xytext=(-0.05, 1), arrowprops=dict(arrowstyle="<-", color='black'))

    # Print axis labels
    if args.axis_labels:
        plt.xlabel("Likelihood", labelpad=20)
        plt.ylabel("Impact", labelpad=20)

    # Print grid
    plt.grid(color='black', alpha=0.5, linestyle='--')

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(
            args.output_png_file, transparent=True, dpi=200,
            bbox_inches='tight')


def recommendations(args):
    """ Grid function """

    # Background
    recommendations_bg = pkg_resources.resource_stream(
        __name__, 'data/recommendations-bg.png')
    img = plt.imread(recommendations_bg)

    # Axis spacing values
    x_axis_spacing = plticker.MultipleLocator(base=150)
    y_axis_spacing = plticker.MultipleLocator(base=100)

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 450, 0, 300])

    # Plot recommendations with a sequential offset inside their quadrant
    if x_coords and y_coords:

        # Build list of sequential x and y offsets
        x_seq = list(range(0, 120, 25))
        y_seq = list(range(0, 80, 25))

        x_plus_y = list(zip(x_coords, y_coords))
        new_x_plus_y = []
        for coord in x_plus_y:
            old_coord = [coord[0], coord[1]]
            if old_coord not in new_x_plus_y:
                new_x_plus_y.append(old_coord)
            else:
                for y_offset in y_seq:
                    plotted = False
                    for x_offset in x_seq:
                        new_coord = [coord[0] + x_offset, coord[1] - y_offset]
                        if new_coord not in new_x_plus_y:
                            new_x_plus_y.append(new_coord)
                            plotted = True
                            break
                    if plotted is True:
                        break

        all_x = []
        all_y = []
        for x, _ in new_x_plus_y:
            all_x.append(x - 125)
        for _, y in new_x_plus_y:
            all_y.append(y - 15)

        for number, i, name, x, y in zip(
                numbers, amount_of_observations, observation_names,
                all_x, all_y):

            # Actual plotting of recommendations
            ax.scatter(
                x, y, marker='o', c='#4f81bd', s=250, edgecolors='black')
            ax.text(
                x+0, y-3, number, fontsize=6, horizontalalignment='center',
                color='white', weight='bold')

    # Hide axis numbers
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Grid spacing
    ax.xaxis.set_major_locator(x_axis_spacing)
    ax.yaxis.set_major_locator(y_axis_spacing)

    # Print arrows along axis
    if args.axis_arrows:
        ax.annotate(
            'High', va="center", xy=(0, -0.07), xycoords='axes fraction',
            xytext=(1, -0.07), arrowprops=dict(arrowstyle="<-", color='black'))
        ax.annotate(
            'High', ha="center", xy=(-0.05, 0), xycoords='axes fraction',
            xytext=(-0.05, 1), arrowprops=dict(arrowstyle="<-", color='black'))

    # Print axis labels
    if args.axis_labels:
        plt.xlabel("Likelihood", labelpad=20)
        plt.ylabel("Impact", labelpad=20)

    # Print grid
    plt.grid(color='black', alpha=0.5, linestyle='--')

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(
            args.output_png_file, transparent=True, dpi=200,
            bbox_inches='tight')


def main():
    """ Main function """

    args = get_args()

    if args.donut or args.grid:
        if args.input_csv_file:
            amount_high, amount_medium, amount_low = load_risk_csv(args)
        elif args.input_yaml_file:
            amount_low, amount_medium, amount_high = load_risk_yaml(args)
        print(amount_high)
    elif args.recommendations:
        if args.input_csv_file:
            load_recommendations_csv(args)
        elif args.input_yaml_file:
            load_recommendations_yaml(args)

    if args.donut:
        donut(args, amount_low, amount_medium, amount_high)
    if args.grid:
        grid(args)
    if args.recommendations:
        recommendations(args)


if __name__ == '__main__':
    main()
