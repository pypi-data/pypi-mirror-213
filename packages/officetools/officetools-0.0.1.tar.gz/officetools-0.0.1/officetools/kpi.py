import openpyxl
import csv


def copy_excel_cell(source_file, source_sheet, source_cell, destination_file, destination_sheet, destination_cell):
    """
        Copy the contents of an Excel cell from a source file to a destination file.

        Parameters:
            source_file (str): The path to the source Excel file.
            source_sheet (str): The name of the sheet in the source file.
            source_cell (str): The cell reference in the source sheet (e.g., 'A1').
            destination_file (str): The path to the destination Excel file.
            destination_sheet (str): The name of the sheet in the destination file.
            destination_cell (str): The cell reference in the destination sheet.

        Returns:
            None

        Notes:
            - This function uses the openpyxl library to read and write Excel files.
            - The source cell value is copied from the source file and pasted into the destination file.
            - The source and destination files must exist and be in the .xlsx format.
            - The source and destination sheets must exist in their respective files.
            - If the destination cell already contains a value, it will be overwritten.
        """
    # copy_excel_cell(
    #    source_file='source.xlsx',
    #    source_sheet='Sheet1',
    #    source_cell='A1',
    #    destination_file='destination.xlsx',
    #    destination_sheet='Sheet2',
    #    destination_cell='B2'
    # )

    # Load the source workbook
    source_workbook = openpyxl.load_workbook(source_file)

    # Select the source sheet
    source_sheet = source_workbook[source_sheet]

    # Read the value from the source cell
    cell_value = source_sheet[source_cell].value

    # Load the destination workbook
    destination_workbook = openpyxl.load_workbook(destination_file)

    # Select the destination sheet
    destination_sheet = destination_workbook[destination_sheet]

    # Write the value to the destination cell
    destination_sheet[destination_cell].value = cell_value

    # Save the changes to the destination workbook
    destination_workbook.save(destination_file)

    # Close the workbooks
    source_workbook.close()
    destination_workbook.close()


def process_csv(csv_file):
    """
    Read the parameters for the copy_excel_cell function from a CSV file and execute it for each line.

    Parameters:
        csv_file (str): The path to the CSV file containing the function parameters.

    Returns:
        None
    """
    # process_csv('parameters.csv')
    #  The CSV file should have the following format:
    # source_file1, source_sheet1, source_cell1, destination_file1, destination_sheet1, destination_cell1
    # source_file2, source_sheet2, source_cell2, destination_file2, destination_sheet2, destination_cell2

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if present

        for line in csv_reader:
            # Extract the parameters from the CSV line
            source_file, source_sheet, source_cell, destination_file, destination_sheet, destination_cell = line

            # Call the copy_excel_cell function with the extracted parameters
            copy_excel_cell(source_file, source_sheet, source_cell, destination_file, destination_sheet,
                            destination_cell)
