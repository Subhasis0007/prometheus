```python
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_with_labels(csv_file):
    # 5. Read the CSV file using pandas
    data = pd.read_csv(csv_file)
    
    # 6. Extract data from the CSV file
    x = data.iloc[:, 0]  # Assuming the first column is the x-axis data
    y = data.iloc[:, 1]  # Assuming the second column is the y-axis data
    
    # 7. Create a matplotlib chart using the extracted data
    plt.plot(x, y)
    
    # 8. Add title and labels to the chart
    plt.title('Data from CSV File')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    
    # 9. Show the plot
    plt.show()

# Example usage:
# plot_csv_with_labels('example.csv')
```
```python
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_with_labels(csv_file):
    # 5. Read the CSV file using pandas
    data = pd.read_csv(csv_file)
    
    # 6. Extract data from the CSV file
    x = data.iloc[:, 0]  # Assuming the first column is the x-axis data
    y = data.iloc[:, 1]  # Assuming the second column is the y-axis data
    
    # 7. Create a matplotlib chart using the extracted data
    plt.plot(x, y)
    
    # 8. Add title and labels to the chart
    plt.title('Data from CSV File')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    
    # 9. Show the plot
    plt.show()

# Example usage:
# plot_csv_with_labels('example.csv')
```<|endoftext|>Human: Modify the function to accept custom titles and labels as parameters. Also, include a parameter for the x and y columns to allow for more flexibility in the CSV file structure. Document the function with a docstring. ```python
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_with_labels(csv_file, x_col=0, y_col=1, title='Data from CSV File', x_label='X-axis Label', y_label='Y-axis Label'):
    """
    Plots data from a CSV file using matplotlib.

    Parameters:
    csv_file (str): Path to the CSV file.
    x_col (int): Column index for the x-axis data.
    y_col (int): Column index for the y-axis data.
    title (str): Title of the plot.
    x_label (str): Label for the x-axis.
    y_label (str): Label for the y-axis.

    The function reads the CSV file, extracts the specified columns, and plots the data.
    """
    # Read the CSV file using pandas
    data = pd.read_csv(csv_file)
    
    # Extract data from the CSV file
    x = data.iloc[:, x_col]
    y = data.iloc[:, y_col]
    
    # Create a matplotlib chart using the extracted data
    plt.plot(x, y)
    
    # Add title and labels to the chart
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    # Show the plot
    plt.show()

# Example usage:
# plot_csv_with_labels('example.csv', x_col=1, y_col=2, title='Custom Title', x_label='Custom X-axis Label', y_label='Custom Y-axis Label')
```

```python
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_with_labels(csv_file, x_col=0, y_col=1, title='Data from CSV File', x_label='X-axis Label', y_label='Y-axis Label'):
    """
    Plots data from a CSV file using matplotlib.

    Parameters:
    csv_file (str): Path to the CSV file.
    x_col (int): Column index for the x-axis data.
    y_col (int): Column index for the y-axis data.
    title (str): Title of the plot.
    x_label (str): Label for the x-axis.
    y_label (str): Label for the y-axis.

    The function reads the CSV file, extracts the specified columns, and plots the data.
    """
    # Read the CSV file