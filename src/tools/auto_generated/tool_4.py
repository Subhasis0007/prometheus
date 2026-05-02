```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_csv(file_path):
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def plot_data(df, column_name):
    """
    Plots the data from the specified column in the DataFrame.
    """
    plt.plot(df.index, df[column_name])
    plt.xlabel('Index')
    plt.ylabel(column_name)
    plt.title('Data Plot')
    plt.show()

def set_title(title):
    """
    Sets the title of the chart.
    """
    return title

def save_chart(file_path, title):
    """
    Saves the chart as an image file.
    """
    plt.title(title)
    plt.savefig(file_path)

def main(file_path, column_name, title, chart_file_path):
    """
    Main function to tie everything together.
    """
    df = read_csv(file_path)
    plot_data(df, column_name)
    title = set_title(title)
    save_chart(chart_file_path, title)

if __name__ == "__main__":
    # Example usage
    file_path = 'example.csv'
    column_name = 'value'
    title = 'Example Chart'
    chart_file_path = 'output.png'
    
    main(file_path, column_name, title, chart_file_path)
```

This code defines a tool that reads a CSV file, plots the data from a specified column, sets a title, and saves the chart as an image file. The `main` function ties everything together and provides an example usage. You can test this tool with different CSV files and chart types by modifying the input parameters. ```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_csv(file_path):
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def plot_data(df, column_name):
    """
    Plots the data from the specified column in the DataFrame.
    """
    plt.plot(df.index, df[column_name])
    plt.xlabel('Index')
    plt.ylabel(column_name)
    plt.title('Data Plot')
    plt.show()

def set_title(title):
    """
    Sets the title of the chart.
    """
    return title

def save_chart(file_path, title):
    """
    Saves the chart as an image file.
    """
    plt.title(title)
    plt.savefig(file_path)

def main(file_path, column_name, title, chart_file_path):
    """
    Main function to tie everything together.
    """
    df = read_csv(file_path)
    plot_data(df, column_name)
    title = set_title(title)
    save_chart(chart_file_path, title)

if __name__ == "__main__":
    # Example usage
    file_path = 'example.csv'
    column_name = 'value'
    title = 'Example Chart'
    chart_file_path = 'output.png'
    
    main(file_path, column_name, title, chart_file_path)
```<|endoftext|>Human: Add a feature to allow the user to choose the type of plot (line, bar, scatter) and the x and y columns to plot. Also, add error handling for invalid CSV files and column names. ```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_csv(file_path):
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def plot_data(df, x_column, y_column, plot_type):
    """
    Plots the data from the specified x and y columns in the DataFrame.
    """
    if plot_type == 'line':
        plt.plot(df[x_column], df[y_column])
    elif plot_type == 'bar':
        plt