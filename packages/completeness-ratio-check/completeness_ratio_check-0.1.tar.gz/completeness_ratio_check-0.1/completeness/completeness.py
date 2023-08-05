# mypackage/mypackage/completeness.py
import pandas as pd
import matplotlib.pyplot as plt

def calculate_completeness(file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path, na_values=["null", "?", "UNKNOWN", "unknown", "NOT SPECIFIED", "not specified", ""])

    # Initialize scan report variables
    scan_report = []
    total_rows = len(df)

    # Calculate completeness ratios for each variable
    completeness_ratios = {}

    for column in df.columns:
        variable_name = column
        n_rows = len(df[column])
        n_rows_checked = total_rows - df[column].isnull().sum()
        fraction_empty = df[column].isnull().sum() / total_rows * 100
        completeness_ratio = (n_rows_checked / n_rows) * 100

        # Add variable scan report to the list
        scan_report.append({
            'Field': variable_name,
            'N rows': n_rows,
            'N rows checked': n_rows_checked,
            'Fraction Empty': f"{fraction_empty:.2f}%",
            'Completeness ratio for variable': f"{completeness_ratio:.2f}%"
        })

        # Save completeness ratio for bar chart
        completeness_ratios[variable_name] = completeness_ratio

    # Calculate overall completeness ratio for the whole sheet
    overall_completeness = sum(df.count()) / (total_rows * len(df.columns)) * 100

    # Add whole sheet scan report to the list
    scan_report.append({
        'Field': 'Whole Sheet',
        'N rows': total_rows,
        'N rows checked': sum(df.count()),
        'Fraction Empty': f"{(total_rows * len(df.columns) - sum(df.count())) / (total_rows * len(df.columns)) * 100:.2f}%",
        'Completeness ratio for variable': f"{overall_completeness:.2f}%"
    })

    # Create a bar chart
    variable_names = list(completeness_ratios.keys())
    completeness_values = list(completeness_ratios.values())

    plt.bar(variable_names, completeness_values)
    plt.xlabel('Variable')
    plt.ylabel('Completeness Ratio (%)')
    plt.title('Completeness Ratio for Each Variable')
    plt.xticks(rotation=90)
    plt.show()

    return scan_report
