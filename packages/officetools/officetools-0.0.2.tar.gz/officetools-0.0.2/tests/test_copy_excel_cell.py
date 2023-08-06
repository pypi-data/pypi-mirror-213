import pytest
import openpyxl
from officetools.kpi import copy_excel_cell

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

def test_copy_excel_cell(source_file, destination_file):
    # Set up the test data
    source_sheet = "Sheet1"
    source_cell = "A1"
    destination_sheet = "Sheet2"
    destination_cell = "B2"

    # Call the function being tested
    copy_excel_cell(
        source_file,
        source_sheet,
        source_cell,
        destination_file,
        destination_sheet,
        destination_cell
    )

    # Load the destination workbook
    destination_workbook = openpyxl.load_workbook(destination_file)
    destination_sheet = destination_workbook[destination_sheet]

    # Check if the value was copied correctly
    assert destination_sheet[destination_cell].value == "Test Value"

    # Clean up the temporary files
    destination_workbook.close()
    source_file.unlink()
    destination_file.unlink()
