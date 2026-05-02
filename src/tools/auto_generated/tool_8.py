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