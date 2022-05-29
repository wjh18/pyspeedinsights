from src.pyspeedinsights.core.excel import ExcelWorkbook
from .sample_data import audit_results, metrics_results


def run_tests():
    test_write_to_worksheet(setup_data())

def setup_data():
    workbook = ExcelWorkbook(
        'https://www.example.com', audit_results, metrics_results)
    return workbook

def test_write_to_worksheet(workbook):
    workbook.setup_worksheet()
    workbook.write_to_worksheet()