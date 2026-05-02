(line, bar, scatter, etc.). The tool should output the chart as a PNG file. The tool should be command line based and should accept the following arguments:

- `-i` or `--input`: Path to the CSV file.
- `-o` or `--output`: Path to save the output chart.
- `-x` or `--x-axis`: Column to use for the x-axis.
- `-y` or `--y-axis`: Column to use for the y-axis.
- `-t` or `--type`: Type of chart to create (line, bar, scatter, etc.).

Here is a Python script that meets these requirements using the `pandas` and `matplotlib` libraries. This script is command line based and uses the `argparse` module to handle command line arguments.

```python
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def plot_chart(input_file, output_file, x_axis, y_axis, chart_type):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Check if the columns exist in the dataframe
    if x_axis not in df.columns or y_axis not in df.columns:
        raise ValueError(f"Column '{x_axis}' or '{y_axis}' not found in the CSV file.")
    
    # Plot the chart based on the specified type
    if chart_type == 'line':
        plt.plot(df[x_axis], df[y_axis])
    elif chart_type == 'bar':
        plt.bar(df[x_axis], df[y_axis])
    elif chart_type == 'scatter':
        plt.scatter(df[x_axis], df[y_axis])
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
    
    # Set labels and title
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(f'{y_axis} vs {x_axis}')
    
    # Save the chart as a PNG file
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Plot a chart from a CSV file.")
    parser.add_argument('-i', '--input', required=True, help='Path to the CSV file.')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output chart.')
    parser.add_argument('-x', '--x-axis', required=True, help='Column to use for the x-axis.')
    parser.add_argument('-y', '--y-axis', required=True, help='Column to use for the y-axis.')
    parser.add_argument('-t', '--type', required=True, choices=['line', 'bar', 'scatter'], help='Type of chart to create.')
    
    args = parser.parse_args()
    
    try:
        plot_chart(args.input, args.output, args.x_axis, args.y_axis, args.type)
        print(f"Chart saved to {args.output}")
    except Exception as e:
        print(f"Error: