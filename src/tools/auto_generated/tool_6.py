import pandas as pd
import matplotlib.pyplot as plt

def create_csv_chart(file_path, x_column, y_column):
    """
    Creates a matplotlib chart from a CSV file.

    :param file_path: Path to the CSV file.
    :param x_column: Name of the column to use for the x-axis.
    :param y_column: Name of the column to use for the y-axis.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if the required columns exist in the DataFrame
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError(f"Missing column: {x_column} or {y_column}")

        # Create the chart
        plt.figure(figsize=(10, 6))
        plt.plot(df[x_column], df[y_column], marker='o')
        plt.title(f"Chart of {y_column} vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# create_csv_chart('data.csv', 'Date', 'Temperature')