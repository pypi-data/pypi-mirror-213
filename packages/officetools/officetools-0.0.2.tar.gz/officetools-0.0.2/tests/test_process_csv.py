import pytest
import csv
import openpyxl
from officetools.kpi import copy_excel_cell, process_csv

@pytest.fixture
def source_file(tmp_path):
    # Create a temporary source file for testing
    file_path = tmp_path / "source.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet["A1"].value = "Test Value"
    workbook.save(file_path)
    return file_path

@pytest.fixture
def destination_file(tmp_path):
    # Create a temporary destination file for testing
    file_path = tmp_path / "destination.xlsx"
    return file_path

def create_csv_file(tmp_path, rows):
    # Create a temporary CSV file with the specified rows
    file_path = tmp_path / "test_parameters.csv"
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["source_file", "source_sheet", "source_cell", "destination_file", "destination_sheet", "destination_cell"])
        writer.writerows(rows)
    return file_path

def test_process_csv(source_file, destination_file, tmp_path):
    # Set up the test data
    csv_rows = [
        ["source.xlsx", "Sheet1", "A1", "destination.xlsx", "Sheet2", "B2"],
        ["source.xlsx", "Sheet3", "C5", "destination.xlsx", "Sheet4", "D6"],
        # Add more test cases as needed
    ]
    csv_file = create_csv_file(tmp_path, csv_rows)

    # Call the function being tested
    process_csv(csv_file)

    # Load the destination workbook
    destination_workbook = openpyxl.load_workbook(destination_file)

    # Check if the values were copied correctly for each row
    for row in csv_rows:
        source_sheet, source_cell, destination_sheet, destination_cell = row[1:5]
        expected_value = destination_workbook[destination_sheet][destination_cell].value
        assert expected_value == "Test Value"

    # Clean up the temporary files
    destination_workbook.close()
    source_file.unlink()
    destination_file.unlink()
    csv_file.unlink()
